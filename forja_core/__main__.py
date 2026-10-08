from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manifest import validate_manifest
from .workspace import connect_repository, init_workspace
from .adapters import create_local, create_ooncore, create_odoo, plan
from .blueprint import BlueprintError, compile_blueprint, write_blueprint
from .quickstart import create_quickstart
from .conversation import conduct


def main() -> None:
    parser = argparse.ArgumentParser(description="FORJA — crie qualquer artefato empresarial com evidência")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="verifica um manifesto empresarial")
    check.add_argument("manifest", type=Path)

    init = sub.add_parser("init", help="prepara um projeto novo de forma guiada")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--name", default="novo-projeto")
    init.add_argument("--owner", default="meu-nome")

    new = sub.add_parser("new", help="comece um sistema com uma frase simples")
    new.add_argument("name", help="nome do sistema, por exemplo: Minha Loja")
    new.add_argument("--root", default=".")
    new.add_argument("--target", choices=["local", "ooncore", "odoo"], default="local")
    new.add_argument("--owner", default="Gustavo")

    talk = sub.add_parser("conversar", aliases=["chat", "talk"], help="crie um sistema respondendo perguntas naturais")
    talk.add_argument("--name", default=None, help="opcional; se faltar, a FORJA pergunta")
    talk.add_argument("--root", default=".")
    talk.add_argument("--target", choices=["local", "ooncore", "odoo"], default="local")
    talk.add_argument("--owner", default="Gustavo")
    talk.add_argument("--provider", choices=["auto", "ollama", "gemini", "aider", "opencode"], default="auto")

    connect = sub.add_parser("connect", help="conecta um repositório em modo somente leitura")
    connect.add_argument("--workspace", default=".")
    connect.add_argument("--repo", required=True, help="caminho local ou URL do repositório")
    connect.add_argument("--name", default="ooncore")

    create = sub.add_parser("create", help="cria um projeto local, OonCore ou addon Odoo")
    create.add_argument("kind", choices=["local", "ooncore", "odoo"])
    create.add_argument("target")
    create.add_argument("--name", default="novo-projeto")
    create.add_argument("--owner", default="Gustavo")
    create.add_argument("--apply", action="store_true", help="escreve arquivos; sem isso apenas mostra o plano")
    create.add_argument("--ooncore-version", default="0.7.8")

    blueprint = sub.add_parser("blueprint", help="compila requisitos em front, back, governança e aceitação")
    blueprint.add_argument("spec", type=Path)
    blueprint.add_argument("output", type=Path)
    blueprint.add_argument("--apply", action="store_true", help="escreve o blueprint compilado")

    args = parser.parse_args()
    if args.command == "check":
        result = validate_manifest(args.manifest)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result["ok"]:
            raise SystemExit(1)
        print(f"FORJA MANIFEST: PASS ({result['artifacts']} artifacts)")
    elif args.command == "init":
        location = init_workspace(args.path, args.name, args.owner)
        print(f"Projeto preparado em: {location}")
        print("Próxima pergunta: Qual problema empresarial precisa mudar?")
    elif args.command == "new":
        result = create_quickstart(args.name, args.root, args.target, args.owner)
        print(f"Pronto! Criei: {result['project']}")
        print(f"Agora abra: {result['requirements']}")
        print(f"Já deixei uma primeira planta em: {result['blueprint']}")
        print(f"Próximo passo: {result['next']}")
    elif args.command in {"conversar", "chat", "talk"}:
        result = conduct(args.name, args.target, args.owner, root=args.root, provider=args.provider)
        if not result.get("ok", False):
            raise SystemExit(1)
    elif args.command == "connect":
        record = connect_repository(args.workspace, args.repo, args.name)
        print(json.dumps(record, indent=2, ensure_ascii=False))
        print("Conexão registrada em modo somente leitura; nenhum arquivo do repositório foi alterado.")
    elif args.command == "create":
        if not args.apply:
            print(json.dumps(plan(args.kind, args.target, args.name), indent=2, ensure_ascii=False))
            print("PLANO SOMENTE LEITURA: use --apply para criar arquivos.")
            return
        if args.kind == "local":
            result = create_local(args.target, args.name, args.owner)
        elif args.kind == "ooncore":
            result = create_ooncore(args.target, args.name, args.ooncore_version, apply=True)
        else:
            result = create_odoo(args.target, args.name, apply=True)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result.get("ok", True):
            raise SystemExit(1)
    elif args.command == "blueprint":
        try:
            if not args.apply:
                spec = json.loads(args.spec.read_text(encoding="utf-8"))
                result = compile_blueprint(spec)
                print(json.dumps({"ok": True, "schema": result["schema"], "target": result["identity"]["target"], "routes": len(result["frontend"]["routes"]), "models": len(result["backend"]["models"])}, indent=2, ensure_ascii=False))
                print("PLANO SOMENTE LEITURA: use --apply para materializar o blueprint.")
            else:
                print(f"Blueprint criado em: {write_blueprint(args.spec, args.output)}")
        except (OSError, json.JSONDecodeError, BlueprintError) as exc:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
            raise SystemExit(1)


if __name__ == "__main__":
    main()
