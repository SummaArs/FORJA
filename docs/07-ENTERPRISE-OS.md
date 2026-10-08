# FORJA Enterprise OS

## A mudança de perspectiva

A primeira FORJA era um método de criar software. A versão seguinte governa qualquer coisa que uma empresa possa criar, operar ou decidir.

Um **artefato empresarial** é qualquer objeto que possa sustentar uma decisão:

| Tipo | Exemplos |
|---|---|
| software | sistema, API, automação |
| processo | cobrança, fechamento, atendimento |
| produto | diagnóstico, serviço, pacote comercial |
| documento | contrato, manual, relatório |
| política | aprovação, segurança, crédito |
| operação | migração, plantão, implantação |
| análise | estudo, benchmark, previsão |
| experimento | hipótese, piloto, spike |
| decisão | escolha de fornecedor ou arquitetura |

Todos usam o mesmo contrato: propósito, dono, risco, estado, afirmações, evidências, limites e gatilhos de reabertura.

## O que a FORJA passa a produzir

A FORJA pode gerar um **pacote empresarial verificável**:

1. definição do problema;
2. mapa de decisões;
3. artefato executável ou operacional;
4. matriz de riscos;
5. evidências;
6. instruções de uso;
7. plano de operação;
8. registro do que não foi provado;
9. gatilhos de reabertura;
10. decisão de promoção ou abandono.

Assim, a mesma lógica serve para criar um software, lançar um produto, desenhar um processo financeiro, elaborar uma política interna, executar uma migração, produzir um relatório ou conduzir um experimento.

## Uso

```bash
PYTHONPATH=. python3 -m forja_core check examples/enterprise-portfolio.json
```

Se um artefato validado não tiver evidência, ou se um artefato de alto risco não tiver gatilho de reabertura, o comando falha. A FORJA não deixa um documento bonito mascarar uma decisão sem base.

## Limite honesto

A FORJA organiza e prova o trabalho; ela não substitui conhecimento de domínio, responsabilidade legal, aprovação do cliente, auditoria independente ou decisão humana. O objetivo é tornar essas responsabilidades explícitas e mais fáceis de executar.
