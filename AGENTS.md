# FORJA — instruções para agentes

Leia `README.md` e `docs/01-METODO-FORJA.md` antes de editar.

## Regras

1. não afirmar sucesso sem executar `./prove.sh`;
2. não adicionar dependência paga;
3. não usar credenciais ou dados reais;
4. não modificar testes para esconder uma falha;
5. toda regra material precisa de um teste adversarial;
6. preservar a lista `not_proven`;
7. executar `git diff --check` antes de concluir;
8. fazer commits pequenos e explicáveis.

## Modo recomendado

Primeiro analise. Depois proponha plano. Só então edite. Ao terminar, mostre arquivos alterados, prova executada, resultado e limitações.
