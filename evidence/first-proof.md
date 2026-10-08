# Primeira prova

Este arquivo é atualizado somente depois de executar `./prove.sh`.

## Escopo

A prova cobre o Forja Ledger local, SQLite, Python 3 e a biblioteca padrão. Ela não cobre autenticação, hospedagem, escala de produção, ERP real ou aceitação de cliente.

## Evidência

A primeira execução falhou antes dos testes por uma omissão na API pública: `Entry`
era usado pelo consumidor, mas não era exportado em `forja_ledger.__init__`. O defeito
foi corrigido antes da segunda execução. Esta falha foi preservada como evidência de
que o portão foi executado de verdade.

Na segunda execução, os 10 testes adversariais e a demonstração local passaram:

```text
FORJA PROOF: PASS
checks=12 violations=0
```
