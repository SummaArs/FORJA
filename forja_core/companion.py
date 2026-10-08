from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".next", "coverage"}
IGNORED_FILES = {"context.generated.md", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
TEXT_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".yaml", ".yml", ".toml", ".css", ".sh", ".sql", ".xml", ".csv"}


@dataclass(frozen=True)
class ContextFile:
    path: str
    score: int
    chars: int
    reason: str


def _files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.name in IGNORED_FILES or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        yield path


def _terms(task: str) -> set[str]:
    return {word.lower() for word in re.findall(r"[a-zA-ZÀ-ÿ0-9_]{3,}", task)}


def rank_files(root: str | Path, task: str, limit: int = 18) -> list[ContextFile]:
    root = Path(root).resolve()
    terms = _terms(task)
    ranked: list[ContextFile] = []
    for path in _files(root):
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lower = f"{relative}\n{text}".lower()
        score = sum(lower.count(term) for term in terms)
        reason = "termos da tarefa"
        if path.name.lower() in {"readme.md", "package.json", "pyproject.toml", "agents.md"}:
            score += 4
            reason = "contrato do projeto"
        if relative.startswith(("tests/", "test/", "src/", "app/", "forja_core/")):
            score += 2
        if score > 0:
            ranked.append(ContextFile(relative, score, len(text), reason))
    ranked.sort(key=lambda item: (-item.score, item.path))
    return ranked[:limit]


def _git(root: Path, args: list[str]) -> str:
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def build_packet(root: str | Path, task: str, budget: int = 12000, limit: int = 18) -> dict:
    root = Path(root).resolve()
    selected = rank_files(root, task, limit)
    files = []
    used = 0
    for item in selected:
        text = (root / item.path).read_text(encoding="utf-8", errors="ignore")
        remaining = max(0, budget - used)
        if remaining < 200:
            break
        # Evita que um log, manifesto gerado ou documento enorme monopolize o handoff.
        per_file_budget = max(1, min(remaining, max(200, budget // 8)))
        clipped = text[:per_file_budget]
        files.append({"path": item.path, "score": item.score, "reason": item.reason, "content": clipped})
        used += len(clipped)
    all_chars = sum(path.stat().st_size for path in _files(root))
    packet = {
        "schema": "forja.claude-companion/v1",
        "task": task,
        "root": str(root),
        "selection": {"files": [item.path for item in selected], "included": len(files), "budget_chars": budget, "used_chars": used, "repository_chars": all_chars, "estimated_reduction": round(1 - used / max(all_chars, 1), 4)},
        "git": {"branch": _git(root, ["branch", "--show-current"]), "status": _git(root, ["status", "--short"]), "diff_stat": _git(root, ["diff", "--stat"])},
        "instructions": ["Use only the included files as initial context.", "Inspect more files only when a dependency is proven.", "Run the project proof after changes.", "Report files changed, tests run, failures, and remaining uncertainty."],
        "files": files,
    }
    packet["fingerprint"] = hashlib.sha256(json.dumps(packet, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    return packet


def write_packet(root: str | Path, task: str, output: str | Path, budget: int = 12000, limit: int = 18) -> dict:
    packet = build_packet(root, task, budget, limit)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "context.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown = ["# FORJA — pacote de contexto para o agente", "", f"**Tarefa:** {task}", f"**Fingerprint:** `{packet['fingerprint']}`", "", "## Regras", *[f"- {rule}" for rule in packet["instructions"]], "", "## Estado Git", f"- branch: `{packet['git']['branch']}`", f"- status: `{packet['git']['status'] or 'limpo'}`", "", "## Arquivos selecionados"]
    for file in packet["files"]:
        markdown += ["", f"### `{file['path']}`", f"_score={file['score']} motivo={file['reason']}_", "", "```text", file["content"], "```"]
    (output / "CLAUDE_CONTEXT.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    return packet
