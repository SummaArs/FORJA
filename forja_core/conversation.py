from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

from .ai import choose_provider, explain_provider
from .blueprint import write_blueprint
from .workspace import init_workspace


def _slug(value: str) -> str:
    value = value.lower().replace("ã", "a").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ç", "c")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "meu-projeto"


def _words(text: str, fallback: str) -> list[str]:
    parts = [p.strip(" .,!?:;") for p in re.split(r",| e | ou |;", text, flags=re.I)]
    return [p.replace(" ", "_").lower() for p in parts if p.strip()] or [fallback]


def build_spec(answers: dict[str, str], target: str) -> dict:
    name = answers["name"]
    actor_words = _words(answers["users"], "owner")
    entity_words = _words(answers["things"], "item")
    action_words = _words(answers["actions"], "manage")
    entities = [{"id": _slug(item).replace("-", "_"), "fields": ["name", "status"]} for item in entity_words]
    journeys = [{"id": _slug(action).replace("-", "_"), "actor": actor_words[0], "steps": [action, "validar", "registrar auditoria"]} for action in action_words]
    risk = "high" if any(word in answers["risk"].lower() for word in ("dinheiro", "pagamento", "saúde", "medico", "crítico", "critico", "segurança", "seguranca")) else "medium"
    controls = ["permissão explícita", "auditoria de ações"]
    if risk == "high":
        controls.append("revisão humana antes de concluir")
    return {"id": _slug(name), "name": name, "purpose": answers["problem"], "target": target, "risk": risk, "actors": actor_words, "entities": entities, "journeys": journeys, "controls": controls}


def conduct(name: str | None = None, target: str = "local", owner: str = "Gustavo", input_fn: Callable[[str], str] = input, output_fn: Callable[[str], None] = print, root: str | Path = ".", provider: str = "auto") -> dict:
    output_fn("\nFORJA — vamos criar seu sistema conversando. Você pode responder do seu jeito.\n")
    output_fn(explain_provider(provider))
    answers = {}
    answers["name"] = name or input_fn("1/6. Como você quer chamar o sistema? ")
    answers["problem"] = input_fn("2/6. Que problema ele resolve? Explique com suas palavras: ")
    answers["users"] = input_fn("3/6. Quem vai usar? Pessoas, cargos ou equipes: ")
    answers["things"] = input_fn("4/6. O que essas pessoas precisam guardar ou acompanhar? ")
    answers["actions"] = input_fn("5/6. O que elas precisam fazer no sistema? ")
    answers["risk"] = input_fn("6/6. Há dinheiro, saúde, segurança ou outra parte importante? Se não, diga não: ")
    spec = build_spec(answers, target)
    output_fn("\nEntendi assim:")
    output_fn(f"Sistema: {spec['name']}")
    output_fn(f"Problema: {spec['purpose']}")
    output_fn(f"Usuários: {', '.join(spec['actors'])}")
    output_fn(f"Itens: {', '.join(e['id'] for e in spec['entities'])}")
    output_fn(f"Ações: {', '.join(j['id'] for j in spec['journeys'])}")
    confirmation = input_fn("Está certo? Digite sim para criar ou não para cancelar: ").strip().lower()
    if confirmation not in {"sim", "s", "yes", "y"}:
        output_fn("Tudo bem. Nada foi criado.")
        return {"ok": False, "cancelled": True, "spec": spec}
    base = Path(root).resolve() / _slug(spec["name"])
    init_workspace(base, spec["name"], owner)
    spec_path = base / "requirements.json"
    spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    blueprint = write_blueprint(spec_path, base / "blueprint")
    (base / "CONVERSA.md").write_text("# Decisões da conversa\n\n" + "\n".join(f"- **{key}:** {value}" for key, value in answers.items()) + "\n", encoding="utf-8")
    output_fn(f"\nPronto. Criei {base}")
    output_fn(f"Agora você pode abrir {spec_path} e continuar conversando com a FORJA.")
    return {"ok": True, "project": str(base), "requirements": str(spec_path), "blueprint": str(blueprint), "provider": choose_provider(provider)["id"]}
