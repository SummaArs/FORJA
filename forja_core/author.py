from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

from .blueprint import write_blueprint
from .conversation import build_spec
from .workspace import init_workspace


def _slug(value: str) -> str:
    value = value.lower()
    value = (value.replace("ã", "a").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ç", "c"))
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "meu-projeto"


def create_author_kit(answers: dict[str, str], root: str | Path = ".", owner: str = "Gustavo") -> dict[str, str]:
    spec = build_spec({"name": answers["name"], "problem": answers["problem"], "users": answers["users"], "things": answers["things"], "actions": answers["first_feature"], "risk": answers["risk"]}, answers.get("target", "local"))
    base = Path(root).resolve() / _slug(spec["name"])
    init_workspace(base, spec["name"], owner)
    requirements = base / "requirements.json"
    requirements.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_blueprint(requirements, base / "blueprint")
    (base / "docs").mkdir(exist_ok=True)
    (base / "docs" / "01-VISAO.md").write_text(f"# Visão\n\n## Problema\n{answers['problem']}\n\n## Usuários\n{answers['users']}\n\n## Limites\n{answers['risk']}\n", encoding="utf-8")
    (base / "NEXT_STEP.md").write_text(f"# Próximo passo\n\nImplemente somente: **{answers['first_feature']}**\n\n## Faça agora\n1. Crie um teste que descreva o comportamento esperado.\n2. Execute o teste e observe a falha.\n3. Escreva o menor código para fazê-lo passar.\n4. Rode a prova novamente.\n5. Explique o que aprendeu antes de escolher o próximo passo.\n\nA FORJA não escreveu o produto por você. Ela organizou o terreno para você aprender e construir.\n", encoding="utf-8")
    (base / "BUILD_LOG.md").write_text("# Diário de construção\n\nRegistre aqui decisões, testes, erros e aprendizados.\n\n- [ ] Entender o primeiro requisito\n- [ ] Escrever o primeiro teste\n- [ ] Implementar o menor comportamento\n- [ ] Rodar a prova\n- [ ] Fazer revisão humana\n", encoding="utf-8")
    return {"project": str(base), "requirements": str(requirements), "next_step": str(base / "NEXT_STEP.md")}


def conduct_author(input_fn: Callable[[str], str] = input, output_fn: Callable[[str], None] = print, root: str | Path = ".", owner: str = "Gustavo", target: str = "local") -> dict:
    output_fn("\nFORJA — modo Autor. Você constrói; a FORJA ensina, organiza e verifica.\n")
    answers = {
        "name": input_fn("Como se chama o software? "),
        "problem": input_fn("Que problema real ele resolve? "),
        "users": input_fn("Quem vai usar? "),
        "things": input_fn("O que precisa existir ou ser acompanhado? "),
        "first_feature": input_fn("Qual é a PRIMEIRA coisa pequena que você quer fazer funcionar? "),
        "risk": input_fn("Há dinheiro, saúde, segurança ou dados sensíveis? "),
        "target": target,
    }
    output_fn(f"\nPrimeiro passo escolhido: {answers['first_feature']}")
    if input_fn("Quer criar o kit de estudo agora? (sim/não) ").strip().lower() not in {"sim", "s", "yes", "y"}:
        output_fn("Nada foi criado.")
        return {"ok": False, "cancelled": True}
    result = create_author_kit(answers, root, owner)
    output_fn(f"Kit criado em {result['project']}")
    output_fn(f"Leia primeiro: {result['next_step']}")
    return {"ok": True, **result}
