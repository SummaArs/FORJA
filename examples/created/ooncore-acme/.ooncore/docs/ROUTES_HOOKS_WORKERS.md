# Rotas, hooks, triggers e execução de processos

Para assinatura de `defineRoutes`, opções de `router.private`, bootstrap, prefixos, permissões, erros e `sensitiveBody`, use [PUBLIC_CONTRACTS.md](PUBLIC_CONTRACTS.md).

## Existente e público

- `defineValidation(model, fn)`: valida estado consolidado antes de persistir.
- `defineTrigger(model, { before, after })`: registra efeitos de domínio associados à mutação. Não trate hooks como entrega exatamente uma vez de efeitos externos.
- `central.process.json`: transições, bindings, invariantes e recálculos suportados. [Contrato completo](BACKEND_PROCESS_MANIFEST.md).
- `capabilities.transactionalEmail`: envio e acompanhamento de e-mail, com fila própria. [Contrato completo](TRANSACTIONAL_EMAIL.md).

## Interno e específico

Jobs de recálculo do processo e workers de e-mail atendem esses recursos; não são uma fila genérica durável para integração externa. `drainProcessJobs` não define enqueue/claim/retry de tarefas arbitrárias. Stores, transports e registries internos não são pontos de extensão de Apps.

## Integração no App e proposta futura

Não há API pública genérica de “integration runtime” para outbox/inbox, locks, retry ou webhooks nesta release. Chamadas externas, mapeamentos, regras fiscais, estado de operação e recuperação de negócio ficam no App por rotas/serviços documentados. [Exemplo de consulta](TASK_EXAMPLES.md#integração).

Quando a jornada precisar de execução assíncrona durável, explicite persistência, idempotência, concorrência, retry limitado, diagnóstico sanitizado e lifecycle no App, ou acompanhe uma nova Capacidade em escopo separado. Não invente APIs do Core, não transforme um timer em garantia de durabilidade e não bloqueie funções independentes à espera da nova Capacidade.

O runtime local não fornece identidade operacional da Plataforma. Operações que a exigem continuam falhando fechado conforme [LOCAL_SECURITY_BOUNDARY.md](LOCAL_SECURITY_BOUNDARY.md).
