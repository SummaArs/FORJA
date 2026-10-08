# Índice por intenção

Documentação distribuída da release **0.7.8**. Escolha a linha da tarefa; não é necessário ler todos os guias.

**Versão mínima:** 0.7.4 é o piso verificado dos exemplos deste roteiro, não uma alegação de que cada API surgiu nessa versão. PDF e e-mail têm contrato dedicado desde 0.6.0. Use versões coordenadas dos três pacotes e não presuma compatibilidade com versões anteriores ao piso indicado.

| Quero… | API/export público | Mínima do roteiro | Exemplo executável / referência completa | Limite principal |
|---|---|---|---|---|
| Cadastrar e listar | back: `defineModel`, `fields`; front: `CoreCollection` | 0.7.4 | [Cadastro e lista](TASK_EXAMPLES.md#cadastro-e-lista); [metadata/CRUD](METADATA_CRUD_UI.md), [domínio](BACKEND_DOMAIN_MANIFEST.md) | CRUD valida escopo; consultas próprias também devem usar contexto autorizado |
| Criar formulário | front: `useOonApi`, `CoreCollection` com formulário nativo | 0.7.4 | [Formulário e ação](PUBLIC_CONTRACTS.md#primeira-jornada-executável); [frontend](FRONTEND_API.md), [modal](DETAIL_MODAL_AND_RELATED_GRIDS.md) | Validação e permissão da UI não substituem backend |
| Registrar rota privada | back: `defineRoutes`, `GenericError` | 0.7.4 | [Rota privada](PUBLIC_CONTRACTS.md#rotas-privadas); [backend](BACKEND_API.md) | Opções como segundo argumento, handler como terceiro; prefixo interno sem `/api` |
| Executar ação | front: `useOonApi`; back: `defineRoutes` | 0.7.4 | [Formulário e ação](PUBLIC_CONTRACTS.md#primeira-jornada-executável); [rotas](ROUTES_HOOKS_WORKERS.md) | Valide permissão, entrada e efeitos no backend; retry de efeito externo é decisão do App |
| Modelar esteira | `central.process.json`, back: `loadProcessManifest`; front: `CorePipeline` | 0.7.4 | [Esteira mínima](TASK_EXAMPLES.md#esteira); [processo](BACKEND_PROCESS_MANIFEST.md), [UI](COLLECTIONS_AND_PIPELINES.md) | Transições/invariantes não são fila genérica de integração |
| Integrar sistema externo | back: `defineRoutes`, `GenericError`; serviço do App; Node `fetch` (não é API OonCore) | 0.7.4 | [Integração](TASK_EXAMPLES.md#integração); [contratos e segredo](PUBLIC_CONTRACTS.md) | Mapeamento, timeout, credenciais e recuperação de negócio pertencem ao App |
| Armazenar credenciais | back: `capabilities.secrets.put/status/use/remove` | 0.7.6 | [Segredos V1](SECRETS.md); `/segredos` no exemplo | Apenas single_tenant dedicado; chave separada e responsabilidade de sanitização do consumidor |
| Gerar PDF | back: `capabilities.pdf.render`; front: `useOonApi` | 0.6.0 | [Exemplo back/front e referência](PDF_RENDERING.md) | Depende de capability resolvida; limites de entrada/saída e timeout no guia |
| Enviar e-mail | back: `capabilities.transactionalEmail.send`; front: `CoreTransactionalEmail` | 0.6.0 | [Exemplo de template, envio e painel](TRANSACTIONAL_EMAIL.md) | Sem anexos; `accepted` não confirma entrega; fila exclusiva de e-mail |
| Diagnosticar | `GenericError`, HTTP `/health/ready`, `/health/version` | 0.7.4 | [Comandos](TASK_EXAMPLES.md#diagnóstico); [erros](ERRORS.md), [troubleshooting](TROUBLESHOOTING.md) | 404 HTML não é envelope de domínio; não colar segredos no diagnóstico |
| Atualizar | CLI `create-central-oon docs sync/check` | 0.7.4 | [Comandos e referência](CORE_UPGRADE.md) | Atualize três pacotes, lockfiles e cache oficial; não edite `.ooncore` à mão |

## Estado dos recursos

- **Existente e público:** exports/contratos acima, CRUD/metadata, validações/fórmulas, manifesto de processo, auditoria, PDF e e-mail. [CAPABILITIES.md](CAPABILITIES.md) detalha os limites por ambiente.
- **Interno, não consumível como contrato de integração:** stores, transports, registries internos, worker de e-mail e jobs de recálculo do processo. Mesmo funções exportadas para o processo não constituem uma API genérica de enqueue/claim/retry.
- **Proposta futura separada:** execução durável genérica de integrações, diagnóstico padronizado operação → tentativa → troca e evolução de segredos. A existência de uma issue não disponibiliza uma API; não use `core.secrets` sem contrato publicado na versão instalada.

A Plataforma homologada fornece identidade, acesso e delivery; o App não assume essa autoridade. Lacunas têm tratamento localizado conforme [AGENTS.md](AGENTS.md).


## Jornada integrada e diagnóstico

Na release 0.7.8, `create-central-oon example` instala o exemplo opt-in em uma base limpa; `create-central-oon doctor` diagnostica versões, lockfiles, manifestos, cache e erros de empacotamento. Veja [EXECUTABLE_EXAMPLE.md](EXECUTABLE_EXAMPLE.md).

## Aplicação dos recursos nativos

A página `/recursos` do exemplo demonstra fórmulas, validações, bindings, invariantes, documentos, dashboard e PDF. O serviço de e-mail é opt-in. Consulte [NATIVE_RESOURCES.md](NATIVE_RESOURCES.md) para o roteiro, helpers de escopo e limites reais de isolamento, auditoria e execução.
