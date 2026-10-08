from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class BlueprintError(ValueError):
    pass


def _strings(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(x, str) and x.strip() for x in value):
        raise BlueprintError(f"{field} must be a non-empty list of strings")
    return value


def validate_spec(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("id", "name", "purpose", "target"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            errors.append(f"{field} is required")
    if spec.get("target") not in {"local", "ooncore", "odoo"}:
        errors.append("target must be local, ooncore or odoo")
    try:
        actors = _strings(spec.get("actors"), "actors")
        if len(actors) != len(set(actors)):
            errors.append("actors must be unique")
    except BlueprintError as exc:
        errors.append(str(exc))
    entities = spec.get("entities")
    if not isinstance(entities, list) or not entities:
        errors.append("entities must be a non-empty list")
    else:
        ids: list[str] = []
        for entity in entities:
            if not isinstance(entity, dict) or not isinstance(entity.get("id"), str) or not entity["id"].strip():
                errors.append("each entity requires an id")
                continue
            ids.append(entity["id"])
            if not isinstance(entity.get("fields"), list) or not entity["fields"]:
                errors.append(f"entity {entity['id']} requires fields")
        if len(ids) != len(set(ids)):
            errors.append("entity ids must be unique")
    journeys = spec.get("journeys")
    if not isinstance(journeys, list) or not journeys:
        errors.append("journeys must be a non-empty list")
    else:
        for journey in journeys:
            if not isinstance(journey, dict) or not journey.get("id") or not journey.get("actor"):
                errors.append("each journey requires id and actor")
            elif journey["actor"] not in spec.get("actors", []):
                errors.append(f"journey actor is not declared: {journey['actor']}")
            if not isinstance(journey.get("steps"), list) or not journey["steps"]:
                errors.append(f"journey {journey.get('id', '<unknown>')} requires steps")
    controls = spec.get("controls", [])
    if not isinstance(controls, list) or not all(isinstance(x, str) and x.strip() for x in controls):
        errors.append("controls must be a list of strings")
    if spec.get("risk") == "high" and len(controls) < 2:
        errors.append("high-risk systems require at least two explicit controls")
    return errors


def compile_blueprint(spec: dict[str, Any]) -> dict[str, Any]:
    errors = validate_spec(spec)
    if errors:
        raise BlueprintError("; ".join(errors))
    entities = spec["entities"]
    journeys = spec["journeys"]
    actors = spec["actors"]
    permissions = {actor: [f"{journey['id']}:execute" for journey in journeys if journey["actor"] == actor] for actor in actors}
    return {
        "schema": "forja.enterprise.blueprint/v1",
        "identity": {key: spec[key] for key in ("id", "name", "purpose", "target")},
        "risk": {"level": spec.get("risk", "medium"), "controls": spec.get("controls", [])},
        "domain": {"entities": entities, "journeys": journeys},
        "frontend": {"routes": [{"path": f"/{j['id']}", "journey": j["id"], "actor": j["actor"]} for j in journeys], "component_boundaries": [f"features/{j['id']}" for j in journeys]},
        "backend": {"models": [e["id"] for e in entities], "validation_required": True, "authorization_required": True},
        "governance": {"actors": actors, "permissions": permissions, "deny_by_default": True, "audit_events": [f"{j['id']}.completed" for j in journeys]},
        "acceptance": {"journeys": [j["id"] for j in journeys], "required_checks": ["schema", "authorization", "validation", "audit", "recovery"], "not_proven": ["production deployment", "customer acceptance"]},
    }


def write_blueprint(spec_path: str | Path, output: str | Path) -> Path:
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    blueprint = compile_blueprint(spec)
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    (root / "blueprint.json").write_text(json.dumps(blueprint, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "frontend.routes.json").write_text(json.dumps(blueprint["frontend"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "backend.domain.json").write_text(json.dumps(blueprint["backend"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "governance.json").write_text(json.dumps(blueprint["governance"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "acceptance.json").write_text(json.dumps(blueprint["acceptance"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return root / "blueprint.json"
