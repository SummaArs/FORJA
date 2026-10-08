# FORJA

## Construir software empresarial confiável com lógica, provas e custo zero

A **FORJA** é um método prático para criar software empresarial melhor, mais confiável e mais econômico usando apenas ferramentas gratuitas ou open source.

Ela transforma uma ideia em um sistema que pode responder, com evidência:

- o que o software afirma;
- o que pode dar errado;
- como a falha é detectada;
- como o sistema evita duplicidade;
- como ele recupera depois de cair;
- como outra pessoa reproduz a prova;
- o que ainda **não** foi verificado.

> **A FORJA não promete que toda IA gratuita substitui um engenheiro. Ela cria um processo que impede que a IA esconda incerteza.**

## O exemplo incluído

Este repositório constrói do zero o **Forja Ledger**, uma pequena central de lançamentos empresariais:

```text
evento de origem → validação → gravação idempotente → auditoria → reconciliação
```

Ele não usa API paga, banco pago, framework pago ou dependência externa. Usa somente:

- Python 3.11+;
- SQLite incluído no Python;
- biblioteca padrão;
- Git e GitHub;
- qualquer agente gratuito opcional.

O exemplo demonstra:

- valores em centavos inteiros;
- chave idempotente por intenção;
- transação atômica;
- trilha de auditoria;
- falha fechada para dados inválidos;
- reconciliação contra a fonte de origem;
- testes adversariais;
- simulação de queda antes e depois do commit.

## Comece em três comandos

```bash
python3 -m unittest discover -s tests -v
./prove.sh
python3 -m forja_ledger demo
```

## Resultado esperado

```text
FORJA PROOF: PASS
checks=12 violations=0
```

## Os cinco passos da FORJA

1. **Definir** — escrever o problema, as afirmações materiais e a definição de pronto.
2. **Modelar** — transformar a operação em estados, invariantes e contratos.
3. **Forjar** — implementar o menor sistema que pode ser provado.
4. **Atacar** — plantar defeitos, simular queda, duplicidade, atraso e dados inválidos.
5. **Reconferir** — comparar o resultado com a fonte da verdade, publicar limites e só então evoluir.

## Documentação

- [Método FORJA](docs/01-METODO-FORJA.md)
- [Tutorial do zero](docs/02-TUTORIAL-DO-ZERO.md)
- [HOROCUM incorporado](docs/03-HOROCUM.md)
- [Criação de software incorporada](docs/04-CRIACAO-DE-SOFTWARE.md)
- [Stack 100% gratuita](docs/05-STACK-GRATUITA.md)
- [Protocolo empresarial](docs/06-PROTOCOLO-EMPRESARIAL.md)
- [Relatório da prova](evidence/first-proof.md)

## Status honesto

**MVP educacional validado localmente.** Ele não é ainda um ERP, não foi homologado em ambiente de cliente e não deve receber dados reais sem revisão, backup, autenticação e implantação apropriada.

A FORJA mede progresso por evidência, não por quantidade de arquivos:

- Definição: 100%
- Exemplo executável: 100%
- Prova local: será registrada após execução
- Produção empresarial: 0% até homologação real

## Licença

MIT para o código e a documentação deste repositório, exceto quando uma fonte externa for explicitamente indicada.
