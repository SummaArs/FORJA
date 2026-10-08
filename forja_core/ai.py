from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AIProvider:
    id: str
    label: str
    command: str | None
    free: bool
    mode: str


PROVIDERS = (
    AIProvider("ollama", "Ollama — modelo local", "ollama", True, "local"),
    AIProvider("gemini", "Gemini CLI — cota gratuita", "gemini", True, "cloud-free-tier"),
    AIProvider("aider", "Aider — agente de terminal", "aider", True, "local-or-free-model"),
    AIProvider("opencode", "OpenCode — agente de terminal", "opencode", True, "local-or-free-model"),
)


def discover_providers(environ: dict[str, str] | None = None) -> list[dict[str, object]]:
    env = os.environ if environ is None else environ
    result = []
    for provider in PROVIDERS:
        available = bool(provider.command and shutil.which(provider.command))
        result.append({"id": provider.id, "label": provider.label, "available": available, "free": provider.free, "mode": provider.mode})
    if env.get("FORJA_AI_COMMAND"):
        result.append({"id": "custom", "label": "Comando gratuito configurado pelo usuário", "available": True, "free": True, "mode": "custom"})
    return result


def choose_provider(preferred: str = "auto", environ: dict[str, str] | None = None) -> dict[str, object]:
    found = discover_providers(environ)
    if preferred != "auto":
        match = next((p for p in found if p["id"] == preferred), None)
        if not match or not match["available"]:
            raise RuntimeError(f"provedor gratuito indisponível: {preferred}")
        return match
    return next((p for p in found if p["available"] and p["free"]), {"id": "deterministic", "label": "Assistente local da FORJA", "available": True, "free": True, "mode": "deterministic"})


def explain_provider(preferred: str = "auto") -> str:
    provider = choose_provider(preferred)
    if provider["id"] == "deterministic":
        return "Nenhuma IA externa foi encontrada. A FORJA usará perguntas guiadas e regras locais, sem custo e sem enviar dados."
    return f"IA selecionada: {provider['label']}. A FORJA continua validando o resultado; a IA apenas ajuda a organizar ideias."


def run_free_command(command: str, prompt: str, timeout: int = 60) -> str:
    """Executa somente um comando explicitamente configurado pelo usuário."""
    completed = subprocess.run(command, input=prompt, text=True, shell=True, capture_output=True, timeout=timeout, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "o provedor gratuito falhou")
    return completed.stdout.strip()
