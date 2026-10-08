# Criação de software na FORJA

Adaptado do manual vivo fornecido por Gustavo.

## Antes de codar

- atacar primeiro a metade desconhecida;
- pedir as decisões e credenciais necessárias de uma vez;
- ler contratos oficiais;
- comparar com o template do framework;
- testar um caso real cedo;
- fazer a conta antes e medir depois;
- não gerar trabalho que não pode ser provado.

## Durante a construção

- idempotência no centro;
- dinheiro em centavos;
- retry separa ruído de erro de negócio;
- webhook é pista, reconciliação é verdade;
- retrato vencido não manda;
- nada desiste em silêncio;
- o sistema deve explicar o que sabe;
- segredo nunca vai para o repositório.

## Durante a prova

- processo separado;
- queda forçada;
- dublê adversarial;
- bug plantado;
- conjunto de teste não pode estar vazio;
- prova precisa acionar o caminho que pretende cobrir;
- reconferência na fonte;
- resultado negativo é evidência, não fracasso inútil.

## Publicação

- portão 0 cedo;
- script sem perguntas interativas;
- log legível;
- rollback conhecido;
- ambiente local reproduzível;
- `git diff --check` antes do commit;
- CI gratuito executa as mesmas provas.
