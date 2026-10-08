# Tutorial do zero

Este tutorial cria um software empresarial pequeno usando apenas o terminal e ferramentas gratuitas.

## 1. Instale o básico

Você precisa de Python 3.11 ou superior e Git. Não precisa de cartão, banco externo, API paga ou conta de nuvem.

```bash
git clone https://github.com/SummaArs/FORJA.git
cd FORJA
```

## 2. Leia antes de mexer

Leia `README.md`, depois `docs/01-METODO-FORJA.md`. Em um projeto real, também leia o contrato da API, o template oficial da plataforma e as decisões do cliente.

## 3. Execute o portão antes de alterar

```bash
./prove.sh
```

Se já falhar, não atribua a falha à sua mudança. Registre o estado inicial.

## 4. Entenda o fluxo

O Forja Ledger recebe um `Entry`. A chave identifica a intenção, o valor é inteiro em centavos e o registro é gravado junto com sua auditoria numa transação SQLite.

A mesma entrada repetida retorna `replayed`. A mesma chave com conteúdo diferente é rejeitada. Isso evita que um retry transforme uma operação em duas.

## 5. Faça uma alteração pequena

Exemplo: adicionar um campo `cost_center`. Antes de codar, escreva:

- qual afirmação muda;
- qual invariante protege o campo;
- qual entrada inválida deve ser recusada;
- como a reconciliação verá o campo;
- qual teste falharia sem a implementação.

## 6. Peça ajuda a uma IA gratuita

Use este prompt no Gemini CLI, Aider ou OpenCode:

```text
Leia README.md, AGENTS.md e docs/01-METODO-FORJA.md.
Não edite ainda. Explique a arquitetura, riscos, invariantes e testes afetados.
Proponha um plano mínimo para adicionar cost_center sem quebrar idempotência,
auditoria ou reconciliação. Diga também o que não pode ser afirmado.
```

Depois da sua revisão:

```text
Implemente somente o plano aprovado. Adicione testes adversariais.
Execute ./prove.sh. Não declare sucesso se o comando falhar.
```

## 7. Ataque a mudança

Sempre teste pelo menos:

- duplicidade;
- payload diferente com a mesma chave;
- queda antes do commit;
- queda depois do commit;
- campo ausente;
- valor negativo;
- divergência na origem.

## 8. Revise e publique

```bash
git diff --check
git status
git add .
git commit -m "feat: add cost center to ledger"
git push origin minha-branch
```

Abra uma Pull Request. O CI deve executar a mesma prova que você executou localmente.

## 9. O que muda ao virar software empresarial

O exemplo é local e educacional. Antes de dados de cliente, acrescente autenticação, autorização, backup testado, migração reversível, logs sem segredos, monitoramento, política de retenção, testes de carga, homologação e aceitação do dono do processo.
