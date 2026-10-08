from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_workspace(path: str | Path, name: str, owner: str) -> Path:
    root = Path(path).resolve()
    (root / "forja").mkdir(parents=True, exist_ok=True)
    manifest = root / "forja" / "manifest.json"
    if not manifest.exists():
        manifest.write_text(json.dumps({"portfolio": name, "artifacts": []}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "forja" / "project.json").write_text(json.dumps({"name": name, "owner": owner, "created_at": _now(), "status": "discovery", "next_question": "Qual problema empresarial precisa mudar?"}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return root / "forja"


def inspect_repository(repo: str | Path, name: str = "ooncore") -> dict[str, Any]:
    """Read-only discovery. It never executes or modifies the target repository."""
    value = str(repo)
    path = Path(value).expanduser()
    is_local = path.exists() and path.is_dir()
    if is_local:
        files = {p.name for p in path.iterdir() if p.is_file()}
        directories = {p.name for p in path.iterdir() if p.is_dir()}
        signals = {
            "git": (path / ".git").exists(),
            "readme": any(name.lower().startswith("readme") for name in files),
            "agent_instructions": any(name in files for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md")),
            "proof_script": any(name in files for name in ("prove.sh", "Makefile", "package.json", "pyproject.toml")),
            "tests": "tests" in directories or "test" in directories,
        }
        return {"name": name, "source": str(path), "mode": "local-read-only", "signals": signals, "safe_to_connect": signals["git"] and signals["readme"]}
    return {"name": name, "source": value, "mode": "remote-reference", "signals": {"git": value.startswith(("https://", "git@"))}, "safe_to_connect": value.startswith(("https://", "git@"))}


def connect_repository(workspace: str | Path, repo: str | Path, name: str = "ooncore") -> dict[str, Any]:
    target = Path(workspace).resolve() / "forja"
    target.mkdir(parents=True, exist_ok=True)
    inspection = inspect_repository(repo, name)
    output = target / f"connection-{name}.json"
    record = {"connected_at": _now(), "read_only": True, **inspection}
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return record
