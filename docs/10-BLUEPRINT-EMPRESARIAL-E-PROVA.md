# Blueprint empresarial e prova da FORJA

## O que mudou

A FORJA deixa de ser apenas um gerador de scaffolds. Ela agora compila uma especificação empresarial em contratos verificáveis para:

- frontend: rotas e fronteiras de componentes;
- backend: modelos e exigência de validação/autorização;
- governança: atores, permissões deny-by-default e eventos de auditoria;
- aceitação: jornadas e checks obrigatórios;
- risco: controles explícitos para sistemas de alto risco.

Isso não é uma alegação de SOTA universal. É uma implementação **SOTA-oriented** de engenharia empresarial: especificação antes do código, separação de camadas, gates fail-closed, reprodutibilidade e limites explícitos.

## Uso

Verifique o plano sem escrever:

```bash
PYTHONPATH=. python3 -m forja_core blueprint \
  examples/enterprise-spec-receivables.json \
  examples/generated/receivables
```

Materialize:

```bash
PYTHONPATH=. python3 -m forja_core blueprint \
  examples/enterprise-spec-receivables.json \
  examples/generated/receivables --apply
```

## Saída

```text
blueprint.json
frontend.routes.json
backend.domain.json
governance.json
acceptance.json
```

## Prova adversarial

A suíte bloqueia:

- sistema de alto risco sem dois controles explícitos;
- jornada com ator não declarado;
- entidades duplicadas;
- ausência de entidades ou jornadas;
- campos obrigatórios ausentes;
- blueprint não reproduzível ou incompleto.

## Limite científico

A FORJA pode provar que a especificação foi compilada de forma determinística e que os contratos mínimos existem. Isso não prova, por si só, que o produto é correto para qualquer cliente, que a UX é boa, que o Odoo está homologado ou que a Central OonCore está pronta para produção. Essas afirmações exigem testes de domínio, ambiente-alvo, segurança, performance e aceitação real.
