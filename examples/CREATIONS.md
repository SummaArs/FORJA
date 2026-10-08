# Criações reais da FORJA

Este diretório é uma prova executável: os três projetos abaixo foram criados pela própria CLI da FORJA em 08/10/2026.

## Comandos usados

Na raiz do repositório:

```bash
PYTHONPATH=. python3 -m forja_core create local examples/created/local-acme \
  --name "Acme Local" --owner Gustavo --apply

PYTHONPATH=. python3 -m forja_core create odoo examples/created/odoo-acme \
  --name "Acme Operação" --apply

PYTHONPATH=. python3 -m forja_core create ooncore examples/created/ooncore-acme \
  --name "Acme Central" --ooncore-version 0.7.8 --apply
```

## Resultado

| Destino | Resultado criado | Verificações |
|---|---|---|
| Local | workspace `forja/` | `project.json` e `manifest.json` válidos |
| Odoo Community | addon `odoo-acme` | manifest, Python, XML e CSV válidos |
| OonCore | Central code-first | schema v2, `.ooncore/`, backend, frontend e deploy manifest |

## Teste automatizado

O teste está em `tests/test_created_examples.py` e verifica:

- o estado inicial do workspace local;
- o `central.app.json` com schema v2;
- a compatibilidade mínima declarada do OonCore;
- a existência do contrato `.ooncore/AGENTS.md`;
- a sintaxe do manifest e dos modelos Odoo;
- a estrutura XML das views;
- a estrutura e permissões do CSV de acesso.

Execute:

```bash
./prove.sh
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## Limites da prova

Esta prova valida a **criação estrutural**. Ela não afirma que:

- o Odoo foi instalado em um servidor;
- o banco MongoDB do OonCore foi configurado;
- credenciais foram fornecidas;
- o projeto foi publicado em produção;
- regras específicas de um cliente foram homologadas.

Essas etapas exigem um ambiente-alvo e permanecem separadas da geração segura do scaffold.
