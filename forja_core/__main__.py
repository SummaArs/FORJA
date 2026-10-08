from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manifest import validate_manifest
from .workspace import connect_repository, init_workspace


def main() -> None:
    parser = argparse.ArgumentParser(description="FORJA — crie qualquer artefato empresarial com evidência")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="verifica um manifesto empresarial")
    check.add_argument("manifest", type=Path)

    init = sub.add_parser("init", help="prepara um projeto novo de forma guiada")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--name", default="novo-projeto")
    init.add_argument("--owner", default="meu-nome")

    connect = sub.add_parser("connect", help="conecta um repositório em modo somente leitura")
    connect.add_argument("--workspace", default=".")
    connect.add_argument("--repo", required=True, help="caminho local ou URL do repositório")
    connect.add_argument("--name", default="ooncore")

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
    elif args.command == "connect":
        record = connect_repository(args.workspace, args.repo, args.name)
        print(json.dumps(record, indent=2, ensure_ascii=False))
        print("Conexão registrada em modo somente leitura; nenhum arquivo do repositório foi alterado.")


if __name__ == "__main__":
    main()
