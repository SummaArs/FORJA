# HOROCUM dentro da FORJA

Este documento é a adaptação do protocolo HOROCUM fornecido por Gustavo.

## Princípios preservados

- funcionamento técnico não prova significado de negócio;
- afirmações materiais precisam de evidência correspondente;
- evidência tem escopo e gatilho de invalidação;
- a lista de pronto é congelada antes da construção;
- o portão de entrega deve ser testado cedo;
- a aceitação final pertence ao dono do processo;
- frameworks e templates oficiais devem ser comparados antes de deduções;
- nenhuma decisão relevante esconde premissa, risco ou evidência.

## Estados de confiança

`hipótese → experimento → decisão provisória → implementada → validada → monitorada → reaberta`

## Portões

| Portão | Pergunta |
|---|---|
| 0 | o software chega a um ambiente executável? |
| 1 | o modelo guarda o necessário? |
| 2 | a conexão é real e segura? |
| 3 | a sincronização preserva todos os dados? |
| 4 | a regra significa o que o negócio afirma? |
| 5 | o operador consegue usar? |
| 6 | uma falha é visível e reversível? |
| 7 | o cliente aceitou em um ciclo real? |

O exemplo local desta FORJA fecha apenas os portões que consegue provar localmente. Portões reais permanecem abertos até haver evidência real.
