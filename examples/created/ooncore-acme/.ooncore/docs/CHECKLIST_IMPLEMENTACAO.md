# Checklist de Implementação

Referência sob demanda: aplique somente os itens relevantes à jornada alterada. Não é um gate para começar uma POC nem exige homologar novamente a Plataforma.

## Contexto e documentação

- [ ] Rodei `npm run ooncore:docs:check`.
- [ ] Rodei `npm run ooncore:docs` se havia documentação desatualizada.
- [ ] Li `.ooncore/AGENTS.md` e o guia de autoria.
- [ ] Consultei o catálogo e o contrato dedicado de cada capability usada.
- [ ] Trabalhei somente com a árvore do App e `.ooncore/`, sem fonte privada, `node_modules` ou outros Apps.
- [ ] Registrei qualquer lacuna em vez de inventar API ou infraestrutura.
- [ ] Entendi qual recurso do Core já resolve parte da necessidade.

## Backend

- [ ] Usei model, validation, trigger, hook ou mapping quando aplicável.
- [ ] Evitei recriar CRUD.
- [ ] Validei entrada.
- [ ] Validei permissão no backend.
- [ ] Propaguei tenant, correlação, cancelamento e idempotência quando aplicáveis.
- [ ] Tratei erros pelo contrato público.
- [ ] Não hardcodei segredos, endpoints internos ou implementations.
- [ ] Mantive rastreabilidade sem registrar conteúdo sensível.

## Frontend

- [ ] Defini o App com `defineOonApp` e `startOonApp`.
- [ ] Reutilizei shell, guards, primitives e padrões públicos do Core.
- [ ] Mantive rotas, navegação, páginas, layouts e temas no código do App.
- [ ] Usei `useOonApi` para chamadas autenticadas e respostas binárias.
- [ ] Não coloquei regra crítica apenas no frontend.

## Integrações e capabilities

- [ ] Fiz a declaração no manifesto indicado pelo guia.
- [ ] Usei serviço do App ou capability com contrato público publicado; não assumi uma fila genérica do Core.
- [ ] Modelei mapping e status operacional quando necessário.
- [ ] Normalizei erros externos e respeitei `retryable`.
- [ ] O runtime local falha fechado ou usa dublê somente no teste.
- [ ] Não expus credenciais.

## Entrega

- [ ] `npm run check` passou (inclui docs check e conformance).
- [ ] Build e testes relevantes declarados pelo App passaram.
- [ ] Provei o fluxo específico do usuário.
- [ ] A Central continua atualizável com novas versões do Core.
- [ ] A alteração é pequena, coesa e aderente à arquitetura.
- [ ] O comportamento específico do App está documentado sem duplicar contrato do Core.
