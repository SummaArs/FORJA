# Protocolo empresarial FORJA

## Definição de pronto mínima

Antes de escrever código, congele uma lista numerada. Para o exemplo:

1. aceitar um lançamento válido;
2. rejeitar valor negativo;
3. rejeitar moeda desconhecida;
4. repetir a chave sem duplicar;
5. preservar o primeiro payload;
6. registrar auditoria;
7. sobreviver a uma queda simulada antes do commit;
8. sobreviver a uma queda simulada depois do commit;
9. reconciliar origem e destino;
10. produzir uma prova reproduzível;
11. informar o que não foi provado.

## Contrato de erro

Erro de negócio não deve ser escondido por retry. Entrada inválida volta para o operador com motivo. Falha técnica pode ser repetida apenas quando a operação é idempotente.

## Fonte da verdade

O banco local é o destino da demonstração. A origem dos eventos fica registrada com sua chave e payload. Reconciliação compara os dois lados; contar apenas respostas HTTP não é suficiente.

## Extensão para produtos reais

Para usar a FORJA em Neotass, Vinde, SwitchPay ou The Eye, adicione:

- autenticação;
- autorização por papel;
- segredo em cofre;
- backup e restauração;
- observabilidade;
- rate limits do fornecedor;
- homologação com dados do cliente;
- aceitação humana;
- política de suporte;
- plano de reversão.
