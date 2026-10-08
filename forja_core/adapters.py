from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .workspace import init_workspace


def _slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")
    return result or "forja_app"


def plan(kind: str, target: str | Path, name: str) -> dict[str, Any]:
    if kind not in {"local", "ooncore", "odoo"}:
        raise ValueError("kind must be local, ooncore or odoo")
    return {"kind": kind, "target": str(Path(target).resolve()), "name": name, "plan_only": True, "apply_required": True, "requires": {"local": [], "ooncore": ["node", "npm", "published OonCore package"], "odoo": ["Odoo Community for runtime validation"]}[kind]}


def create_ooncore(target: str | Path, name: str, package_version: str = "0.7.8", apply: bool = False) -> dict[str, Any]:
    target = Path(target).resolve()
    package = f"@oondemand/create-central-oon@{package_version}"
    command = ["npx", "--yes", "--package", package, "create-central-oon", target.name, "--no-install"]
    result: dict[str, Any] = {"kind": "ooncore", "target": str(target), "package": package, "command": command, "apply": apply, "read_only": not apply}
    if not apply:
        return result
    target.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, cwd=str(target.parent), text=True, capture_output=True, check=False)
    result.update({"returncode": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]})
    result["ok"] = completed.returncode == 0 and (target / "central.app.json").exists()
    return result


def create_odoo(target: str | Path, name: str, version: str = "18.0", apply: bool = False) -> dict[str, Any]:
    target = Path(target).resolve()
    module = _slug(name)
    files = {
        "__init__.py": "from . import models\n",
        "__manifest__.py": f'''{{\n    "name": {name!r},\n    "version": "{version}.1.0.0",\n    "summary": "Módulo criado pela FORJA",\n    "category": "Tools",\n    "license": "LGPL-3",\n    "author": "FORJA",\n    "depends": ["base"],\n    "data": ["security/ir.model.access.csv", "views/{module}_views.xml"],\n    "installable": True,\n    "application": True,\n}}\n''',
        "models/__init__.py": "from . import record\n",
        "models/record.py": f'''from odoo import fields, models\n\n\nclass {module.title().replace("_", "")}(models.Model):\n    _name = "forja.{module}"\n    _description = {name!r}\n\n    name = fields.Char(required=True)\n    active = fields.Boolean(default=True)\n''',
        "security/ir.model.access.csv": f'''id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\naccess_{module}_user,{name} user,model_forja_{module},base.group_user,1,1,1,1\n''',
        f"views/{module}_views.xml": f'''<odoo>\n    <record id="view_{module}_list" model="ir.ui.view">\n        <field name="name">forja.{module}.list</field>\n        <field name="model">forja.{module}</field>\n        <field name="arch" type="xml"><list><field name="name"/><field name="active"/></list></field>\n    </record>\n    <record id="action_{module}" model="ir.actions.act_window">\n        <field name="name">{name}</field><field name="res_model">forja.{module}</field><field name="view_mode">list,form</field>\n    </record>\n    <menuitem id="menu_{module}" name="{name}" action="action_{module}"/>\n</odoo>\n''',
        "README.md": f"# {name}\n\nAddon Odoo Community gerado pela FORJA.\n\nValidar com o Odoo alvo antes da instalação.\n",
    }
    result: dict[str, Any] = {"kind": "odoo", "target": str(target), "module": module, "files": sorted(files), "apply": apply, "read_only": not apply}
    if not apply:
        return result
    for relative, content in files.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    result["ok"] = all((target / relative).exists() for relative in files)
    return result


def create_local(target: str | Path, name: str, owner: str = "Gustavo") -> dict[str, Any]:
    location = init_workspace(target, name, owner)
    return {"kind": "local", "target": str(location), "ok": True, "next_question": "Qual problema empresarial precisa mudar?"}
