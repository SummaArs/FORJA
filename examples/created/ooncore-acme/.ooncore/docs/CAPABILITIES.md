# Catálogo de capacidades do OonCore

Comece pela tarefa em [TASK_INDEX.md](TASK_INDEX.md), com API pública, piso de versão, exemplo e limite. Este catálogo é referência adicional sob demanda; consulte somente os guias das capabilities usadas.

| Capacidade | Backend | Frontend | Declaração/extensão | Local | Plataforma |
|---|---|---|---|---|---|
| Models e CRUD | `defineModel`, domain manifest, `/core/*` | `CoreCollection`, hooks de API | `central.domain.json` ou composição code-first | Sim | Sim |
| Metadata | registry e `/core/metadata` | `useCoreMetadata`, renderers | models/domain manifest | Sim | Sim |
| Validações e fórmulas | `defineValidation`, domain rules | prévia reativa | domain manifest/validation | Sim | Sim |
| Esteiras | process manifest/runtime | `CorePipeline` | `central.process.json`, UI code-first | Sim | Sim |
| Documentos | `defineDocument` | `CoreDocument` | UI/domain manifest | Sim | Sim |
| Dashboards | agregações e rotas | `CoreDashboard` | UI code-first | Sim | Sim |
| RBAC | policy, middleware e `requirePermission` | `PermissionGate`, `can` | `central.app.json` | Simulação declarada | Identidade real |
| Tenant e escopo | access context e scope helpers | `TenantProvider` | `central.app.json` | Contexto técnico | Contexto autorizado |
| Auditoria | CRUD e request context | headers do SDK | automática/extensão | Local | Operacional |
| Rotas customizadas | `defineRoutes` | página/ação declarada | `backend/src/routes` | Sim | Sim |
| Recálculos de processo | manifesto de processo; execução específica | projeção do estado | `central.process.json` | Sim | Sim |
| E-mail transacional | `capabilities.transactionalEmail` | `CoreTransactionalEmail` | [TRANSACTIONAL_EMAIL.md](TRANSACTIONAL_EMAIL.md) | Fail-closed/dublê de teste | Implementação resolvida pelo Core |
| Segredos V1 | `capabilities.secrets` | Formulário do App | [SECRETS.md](SECRETS.md) | Chave local explícita | Chave por runtime dedicado/ambiente |
| PDF | `capabilities.pdf.render` | `useOonApi`/download | [PDF_RENDERING.md](PDF_RENDERING.md) | Fail-closed/dublê de teste | Implementação resolvida pelo runtime |
| Publicação/promoção | serviço homologado da Plataforma | Workspace existente | consumir fluxo existente; não reimplementar | Não | Sim |
| Runtime local | sessão e guardas locais | bootstrap/cookie/banner | `OON_RUNTIME_MODE=local` | Sim | Não aplicável |

Para cada capacidade, use o manifesto quando houver contrato declarativo e código da Central apenas nos pontos de extensão documentados. Se uma capability não possuir guia dedicado suficiente, registre uma lacuna; não descubra o contrato lendo fonte privada ou outro repositório.


Não há contrato público genérico de integration runtime. Workers de e-mail e jobs de recálculo são específicos; execução durável genérica e diagnóstico de integrações são propostas separadas. Consulte [ROUTES_HOOKS_WORKERS.md](ROUTES_HOOKS_WORKERS.md).

## Aplicação dos recursos nativos

A página `/recursos` do exemplo demonstra fórmulas, validações, bindings, invariantes, documentos, dashboard e PDF. O serviço de e-mail é opt-in. Consulte [NATIVE_RESOURCES.md](NATIVE_RESOURCES.md) para o roteiro, helpers de escopo e limites reais de isolamento, auditoria e execução.
