from __future__ import annotations

import json
import re
from pathlib import Path

from .blueprint import write_blueprint
from .workspace import init_workspace


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-") or "meu-projeto"


def create_quickstart(name: str, root: str | Path = ".", target: str = "local", owner: str = "Gustavo") -> dict[str, str]:
    base = Path(root).resolve() / _slug(name)
    init_workspace(base, name, owner)
    spec = {
        "id": _slug(name), "name": name, "purpose": "Transformar uma ideia em um sistema verificável.",
        "target": target, "risk": "low", "actors": ["owner"],
        "entities": [{"id": "item", "fields": ["name", "status"]}],
        "journeys": [{"id": "manage_item", "actor": "owner", "steps": ["criar item", "alterar status", "registrar auditoria"]}],
        "controls": ["permissão explícita"],
    }
    spec_path = base / "requirements.json"
    spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    blueprint_path = write_blueprint(spec_path, base / "blueprint")
    (base / "README.md").write_text(f"# {name}\n\nProjeto criado pela FORJA.\n\n1. Abra `requirements.json`.\n2. Diga o que o sistema deve fazer.\n3. Rode `./prove.sh` na FORJA.\n4. Escolha Local, OonCore ou Odoo.\n\nBlueprint inicial: `{blueprint_path.relative_to(base)}`.\n", encoding="utf-8")
    return {"project": str(base), "requirements": str(spec_path), "blueprint": str(blueprint_path), "next": "Abra requirements.json e conte qual problema o sistema resolve."}
