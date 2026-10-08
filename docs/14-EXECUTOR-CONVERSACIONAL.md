# Executor conversacional da FORJA

A FORJA agora fecha o ciclo entre conversa e software executável.

## Uso

```bash
PYTHONPATH=. python3 -m forja_core blueprint examples/enterprise-spec-receivables.json /tmp/receivables
```

O comando acima mostra um plano e não escreve nada. Para materializar:

```bash
PYTHONPATH=. python3 -m forja_core build examples/enterprise-spec-receivables.json /tmp/receivables --apply
```

A execução gera:

- `frontend/index.html`: frontend responsivo com design system inicial;
- `backend/app.py`: backend local de health check e catálogo;
- `forja/blueprint.json`: contrato compilado;
- `tests/test_smoke.py`: prova mínima executável;
- `run.sh`: comando local do backend;
- `README.md`: instruções e limites.

## Autoridade

A FORJA não escreve por padrão. O plano é somente leitura até o usuário informar `--apply`. A execução não usa rede, não instala dependências e roda compilação e testes automaticamente.

## O que isso prova

Prova que a FORJA consegue transformar uma especificação empresarial válida em um artefato frontend/backend executável e testado localmente.

## O que ainda não prova

Não prova produção, segurança de autenticação, escala, homologação do cliente, banco persistente ou equivalência ao Claude Code. Esses itens permanecem explicitamente pendentes.
