from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ARTIFACT_TYPES = {
    "software", "process", "product", "document", "policy",
    "operation", "analysis", "experiment", "decision",
}
STATES = {"hypothesis", "experiment", "provisional", "implemented", "validated", "monitored", "reopened"}
RISK_LEVELS = {"low", "medium", "high"}


class ManifestError(ValueError):
    pass


@dataclass(frozen=True)
class Artifact:
    id: str
    name: str
    kind: str
    purpose: str
    owner: str
    risk: str = "medium"
    state: str = "hypothesis"
    claims: tuple[str, ...] = field(default_factory=tuple)
    evidence: tuple[str, ...] = field(default_factory=tuple)
    reopening_triggers: tuple[str, ...] = field(default_factory=tuple)
    not_proven: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Artifact":
        def items(key: str) -> tuple[str, ...]:
            value = raw.get(key, [])
            if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
                raise ManifestError(f"{key} must be a list of non-empty strings")
            return tuple(value)
        return cls(
            id=str(raw.get("id", "")), name=str(raw.get("name", "")), kind=str(raw.get("kind", "")),
            purpose=str(raw.get("purpose", "")), owner=str(raw.get("owner", "")),
            risk=str(raw.get("risk", "")), state=str(raw.get("state", "")),
            claims=items("claims"), evidence=items("evidence"),
            reopening_triggers=items("reopening_triggers"), not_proven=items("not_proven"),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.id or not self.name or not self.purpose or not self.owner:
            errors.append("id, name, purpose and owner are required")
        if self.kind not in ARTIFACT_TYPES:
            errors.append(f"kind must be one of: {', '.join(sorted(ARTIFACT_TYPES))}")
        if self.risk not in RISK_LEVELS:
            errors.append(f"risk must be one of: {', '.join(sorted(RISK_LEVELS))}")
        if self.state not in STATES:
            errors.append(f"state must be one of: {', '.join(sorted(STATES))}")
        if not self.claims:
            errors.append("at least one material claim is required")
        if self.state in {"validated", "monitored"} and not self.evidence:
            errors.append("validated or monitored artifacts require evidence")
        if self.risk == "high" and not self.reopening_triggers:
            errors.append("high-risk artifacts require reopening triggers")
        if self.state in {"validated", "monitored"} and not self.not_proven:
            errors.append("validated artifacts must declare what is not proven")
        return errors


def load_manifest(path: str | Path) -> list[Artifact]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("artifacts"), list):
        raise ManifestError("manifest must contain an artifacts list")
    artifacts = [Artifact.from_dict(item) for item in raw["artifacts"]]
    ids = [a.id for a in artifacts]
    if len(ids) != len(set(ids)):
        raise ManifestError("artifact ids must be unique")
    return artifacts


def validate_manifest(path: str | Path) -> dict[str, Any]:
    try:
        artifacts = load_manifest(path)
    except (OSError, json.JSONDecodeError, ManifestError) as exc:
        return {"ok": False, "errors": [str(exc)], "artifacts": 0}
    errors = [f"{artifact.id}: {error}" for artifact in artifacts for error in artifact.validate()]
    return {"ok": not errors, "errors": errors, "artifacts": len(artifacts)}
