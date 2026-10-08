# OonCore — Contexto consolidado para IA/Agents

> Arquivo gerado automaticamente por `create-central-oon docs sync`.
> Não edite manualmente. A fonte de verdade está no pacote `@oondemand/create-central-oon` instalado.

Compilação opcional para consulta. Comece por docs/OON_APP_AGENT_GUIDE.md e docs/TASK_INDEX.md; não é necessário ler este arquivo inteiro.

---

<!-- source: ADVANCED_UX_PATTERNS.md -->

# ADVANCED_UX_PATTERNS.md — UX Avançada Declarativa no OonCore

Este documento orienta Agents a usarem os componentes públicos do OonCore e a
composição code-first antes de recriar padrões operacionais.

## Objetivo

Permitir que uma Central declare experiências avançadas como:

```txt
Entidade principal
├── grid principal com filtros e ações
└── modal de detalhe com abas
    ├── resumo
    ├── dados principais
    ├── itens relacionados editáveis inline
    └── registros relacionados somente leitura
```

Caso de referência: `OrcamentoProjeto -> OrcamentoItem -> Pagamento`.

## Regra de ouro para IAs

Antes de criar uma página React customizada, verifique se a necessidade pode ser resolvida por:

1. Views `collection` em `defineOonApp({ ui })`.
2. `list.filters` e `list.rowActions`.
3. `detailModal.tabs`.
4. `form.groups`.
5. `relatedGrid`.
6. `rowActions` declarativas.
7. Um pequeno `customComponent` isolado.

Código customizado de página inteira deve ser a última opção.

## Padrão 1 — Tela principal limpa

A tela principal de uma coleção operacional deve conter apenas:

- título e descrição;
- filtros;
- busca;
- botão novo;
- grid principal;
- ações por linha.

Ela **não deve** expandir detalhes complexos abaixo do grid. Relações, edição profunda e acompanhamento devem ir para a modal de detalhe.

## Padrão 2 — Modal de detalhe com abas

Use uma modal quando o usuário precisar operar um registro com várias perspectivas.

Abas recomendadas:

- `summary`: visão rápida de indicadores e contadores.
- `form`: dados principais do registro.
- `relatedGrid`: filhos editáveis, como itens do orçamento.
- `readonlyGrid`: registros relacionados apenas para consulta, como pagamentos gerados.

## Padrão 3 — Formulários agrupados

Formulários longos devem ser divididos em grupos semânticos:

```json
{
  "type": "form",
  "groups": [
    { "label": "Identificação", "fields": ["codigo", "nome", "status"] },
    { "label": "Faturamento", "fields": ["cliente", "cnpj", "contato"] },
    { "label": "Observações", "fields": ["observacoes"] }
  ]
}
```

## Padrão 4 — Itens relacionados editáveis inline

Quando uma entidade principal tem muitos itens filhos, como itens de orçamento, serviços, parcelas, documentos ou pedidos, prefira `relatedGrid` com `editMode: "inline"`.

Comportamento esperado:

- edição célula a célula;
- indicação de linha alterada;
- botão `Salvar` por linha;
- botão `Cancelar` por linha;
- validação antes de salvar;
- loading por linha;
- erro por linha;
- atualização automática dos dados relacionados.

## Padrão 5 — Ações por linha

Ações de domínio devem ser declaradas no manifesto e executadas por HTTP.

Exemplo:

```json
{
  "id": "gerarPagamento",
  "label": "Gerar pagamento",
  "type": "apiAction",
  "method": "POST",
  "endpoint": "/api/ss-eventos/orcamentos-itens/:id/gerar-pagamento",
  "disabledWhen": { "field": "pagamentoId", "exists": true },
  "refresh": ["self", "pagamentos", "resumo"]
}
```

A regra de negócio continua na Central ou no backend. O Core apenas renderiza, valida permissões, executa a ação e atualiza a interface.

## Padrão 6 — Relações declarativas

Sempre que possível, declare relações no manifesto:

```json
{
  "relations": {
    "itens": {
      "model": "OrcamentoItem",
      "foreignKey": "projetoId",
      "parentKey": "_id"
    },
    "pagamentos": {
      "model": "Pagamento",
      "foreignKey": "projetoId",
      "parentKey": "_id"
    }
  }
}
```

Assim, qualquer aba pode referenciar `relation: "itens"` sem repetir configuração.

## Padrão 7 — Abas somente leitura

Use `readonlyGrid` para dados relacionados que não devem ser editados naquela tela.

Exemplo: pagamentos gerados a partir dos itens de um orçamento.

## Padrão 8 — Refresh entre abas

Ações em uma aba podem afetar outras abas. O manifesto deve declarar o refresh esperado:

```json
"refresh": ["self", "pagamentos", "resumo"]
```

Significado:

- `self`: recarrega o grid atual;
- `pagamentos`: recarrega a aba pagamentos;
- `resumo`: recalcula cards da aba resumo;
- `parent`: recarrega o registro principal.

## Quando ainda usar componente customizado

Use componente customizado apenas quando:

- houver visualização muito específica de negócio;
- o padrão ainda não existir no Core;
- a regra envolver interação visual não generalizável;
- o componente puder ser isolado e reaproveitado.

Mesmo nesses casos, prefira plugar o componente em uma aba `customComponent` da modal, e não substituir a página inteira.

## Checklist para Agents

Antes de criar tela customizada:

- [ ] A coleção principal pode usar `collections[]`?
- [ ] Os filtros cabem em `list.filters`?
- [ ] As ações de linha cabem em `list.rowActions`?
- [ ] O detalhe cabe em `detailModal`?
- [ ] Os campos cabem em `form.groups`?
- [ ] Os filhos cabem em `relatedGrid`?
- [ ] As ações dos filhos cabem em `rowActions`?
- [ ] A consulta relacionada cabe em `readonlyGrid`?
- [ ] O refresh entre abas está declarado?
- [ ] RBAC está no backend e refletido no manifesto?

## Antipadrões

Evite:

- recriar shell, menu, roteamento e providers;
- codificar página inteira só para mudar layout do formulário;
- chamar `fetch` direto se `useOonApi`/client do Core atende;
- duplicar regra de permissão apenas no frontend;
- hardcode de endpoints quando a metadata pode resolver;
- editar `.ooncore/` manualmente;
- criar variações visuais fora do padrão sem necessidade.

## Implementação disponível no Core

Use `collections[].list` para filtros, colunas e ações da lista principal. Use `collections[].relations` para nomear relações reutilizáveis e `collections[].detailModal.tabs` para declarar abas `summary`, `form`, `relatedGrid`, `readonlyGrid` ou `customComponent`.

Ações por linha (`rowActions`) podem abrir a modal (`openDetailModal`), navegar (`navigate`) ou chamar endpoints (`apiAction`). Condições declarativas (`exists`, `equals`, `notEquals`, `in`, `gt`, `gte`, `lt`, `lte`) controlam visibilidade e bloqueio sem hardcode de Central no Core.

---

<!-- source: AGENT_WORKFLOW.md -->

# Fluxo de trabalho para Agents

1. Gere a base oficial e execute: [OON_APP_AGENT_GUIDE.md](OON_APP_AGENT_GUIDE.md).
2. Escolha a jornada e consulte somente a intenção em [TASK_INDEX.md](TASK_INDEX.md).
3. Implemente domínio e experiência pelos contratos públicos, preservando permissões, contexto e segredos.
4. Valide com `npm run check`, build e testes relevantes disponíveis; prove a jornada.
5. Publique pelo fluxo existente e registre commit e evidência em Dev.

A documentação desta release é 0.7.8, linha 0.7.x. Para coordenar os três pacotes, consulte [CORE_UPGRADE.md](CORE_UPGRADE.md).

Se faltar assinatura, declaração, exemplo ou limite, registre a lacuna e continue partes independentes com extensões públicas documentadas no App. Apenas a operação sem contrato seguro fica pendente. Nunca use internals como API, invente contratos ou crie autoridade de autenticação/RBAC paralela.

Não exija leitura integral do contexto consolidado, planejamento completo nem homologação global da Plataforma para começar. Consulte referências detalhadas sob demanda.

---

<!-- source: AGENTS.md -->

# OonCore — entrada canônica para IA/Agents

Leia o `AGENTS.md` da raiz do App, quando existir, e siga o roteiro curto em [OON_APP_AGENT_GUIDE.md](OON_APP_AGENT_GUIDE.md). Para uma alteração existente, vá direto à intenção em [TASK_INDEX.md](TASK_INDEX.md).

- Use a documentação distribuída correspondente aos pacotes instalados. `npm run check` verifica cache e conformidade; se o cache estiver desatualizado, regenere com `npm run ooncore:docs`.
- Leia somente a referência necessária à jornada. `context.generated.md` é uma compilação opcional para consulta, não uma leitura inicial obrigatória.
- Use exports públicos; fontes internas e outros Apps não substituem contratos. Exemplos de domínio de outros Apps não são scaffold.
- Se faltar contrato, registre a lacuna com versão, tarefa e informação ausente. Use uma extensão pública documentada no próprio App quando adequada e continue as partes independentes. Suspenda apenas a operação que não pode ser implementada com segurança; não invente APIs nem importe internals.
- Preserve autenticação, autorização de backend, contexto autorizado, isolamento, auditoria e proteção de segredos. POC reduz escopo funcional, não proteção.
- Plataforma homologada: consuma identidade, acesso, tenancy, licenciamento e delivery existentes. Não repita sua implementação/homologação global no App. Nova Capacidade exige escopo separado e explícito.
- Entregue uma jornada utilizável com página, navegação, endpoint e permissão. Admin pode validar a POC controlada; uma matriz final de perfis, roadmap completo e novas Capacidades não são pré-requisitos.
- Antes do PR: `npm run check`, build do frontend e testes relevantes existentes. Relate separadamente implementação, build, publicação e homologação da jornada.

O `AGENTS.md` da raiz pertence ao App; o gerador e o sync não o sobrescrevem. Consulte [CORE_UPGRADE.md](CORE_UPGRADE.md) para migração e [releases/0.7.0.md](releases/0.7.0.md) para o histórico desta linha.

---

<!-- source: APP_PACKAGING.md -->

# Empacotamento e validação da imagem do Oon-App

O contrato abaixo descreve o builder governado de delivery do OonCore. Estar no
checkout ou no contexto Docker **não** significa estar na imagem final.

| Origem | Destino/efeito | Contrato |
|---|---|---|
| `backend/` | `/app/backend/` | Código, manifests e assets de runtime; preserva caminhos relativos |
| `backend/package*.json` | instalação no estágio backend | Somente dependências de produção (`--omit=dev`) |
| `frontend/` | compilação no estágio frontend | `npm run build`; fontes não são copiadas para o runtime |
| `frontend/dist/` produzido no build | `/usr/share/nginx/html/` | Artefatos estáticos compilados |
| `central.app.json` | `/app/central.app.json` e `/src/central.app.json` no build frontend | Quando existente |
| Definições em `capabilitySettings["core.transactional-email"].templates[].definition` | Mesmo caminho relativo a `/app` | Somente arquivos declarados, dentro da raiz; traversal/symlink externo rejeitado |
| `docs/`, `.ooncore/`, arquivos da raiz e demais diretórios | Sem cópia genérica para o runtime | Não usar como origem de imports necessários em produção |
| `node_modules`, `.git`, `.env*`, `.npmrc`, `*.pem`, `*.key` | Excluídos pelo builder | A instalação local não pode sobrescrever dependências de produção |
| `frontend/.env.production` | Entrada do build frontend | Única exceção `.env`; gerada pelo executor, sem segredos |
| Testes dentro de `backend/` | Podem ser copiados como qualquer arquivo backend | Não são executados no runtime; não colocar segredos em fixtures |

O `.dockerignore` do App é preservado e acrescido de exclusões obrigatórias em
`.oon-delivery/Dockerfile.dockerignore`. Ele pode restringir ainda mais o contexto,
mas não reintroduzir dependências locais ou arquivos excluídos por essas regras.
As extensões listadas não identificam todos os segredos possíveis: nunca versione
credenciais. Assets adicionais não têm um mecanismo de cópia genérica.

## Assets e dependências

Para catálogos usados por `backend/src/services/omie-contracts.js`, use por exemplo:

```text
backend/src/assets/omie/catalog.json
backend/src/assets/omie/conversion-catalog.json
```

```js
const catalog = require('../assets/omie/catalog.json');
const conversions = require('../assets/omie/conversion-catalog.json');
```

O import `require('../../../docs/omie/catalog.json')` depende de um diretório da
raiz que não está na imagem; o resultado esperado é `IMAGE_MODULE_NOT_FOUND`.
Declare pacotes exigidos em runtime em `backend/package.json#dependencies`, não
apenas em `devDependencies` nem apenas no package da raiz.

## Carregamento não é cópia

O bootstrap carrega `central.config.js`, manifests declarativos do backend e os
arquivos `.js`/`.cjs` recursivos de `src/models`, `src/validations`, `src/triggers`,
`src/routes`, `src/pipelines`, `src/documents` e `src/hooks`. Outros diretórios,
como `src/services` e `src/assets`, entram por imports desses módulos; não são
autocarregados só por existirem. Não mantenha scripts executáveis de teste nos
diretórios de autocarregamento.

## Testes e imagem final

Se existe `scripts.test` na raiz, ele é o ponto de entrada da suíte e deve
orquestrar os componentes. Sem esse script, o executor roda os testes declarados
em backend e frontend. Não há inferência por texto de comando. Relatórios
registram `not_declared`, `root_orchestrated`, `not_run`, `passed` ou `failed`;
nenhum teste declarado não equivale a uma suíte aprovada.

Os testes usam dependências instaladas sem lifecycle scripts, em contêiner sem
credenciais e sem rede durante a execução. Testes que exigem serviços externos ou
scripts de instalação precisam ser compatibilizados com esse contrato; uma falha
nessa etapa não é automaticamente classificada como defeito da aplicação.

Após o build, a **mesma imagem**, identificada por ID `sha256`, é iniciada com o
entrypoint normal, usuário não privilegiado, filesystem de leitura, diretórios
temporários limitados, limites de CPU/memória/processos e timeout. MongoDB é
descartável. Ambos compartilham apenas loopback, sem acesso à rede externa,
credenciais reais, socket Docker ou mounts do host. Não há bypass de imports,
ativação ou permissões. Readiness deve passar em três observações consecutivas.

A morte do backend ou Nginx encerra o contêiner. Liveness consulta o backend sem
exigir banco saudável; readiness conserva os requisitos de banco. Perda
transitória do banco não deve provocar reinício só pela liveness.

Falha impede exportação da imagem para deploy; o executor não faz push,
provisionamento nem apply. O Workspace recebe etapa, categoria, código, caminho e
importador quando disponíveis e orientação. `502`/timeout isolados não comprovam
erro de código. O relatório não contém logs ou stack brutos.

Essa prova cobre carregamento e inicialização na configuração isolada. Não
substitui testes funcionais, autenticação/tenancy, integrações reais, imports
preguiçosos acionados somente por requisições nem a homologação Dev → HML → Prod.

---

<!-- source: AUTH_ACTIVATION_RBAC.md -->

# Autenticação, ativação e RBAC

## Plataforma

O backend verifica o token no escopo do App, resolve tenant e acesso, aplica a política local de RBAC e cria `req.accessContext`. O frontend usa permissões somente para experiência; o backend autoriza cada operação.

Ativação de plataforma cria a identidade operacional usada por integrações autorizadas. Rotas de login, launch exchange, ativação e primeiro acesso não estão disponíveis no runtime local.

## Catálogo público de perfis

Todo App com RBAC declarado expõe `GET /core/role-catalog`. O contrato `schemaVersion: 1` contém `appCode`, `enabled` e `roles[]` com `code`, `name`, `description` e `admin`. Desde o SDK 0.7.1, a extensão aditiva opcional `roles[].commercialPermissions` publica nomes explícitos de permissões funcionais permitidas pelo papel. Wildcards são expandidos somente pelas permissões declaradas em `rbac.permissions`; wildcard literal e namespaces `tenant`, `publications`, `homologation`, `production`, `apps`, `users` e `roles` são excluídos. Políticas internas e permissões técnicas não são publicadas.

O campo permanece opcional no schemaVersion 1: catálogos anteriores são conformes para descoberta e fluxos existentes. O novo aceite comercial inicial requer essa capacidade e deve falhar fechado com `APP_ROLE_CATALOG_UNAVAILABLE` quando ausente; não se infere autoridade do nome admin. Consumidores antigos devem tolerar campos adicionais. O runtime continua intersectando cada grant explícito com a política local atual.

O catálogo serve para descoberta e seleção de perfis pelo Control Plane. Ele não concede acesso: o backend consumidor deve validar `schemaVersion` e `appCode`, consultar somente o Deployment resolvido pela plataforma, revalidar o perfil antes de persistir o grant e falhar fechado quando o catálogo estiver ausente ou inválido.

## Local

O principal técnico é `local:developer`, sem usuário/tenant/licença na plataforma. O papel inicial é `developer` quando declarado, seguido por admin ou primeiro papel. A troca de perfil aceita apenas o manifesto e atualiza a sessão local.

O estado é `ativa_local`; o `ActivationGuard` não cria nem consulta `InstanciaEcossistema`. Isso não equivale a `ativa` publicada.

## Regras para extensões

- use `requirePermission` em rotas customizadas;
- derive filtros de `req.accessContext`;
- nunca autorize por header/body de perfil ou tenant;
- não implemente `verifyToken` em Central member/portal;
- não persista bearer no frontend;
- não trate simulação local como identidade operacional.


## Apps globais e tenant-alvo

Apps com `tenancyModel=none` não montam `TenantProvider`, não restauram tenant
do storage e não consomem o parâmetro reservado `tenant`. Cockpits globais
devem transportar a organização administrada com um identificador próprio,
como `targetTenantId`, e o BFF deve convertê-lo no header específico do
contrato administrativo. Esse alvo nunca integra a sessão do App.

---

<!-- source: BACKEND_API.md -->

# API pública do `@oondemand/oon-core-back`

Importe exclusivamente de `@oondemand/oon-core-back`. Caminhos internos não têm estabilidade garantida.

## Boot e definição

- `start({ cwd, listen })`: carrega o backend indicado por `cwd`, conecta Mongo, inicializa capabilities e inicia HTTP. `listen=false` devolve `{ app }`; com escuta, `{ app, server }`.
- `createApp()`: monta o Express já protegido usando o registro existente; não carrega os módulos do App nem conecta o banco sozinho.
- `activate()`: fluxo legado de ativação; não é usado no runtime local.
- `defineCentral`, `defineModel`, `defineCollection`, `defineDocument`, `definePipeline`, `defineRoutes`, `defineValidation`, `defineTrigger`: extensões imperativas suportadas.
- `fields`: factories de campos compatíveis com schema e metadata.
- `registry`: registry do processo; use APIs `define*`, não mutações internas.

## Segurança, RBAC e tenant

- `requirePermission(permission)`: middleware público de autorização. Em `router.private`, declare `{ permission }` no segundo argumento; não passe middleware nessa posição. Veja [PUBLIC_CONTRACTS.md](PUBLIC_CONTRACTS.md).
- `CORE_PERMISSIONS`, `rbacPolicy`, `roleByCode`, `permissionGranted`: leitura e avaliação da política declarada.
- `TENANT_HEADER`, `TENANCY_MODELS`, `DATA_SCOPES`: constantes canônicas.
- `createAccessContext` estrutura identidade já verificada; `readRequestedTenantId` lê a seleção solicitada, sem autenticá-la. Nas rotas use `req.accessContext`.
- `scopeFilter`, `mergeScopedFilter`, `scopeMutation`, `scopedIdFilter`: aplicam isolamento aos dados. Nunca aceite tenant do body como autoridade.

## Manifestos

- App: `APP_MANIFEST_FILENAME`, `APP_MANIFEST_SCHEMA_VERSION`, `SUPPORTED_APP_KINDS`, `SUPPORTED_APP_MODULES`, `AppManifestError`, `validateAppManifest`, `resolveAppManifestPath`, `appManifestToConfig`, `registerAppManifest`, `loadAppManifest`.
- Domínio: `DOMAIN_MANIFEST_FILENAME`, `DOMAIN_MANIFEST_SCHEMA_VERSION`, `SUPPORTED_DOMAIN_FIELD_KINDS`, `DOMAIN_EXPRESSION_OPERATORS`, `DomainManifestError`, `DomainRuleError`, `validateDomainManifest`, `domainManifestToDefinitions`, `registerDomainManifest`, `loadDomainManifest`, `evaluateDomainExpression`, `applyDomainMutation`, `validateDomainRecord`, `detectChangedFields`.
- Processo: `PROCESS_MANIFEST_FILENAME`, `PROCESS_MANIFEST_SCHEMA_VERSION`, `ProcessManifestError`, `validateProcessManifest`, `registerProcessManifest`, `loadProcessManifest`, `prepareProcessMutation`, `resolveProcessBindings`, `assertReferencePolicies`, `assertAtomicInvariants`, `assertDeleteAllowed`, `recalculateDependents`, `drainProcessJobs`.

Erros de manifesto carregam `code`, `statusCode` e `issues[]` com `path` e `message`.

## Capabilities

O namespace público `capabilities` contém:

- `capabilities.pdf.render(input, context): Promise<Buffer>`; contrato completo em [PDF_RENDERING.md](PDF_RENDERING.md);
- alias compatível `capabilities.pdfRendering.render`;
- `capabilities.transactionalEmail.send(input, context)` e operações administrativas; contrato completo em [TRANSACTIONAL_EMAIL.md](TRANSACTIONAL_EMAIL.md);
- `PdfRenderingError` e `TransactionalEmailError` para normalização específica.

O App nunca configura URL, credencial interna ou implementação de uma capability. A única exceção é a injeção de dublês documentada para testes automatizados.

`operationalRequestHeaders(options)` produz headers de identidade do Deployment. Retorna `LOCAL_OPERATION_NOT_SUPPORTED` no runtime local; nunca improvise identidade local.

## Runtime local

O namespace público `localDevelopment` expõe detecção, validação de loopback e utilitários de teste/integração do runtime. Apps consumidores normalmente apenas definem `OON_RUNTIME_MODE=local` e usam o scaffold.

## Erros

`GenericError(message, { statusCode, code, details })` é o erro operacional base. O App deve fornecer mensagem/detalhes seguros; o middleware produz o envelope, mas não remove automaticamente segredos do conteúdo arbitrário fornecido pelo App. Bootstrap, rotas, prefixos, permissões e `sensitiveBody` estão consolidados em [PUBLIC_CONTRACTS.md](PUBLIC_CONTRACTS.md).

---

<!-- source: BACKEND_DOMAIN_MANIFEST.md -->

# Manifesto declarativo de domínio — `central.domain.json`

O arquivo `central.domain.json`, localizado na raiz do backend da Central, declara models, campos, fórmulas e validações sem exigir um arquivo JavaScript por model.

O OonCore carrega o manifesto durante o bootstrap, antes de carregar `src/models`, `src/validations`, `src/triggers` e os demais diretórios de extensão.

> A Central declara o domínio e as regras. O OonCore constrói schema Mongoose, metadata, CRUD, cálculos protegidos e validações.

## Escopo da versão 1

O contrato cobre:

- identidade do manifesto;
- models e seus caminhos de API;
- configuração de CRUD já aceita por `defineModel`;
- campos primitivos, enumerações, referências e moedas;
- obrigatoriedade, valor padrão, busca, unicidade e índice simples;
- limites numéricos e de tamanho de texto;
- campos somente leitura protegidos nas mutações HTTP;
- campos calculados no servidor;
- dependências entre campos calculados, ordenadas automaticamente;
- precisão e tratamento de valores ausentes em fórmulas;
- validações declarativas entre campos, com condição opcional;
- validação estrutural com todos os problemas retornados em uma única exceção.

Ainda não fazem parte desta versão:

- índices compostos;
- triggers e transições declarativas;
- migrações automáticas de dados;
- mappings de integração;
- funções JavaScript embutidas no JSON.

As expressões são interpretadas por um avaliador fechado. O Core não usa `eval`, `Function` ou execução de código vindo do manifesto.

## Exemplo financeiro

```json
{
  "name": "Central SS Eventos",
  "slug": "ss-eventos",
  "schemaVersion": 1,
  "models": [
    {
      "name": "ProjetoItem",
      "singular": "item",
      "basePath": "/itens",
      "crud": {
        "enabled": true
      },
      "fields": {
        "quantidade": {
          "kind": "number",
          "required": true
        },
        "diarias": {
          "kind": "number",
          "required": true
        },
        "valorUnitario": {
          "kind": "currency",
          "required": true
        },
        "percentualFee": {
          "kind": "number",
          "default": 0
        },
        "valorContratado": {
          "kind": "currency",
          "default": 0
        },
        "valorPago": {
          "kind": "currency",
          "default": 0
        },
        "statusIntegracao": {
          "kind": "string",
          "readonly": true
        },
        "subtotal": {
          "kind": "currency",
          "computed": {
            "precision": 2,
            "expression": {
              "op": "multiply",
              "args": [
                { "field": "quantidade" },
                { "field": "diarias" },
                { "field": "valorUnitario" }
              ]
            }
          }
        },
        "valorFee": {
          "kind": "currency",
          "computed": {
            "precision": 2,
            "expression": {
              "op": "divide",
              "args": [
                {
                  "op": "multiply",
                  "args": [
                    { "field": "subtotal" },
                    { "field": "percentualFee" }
                  ]
                },
                { "value": 100 }
              ]
            }
          }
        },
        "total": {
          "kind": "currency",
          "computed": {
            "precision": 2,
            "expression": {
              "op": "add",
              "args": [
                { "field": "subtotal" },
                { "field": "valorFee" }
              ]
            }
          }
        }
      },
      "validations": [
        {
          "name": "pagamento-limitado-ao-contratado",
          "code": "PAGAMENTO_ACIMA_CONTRATADO",
          "field": "valorPago",
          "message": "O valor pago não pode superar o valor contratado.",
          "assert": {
            "op": "lte",
            "args": [
              { "field": "valorPago" },
              { "field": "valorContratado" }
            ]
          }
        }
      ]
    }
  ]
}
```

## Estrutura principal

| Propriedade | Obrigatória | Descrição |
|---|---:|---|
| `name` | sim | Nome legível da declaração de domínio. |
| `slug` | não | Identificador em minúsculas, números e hífens. |
| `schemaVersion` | sim | Nesta versão, deve ser `1`. |
| `models` | sim | Lista não vazia de models. |

## Model

| Propriedade | Obrigatória | Descrição |
|---|---:|---|
| `name` | sim | Nome PascalCase usado no registry e no Mongoose. |
| `singular` | não | Nome singular usado pelo Core. |
| `basePath` | não | Caminho iniciado por `/`. |
| `crud` | não | Mesmo contrato aceito por `defineModel`. |
| `options` | não | Opções JSON compatíveis com o schema Mongoose. |
| `fields` | sim | Objeto com pelo menos um campo. |
| `validations` | não | Lista de regras declarativas executadas depois dos cálculos. |

Não declare a mesma model no manifesto e em `src/models`. O registry interrompe o bootstrap para impedir duas fontes de verdade.

## Tipos de campo

- `string`
- `number`
- `boolean`
- `date`
- `ref`
- `enum`
- `currency`
- `currencyCode`
- `currencyConverted`

### Opções comuns

- `label`: rótulo para metadata e frontend;
- `description`: explicação funcional;
- `required`: campo obrigatório;
- `default`: valor padrão JSON;
- `readonly`: campo controlado pelo servidor;
- `searchable`: inclui texto na busca derivada do Core;
- `unique`: índice único simples;
- `index`: índice simples;
- `computed`: fórmula declarativa para campos numéricos ou monetários.

### Opções por tipo

- textos: `minLength`, `maxLength`;
- números e moedas: `min`, `max`;
- `ref`: `ref` com o nome da model relacionada;
- `enum`: `values` com textos únicos e não vazios;
- `currencyConverted`: `base` com código ISO de três letras.

## Campos calculados

`computed` é permitido em `number`, `currency` e `currencyConverted`.

```json
{
  "kind": "currency",
  "computed": {
    "expression": {
      "op": "multiply",
      "args": [
        { "field": "quantidade" },
        { "field": "valorUnitario" }
      ]
    },
    "precision": 2,
    "nullAsZero": true
  }
}
```

| Propriedade | Padrão | Descrição |
|---|---:|---|
| `expression` | — | Expressão obrigatória. |
| `precision` | `2` | Casas decimais, entre 0 e 8. |
| `nullAsZero` | `true` | Trata campos ausentes ou vazios como zero nas operações numéricas. |

Campos calculados:

- são automaticamente `readonly`;
- são protegidos pelo pipeline de mutação HTTP; valores calculados continuam graváveis pelo próprio Core após recálculo;
- são recalculados no backend em criação, edição, patch e importação;
- são calculados em ordem de dependência;
- não podem formar ciclos;
- aparecem na metadata com `readonly: true` e a declaração `computed`.

## Expressões

Uma expressão declara exatamente um destes nós:

```json
{ "value": 100 }
```

```json
{ "field": "valorUnitario" }
```

```json
{
  "op": "multiply",
  "args": [
    { "field": "quantidade" },
    { "field": "valorUnitario" }
  ]
}
```

### Operadores aritméticos

- `add`
- `subtract`
- `multiply`
- `divide`
- `min`
- `max`
- `abs`
- `negate`
- `coalesce`

### Operadores de comparação

- `eq`
- `neq`
- `gt`
- `gte`
- `lt`
- `lte`

### Operadores lógicos e de presença

- `and`
- `or`
- `not`
- `present`
- `in`

Divisão por zero e valores não numéricos em fórmulas geram `DomainRuleError` com status 422.

## Validações entre campos

As validações rodam depois que o Core consolidou o registro e recalculou todos os campos dependentes.

```json
{
  "name": "valor-pago-valido",
  "code": "PAGAMENTO_ACIMA_CONTRATADO",
  "field": "valorPago",
  "message": "O valor pago não pode superar o valor contratado.",
  "when": {
    "op": "present",
    "args": [{ "field": "valorPago" }]
  },
  "assert": {
    "op": "lte",
    "args": [
      { "field": "valorPago" },
      { "field": "valorContratado" }
    ]
  }
}
```

| Propriedade | Obrigatória | Descrição |
|---|---:|---|
| `name` | sim | Identificador único da validação dentro da model. |
| `message` | sim | Mensagem operacional apresentada ao usuário. |
| `assert` | sim | Expressão que deve resultar em verdadeiro. |
| `when` | não | Condição para executar a regra. |
| `field` | não | Campo associado ao erro. |
| `code` | não | Código em maiúsculas para tratamento programático. |

Falhas geram `DomainRuleError` com `statusCode: 422`, `code`, `field`, `rule` e detalhes compatíveis com o tratamento de erros do Core.

## Proteção de campos somente leitura

A proteção não depende apenas do frontend.

- valor readonly enviado na criação é rejeitado;
- alteração de valor readonly é rejeitada;
- em edição, o mesmo valor pode voltar no payload e é removido antes da persistência;
- campos calculados podem voltar no payload somente quando coincidem com o resultado calculado pelo servidor;
- tentativa de adulterar um campo calculado é rejeitada;
- services recebem somente campos permitidos e os resultados recalculados.

Isso permite formulários que enviam o registro completo sem abrir espaço para alterar totais, status técnicos ou identificadores controlados pelo sistema.

## Atualizações parciais

Em `PUT` ou `PATCH`, o Core:

1. carrega o registro atual quando existem regras declarativas ou `defineValidation`;
2. remove ou bloqueia campos readonly;
3. consolida os campos atuais com as alterações recebidas;
4. recalcula campos dependentes em ordem;
5. executa validações declarativas;
6. executa a validação JavaScript registrada, quando existir;
7. persiste somente as alterações permitidas e os valores calculados.

A validação JavaScript recebe:

```js
{
  op,
  method,
  id,
  current,
  requestedChanges,
  changes,
  consolidated
}
```

## Erros de validação do manifesto

Um manifesto estruturalmente inválido lança `DomainManifestError`:

```js
{
  name: "DomainManifestError",
  code: "OON_DOMAIN_MANIFEST_INVALID",
  statusCode: 422,
  issues: [
    {
      path: "models[0].fields.total.computed.expression",
      message: "dependência circular entre campos calculados: total -> fee -> total."
    }
  ]
}
```

A validação agrega os problemas para que o autor corrija o documento em uma única rodada.

## APIs públicas

```js
const {
  validateDomainManifest,
  domainManifestToDefinitions,
  registerDomainManifest,
  loadDomainManifest,
  evaluateDomainExpression,
  applyDomainMutation,
  DomainManifestError,
  DomainRuleError,
  DOMAIN_EXPRESSION_OPERATORS
} = require("@oondemand/oon-core-back");
```

Na operação normal não é necessário chamar essas funções: `oonCore-back start` descobre automaticamente `central.domain.json` e o CRUD aplica as regras.

## Compatibilidade durante a migração

Os diretórios JavaScript continuam disponíveis para regras ainda não declarativas. A ordem é:

1. `central.config.js`;
2. `central.domain.json`;
3. diretórios em `src/`.

Isso permite migrar model por model. `defineValidation` continua disponível e roda depois das fórmulas e validações declarativas.

---

<!-- source: BACKEND_PATTERNS.md -->

# Padrões Backend

O backend da Central deve conter apenas domínio e extensões. Boot, infraestrutura, CRUD padrão, autenticação, RBAC e metadata pertencem ao `@oondemand/oon-core-back`.

## Estrutura esperada

```txt
backend/
├── central.config.js
├── central.manifest.json
└── src/
    ├── models/
    ├── validations/
    ├── triggers/
    ├── hooks/
    ├── mappings/
    ├── documents/
    ├── pipelines/
    ├── routes/
    ├── controllers/
    └── services/
```

## Models

Use models para declarar entidades de negócio. Cada model deve ser pequeno, com nomes claros e campos compatíveis com as telas e processos.

Boas práticas:

- use campos explícitos;
- defina tipos, obrigatoriedade e enums quando aplicável;
- preserve campos de status para esteiras;
- evite regras complexas diretamente no schema;
- evite dependência direta de frontend.

## Validations

Use validations para regras de negócio síncronas e mensagens claras para o usuário.

Exemplos:

- campo obrigatório condicional;
- status permitido para transição;
- valor mínimo/máximo;
- combinação inválida de campos;
- bloqueio por permissão ou perfil.

Em inclusões, a validation recebe os dados enviados. Em atualizações por `PUT` ou `PATCH`, o OonCore carrega o registro atual e entrega à validation o registro consolidado com as alterações. Isso permite que formulários em abas e datagrids enviem somente os campos modificados sem perder referências obrigatórias durante a validação.

O segundo argumento informa o contexto da operação:

```js
async function validar(dados, contexto) {
  // contexto.op: "create" ou "update"
  // contexto.method: "post", "put" ou "patch"
  // contexto.id: identificador do registro em updates
  // contexto.current: registro antes da alteração
  // contexto.changes: somente os campos enviados
  // contexto.consolidated: registro completo usado em `dados`
}
```

A validation deve avaliar `dados` como estado final pretendido. Use `contexto.changes` apenas quando a regra depender de quais campos foram efetivamente alterados.

## Triggers e hooks

Use triggers e hooks para efeitos controlados depois ou antes de alterações.

Exemplos:

- criar ticket de integração;
- recalcular campos derivados;
- gerar histórico operacional;
- disparar conector;
- atualizar etapa da esteira.

Regras:

- trigger não deve esconder regra crítica sem validação;
- evite efeitos irreversíveis sem log;
- integração externa deve passar por camada de integração/conector;
- falhas de integração devem gerar status rastreável, não quebrar silenciosamente o processo.

## Rotas customizadas

Crie rotas customizadas somente quando o CRUD/metadata do Core não resolver.

Toda rota customizada deve ter:

- autenticação;
- verificação de permissão;
- validação de entrada;
- tratamento de erro;
- resposta padronizada;
- ausência de segredo hardcoded.

## Serviços

Use `services/` para regras reutilizáveis. Evite controllers grandes.

## Segurança

Nunca confie no frontend para permissão, tenant, app ou perfil. O backend deve validar tudo que altera dados, dispara integrações ou expõe informações sensíveis.

---

<!-- source: BACKEND_PROCESS_MANIFEST.md -->

# Manifesto backend de processos

O arquivo opcional `backend/central.process.json` declara capacidades de processo que pertencem ao OonCore e não à implementação local de uma Central.

Ele complementa:

- `central.app.json`: identidade, módulos e capabilities da aplicação;
- `backend/central.domain.json`: models, campos, fórmulas do próprio registro e validações locais;
- `frontend/src/app`: composição code-first de coleções, esteiras e ações exibidas.

O manifesto de processos é carregado **depois** do domínio. Por isso, toda model e todo campo citados precisam existir em `central.domain.json`.

## Contrato mínimo

```json
{
  "schemaVersion": 1,
  "models": {
    "Pagamento": {
      "workflow": {},
      "bindings": [],
      "deleteProtection": [],
      "atomicInvariants": []
    }
  }
}
```

O runtime não executa JavaScript, `eval`, nomes de funções ou módulos informados no JSON. Expressões usam a mesma AST fechada das regras de domínio.

## Workflow e transições

```json
{
  "workflow": {
    "stageField": "etapa",
    "initialStages": ["Solicitado"],
    "defaultStage": "Solicitado",
    "transitions": [
      { "from": "Solicitado", "to": "Aprovado" },
      {
        "from": "Aprovado",
        "to": "Aguardando NF",
        "when": {
          "op": "eq",
          "args": [
            { "field": "aprovadoFinanceiro" },
            { "value": true }
          ]
        }
      }
    ],
    "lockedFieldsByStage": {
      "Enviado para pagamento": ["valor", "projetoId", "projetoItemId"],
      "Pagamento Ok": ["valor", "projetoId", "projetoItemId"]
    },
    "lockedMessage": "Os dados de negócio ficam bloqueados nesta etapa.",
    "onEnter": [
      {
        "stage": "Enviado para pagamento",
        "set": {
          "statusTrabalho": "Trabalhando",
          "statusPagamento": "Pendente"
        }
      }
    ],
    "automaticTransitions": [
      {
        "when": {
          "op": "eq",
          "args": [
            { "field": "pagamentoLiquidado" },
            { "value": true }
          ]
        },
        "to": "Pagamento Ok",
        "set": { "statusTrabalho": "Trabalhando" }
      }
    ]
  }
}
```

Regras importantes:

- o backend compara o valor anterior e o novo; enviar novamente a mesma etapa não cria uma transição;
- uma mudança manual precisa existir em `transitions` e satisfazer `when`;
- `lockedFieldsByStage` é aplicado sobre a etapa anterior e impede alterações de negócio mesmo por `PUT` ou `PATCH` diretos;
- `onEnter` produz alterações confiáveis do Core;
- `automaticTransitions` é executado pelo servidor depois dos bindings e não depende do frontend.

A UI pode continuar declarando botões `transition` e `setField`. Ela é uma projeção; a autoridade permanece no backend.

## Bindings cross-model

Bindings preenchem campos derivados a partir de outra model ou de registros relacionados. Todos são resolvidos em lote.

### Lookup

```json
{
  "field": "percentualFeeAplicado",
  "kind": "lookup",
  "sourceModel": "Projeto",
  "localField": "projetoId",
  "sourceField": "percentualFee",
  "watchFields": ["percentualFee"],
  "recalculate": "async",
  "default": 0
}
```

Quando `Projeto.percentualFee` muda, o Core encontra os itens dependentes e agenda um recálculo assíncrono. O recálculo usa uma leitura por binding e um `bulkWrite`, em vez de executar `save()` item a item na requisição do usuário.

### Agregação de relacionamento

```json
{
  "field": "pagamentoTotalPlanejado",
  "kind": "aggregate",
  "sourceModel": "Pagamento",
  "foreignField": "projetoItemId",
  "operator": "sum",
  "sourceField": "valor",
  "match": {
    "canceladoNaCentral": { "neq": true }
  },
  "default": 0
}
```

Operadores disponíveis:

- `sum`;
- `count`;
- `min`;
- `max`.

Filtros aceitam igualdade direta ou `{ "eq": ... }`, `{ "neq": ... }`, `{ "in": [...] }` e `{ "nin": [...] }`.

### Expressão derivada

```json
{
  "field": "pagamentoValorPendente",
  "kind": "expression",
  "precision": 2,
  "expression": {
    "op": "max",
    "args": [
      { "value": 0 },
      {
        "op": "subtract",
        "args": [
          { "field": "contratacaoTotal" },
          { "field": "pagamentoTotalPago" }
        ]
      }
    ]
  }
}
```

Bindings são avaliados na ordem declarada. Assim, uma expressão pode consumir lookups e agregações anteriores.

Além dos operadores numéricos e lógicos do domínio, processos podem usar:

- `if`: condição, valor verdadeiro e valor falso;
- `concat`: concatenação segura de valores;
- `formatCurrency`: valor, moeda opcional e locale opcional.

## Recálculo imediato e assíncrono

`recalculate` controla a reação quando a model de origem muda:

- `immediate` (padrão): dependentes são atualizados no mesmo ciclo da mutação;
- `async`: a resposta não percorre todos os dependentes; o Core coloca o recálculo na fila interna e usa operações em lote.

Use `async` para alterações de um pai com muitos filhos, como a mudança de percentuais de um Projeto. Use `immediate` quando o registro pai precisa refletir a alteração antes da resposta, como o resumo de pagamentos de um item.

A API `drainProcessJobs()` existe para testes e homologações determinísticas.

## Proteção declarativa de exclusão

```json
{
  "deleteProtection": [
    {
      "sourceModel": "Pagamento",
      "foreignField": "projetoItemId",
      "message": "Não é possível excluir o item porque existem pagamentos vinculados."
    }
  ]
}
```

A verificação ocorre no CRUD oficial antes de `findByIdAndDelete`. Não é necessário sobrescrever métodos do Mongoose.

## Invariável financeira atômica

```json
{
  "atomicInvariants": [
    {
      "name": "pagamentos-limitados-ao-contratado",
      "kind": "relatedSumLteParentField",
      "parentModel": "ProjetoItem",
      "parentLocalField": "projetoItemId",
      "sourceField": "valor",
      "parentField": "contratacaoTotal",
      "match": {
        "canceladoNaCentral": { "neq": true }
      },
      "tolerance": 0.01,
      "code": "PAGAMENTO_ACIMA_CONTRATADO",
      "message": "A soma {total} não pode ultrapassar o valor contratado {limit}."
    }
  ]
}
```

O Core executa a mutação em transação MongoDB e incrementa uma versão interna no registro pai antes de calcular a soma. Duas inclusões simultâneas disputam a mesma escrita do pai:

1. uma transação conclui;
2. a outra recebe conflito transitório;
3. o Core repete a transação;
4. a soma é refeita já considerando a primeira inclusão;
5. a segunda inclusão é aceita ou rejeitada pela invariável.

Uma simples validação `find + sum + save`, fora de transação, **não** oferece essa garantia.

## Alterações reais

O contexto enviado a `defineValidation` agora inclui `changedFields`. A lista contém somente campos cujo valor final difere do registro anterior, incluindo valores derivados pelo Core. Isso evita efeitos colaterais acionados por round-trips de campos sem alteração real.

## Fronteira recomendada

Pertence ao Core/process manifest:

- transições e bloqueios de etapa;
- status operacionais recorrentes;
- dependências e recálculos cross-model;
- agregações relacionadas;
- proteção de exclusão;
- invariáveis concorrentes;
- processamento em lote/assíncrono.

Permanece na Central:

- fórmula comercial específica;
- tipos de responsáveis permitidos pelo negócio;
- regras fiscais específicas;
- integrações e mapeamentos particulares;
- mensagens e condições próprias do processo.

A Central declara essas particularidades usando o contrato; não reimplementa o mecanismo.

---

<!-- source: CAPABILITIES.md -->

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

---

<!-- source: CHECKLIST_IMPLEMENTACAO.md -->

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

---

<!-- source: CODEX.md -->

# CODEX.md — ponte de compatibilidade

A fonte canônica, completa e neutra do OonCore é `AGENTS.md`.

Ao trabalhar em uma Central:

1. leia primeiro o `AGENTS.md` da raiz do projeto, quando existir;
2. leia `.ooncore/AGENTS.md`;
3. valide `.ooncore/manifest.json` com `npm run ooncore:docs:check`;
4. siga as referências de `.ooncore/docs/` indicadas para a tarefa.

Não mantenha regras exclusivas neste arquivo. Codex, ChatGPT, Kimi, Manus e outros Agents devem consumir o mesmo contrato versionado.

---

<!-- source: COLLECTIONS_AND_PIPELINES.md -->

# Coleções, Documentos e Esteiras

Coleções, documentos e esteiras são a base operacional da Central Oon.

## Coleções

Use coleções para entidades de negócio:

- clientes;
- fornecedores;
- pedidos;
- pagamentos;
- documentos fiscais;
- serviços tomados;
- serviços prestados;
- integrações;
- tickets operacionais.

Cada coleção deve ter:

- model no backend;
- metadata para CRUD;
- campos de status quando participar de esteira;
- validações de negócio;
- configuração de tela no frontend.

## Documentos

Use documentos para entidades que exigem governança documental, aprovação, anexos ou histórico específico.

Exemplos:

- NF;
- contrato;
- proposta;
- comprovante;
- ordem de serviço;
- pedido de compra.

## Esteiras de processo

Use esteiras para fluxos operacionais com etapas claras.

Boas práticas:

- status/etapa deve estar no backend;
- transições devem ser validadas;
- ações devem registrar usuário e data;
- exceções devem ter status próprio;
- cada etapa deve representar uma decisão operacional real.

## Esteiras de integração

Use esteiras de integração para acompanhar comunicação com sistemas externos.

Estados recomendados:

- pendente;
- em processamento;
- enviado;
- concluído;
- falha;
- aguardando retry;
- cancelado.

Integrações não devem ser caixas-pretas. O usuário operacional precisa enxergar o que aconteceu, qual erro ocorreu e qual ação pode ser tomada.

---

<!-- source: CORE_UPGRADE.md -->

# Atualização coordenada do OonCore

Esta documentação corresponde à release **0.7.8**, linha `0.7.x`. Preserve as regras e o domínio do App. Escolha uma versão publicada e compatível e atualize backend, frontend e gerador juntos.

Na raiz do App, para adotar a release deste guia:

```bash
npm install --save-dev --save-exact @oondemand/create-central-oon@0.7.8
npm install --prefix backend --save-exact @oondemand/oon-core-back@0.7.8
npm install --prefix frontend --save-exact @oondemand/oon-core-front@0.7.8
npm run ooncore:docs
npx --no-install create-central-oon doctor
npm run build --prefix frontend
```

O comando oficial regenera cache, manifesto e hashes; nunca edite `.ooncore` à mão. Versione os três package.json, seus lockfiles e o cache. Em Apps organizados como workspaces, use as opções de workspace equivalentes e preserve o lockfile único do projeto.

Revise `central.app.json#compatibility.core` conforme as funções usadas e só aumente o mínimo após validar a migração. A faixa da linha é `>=0.7.0 <0.8.0`; os exemplos de [TASK_INDEX.md](TASK_INDEX.md) indicam seu piso específico. Não confunda o schema do manifesto com a versão do pacote.

Execute os testes existentes e o smoke da jornada. Testes do App devem verificar comportamento/compatibilidade, não um literal de versão antiga sem justificativa. Preserve configurações operacionais de publicação; tokens fixos e identidade de plataforma não pertencem ao caminho local. Publique pelo fluxo existente e registre o commit homologado em Dev. Nenhum outro App precisa atualizar por causa desta entrega.


Em Apps existentes, altere o script raiz `check` para `create-central-oon doctor`. Ele já inclui cache e conformance: não duplique essas duas verificações no mesmo CI. O procedimento acima preserva o domínio; o comando `example` é somente para bases novas. Falha parcial em npm install exige concluir os três upgrades antes do sync/check; não publique versões divergentes.

---

<!-- source: DETAIL_MODAL_AND_RELATED_GRIDS.md -->

# DETAIL_MODAL_AND_RELATED_GRIDS.md — Modal com Abas e Grids Relacionados

Este documento define o contrato desejado para evoluir o `@oondemand/oon-core-front` com modal de detalhe, abas, grids relacionados, edição inline e ações por linha.

Status: **especificação para implementação**.

## 1. Motivação

Centrais operacionais frequentemente têm uma entidade principal com filhos operacionais.

Exemplos:

- Projeto -> Itens -> Pagamentos
- Pedido -> Produtos -> Expedições
- Contrato -> Parcelas -> Documentos
- Cliente -> Atividades -> Histórico
- Migração -> Registros -> Exceções

Hoje, esses casos tendem a virar páginas customizadas. O objetivo é abstrair o padrão no Core.

## 2. Resultado esperado

O manifesto deve ser capaz de declarar:

```txt
Grid principal da coleção
└── ação editar
    └── modal com abas
        ├── Resumo
        ├── Dados Principais
        ├── Itens relacionados editáveis inline
        └── Pagamentos/Histórico somente leitura
```

## 3. Extensão proposta do manifesto

### 3.1. Collections com list e detailModal

```json
{
  "model": "OrcamentoProjeto",
  "mode": "dynamic",
  "path": "/orcamentos-projetos",
  "label": "Orçamentos/Projetos",
  "section": "Operação",
  "list": {
    "filters": [],
    "columns": [],
    "rowActions": []
  },
  "relations": {},
  "detailModal": {
    "enabled": true,
    "titleField": "nome",
    "size": "xl",
    "defaultTab": "resumo",
    "tabs": []
  }
}
```

### 3.2. list.filters

Filtros declarativos renderizados acima do grid.

```json
{
  "field": "tipoRegistro",
  "label": "Tipo",
  "type": "select",
  "options": [
    { "label": "Orçamentos e projetos", "value": "" },
    { "label": "Só orçamentos", "value": "Orçamento" },
    { "label": "Só projetos", "value": "Projeto" }
  ]
}
```

Tipos iniciais:

- `text`
- `select`
- `date`
- `dateRange`
- `numberRange`
- `boolean`
- `ref`

### 3.3. list.rowActions

Ações no grid principal.

```json
{
  "type": "openDetailModal",
  "label": "Editar",
  "icon": "edit",
  "initialTab": "resumo"
}
```

Tipos iniciais:

- `openDetailModal`
- `navigate`
- `apiAction`
- `customAction`

### 3.4. relations

Relações nomeadas reutilizáveis por abas, filtros e ações.

```json
{
  "relations": {
    "itens": {
      "model": "OrcamentoItem",
      "foreignKey": "projetoId",
      "parentKey": "_id"
    },
    "pagamentos": {
      "model": "Pagamento",
      "foreignKey": "projetoId",
      "parentKey": "_id"
    }
  }
}
```

## 4. Abas suportadas

### 4.1. summary

Cards de resumo.

```json
{
  "id": "resumo",
  "label": "Resumo",
  "type": "summary",
  "cards": [
    { "label": "Itens", "source": "relatedCount", "relation": "itens" },
    { "label": "Total PARA", "field": "totalParaComImpostos", "format": "currency" }
  ]
}
```

Fontes:

- `field`
- `relatedCount`
- `relatedSum`
- `relatedAvg`
- `customMetric`

Formatos:

- `text`
- `number`
- `currency`
- `percent`
- `date`
- `badge`

### 4.2. form

Formulário do registro principal.

```json
{
  "id": "dados",
  "label": "Dados Principais",
  "type": "form",
  "groups": [
    {
      "label": "Identificação",
      "fields": ["tipoRegistro", "codigo", "nome", "status"]
    }
  ]
}
```

### 4.3. relatedGrid

Grid de filhos editável ou não.

```json
{
  "id": "itens",
  "label": "Itens",
  "type": "relatedGrid",
  "relation": "itens",
  "editable": true,
  "editMode": "inline",
  "columns": [],
  "rowActions": []
}
```

### 4.4. readonlyGrid

Grid relacionado somente leitura.

```json
{
  "id": "pagamentos",
  "label": "Pagamentos",
  "type": "readonlyGrid",
  "relation": "pagamentos",
  "columns": ["codigo", "descricao", "statusEsteira", "valorFechamento"]
}
```

### 4.5. customComponent

Aba com componente customizado registrado por chave.

```json
{
  "id": "analise",
  "label": "Análise",
  "type": "customComponent",
  "component": "custom:AnaliseProjeto"
}
```

## 5. Colunas de relatedGrid

```json
{
  "field": "totalParaComImpostos",
  "label": "Total PARA",
  "editable": true,
  "format": "currency",
  "width": 140
}
```

Propriedades:

- `field`
- `label`
- `editable`
- `readonly`
- `format`
- `renderer`
- `editor`
- `width`
- `hidden`
- `roles`
- `required`

## 6. Edição inline

O grid editável deve manter alterações em estado local por linha.

Requisitos:

- célula editável conforme metadata do campo;
- linha marcada como alterada;
- botão `Salvar` por linha;
- botão `Cancelar` por linha;
- `PUT /:modelPath/:id` usando CRUD genérico;
- loading por linha;
- erro por linha;
- refresh pós-salvamento configurável.

## 7. Row actions

### 7.1. apiAction

```json
{
  "id": "gerarPagamento",
  "label": "Gerar pagamento",
  "type": "apiAction",
  "method": "POST",
  "endpoint": "/api/ss-eventos/orcamentos-itens/:id/gerar-pagamento",
  "confirm": {
    "title": "Gerar pagamento?",
    "description": "Será criado um ticket financeiro vinculado a este item."
  },
  "disabledWhen": {
    "field": "pagamentoId",
    "exists": true
  },
  "refresh": ["self", "pagamentos", "resumo", "parent"]
}
```

### 7.2. Interpolação de endpoint

Suportar:

- `:id` -> `_id` da linha;
- `:parentId` -> `_id` do registro pai;
- `:fieldName` -> valor do campo na linha;
- `:parent.fieldName` -> valor do campo no pai.

### 7.3. disabledWhen

Operadores mínimos:

```json
{ "field": "pagamentoId", "exists": true }
{ "field": "status", "equals": "Cancelado" }
{ "field": "valor", "gt": 0 }
{ "field": "tipo", "in": ["A", "B"] }
```

### 7.4. refresh

Alvos:

- `self`: grid/aba atual;
- `parent`: registro principal;
- nome de aba: `pagamentos`, `resumo` etc.;
- `all`: todas as queries da modal.

## 8. RBAC

Cada nível pode ter `roles` ou `permissions`.

```json
{
  "id": "gerarPagamento",
  "roles": ["admin", "financeiro"]
}
```

A UI deve ocultar/desabilitar conforme permissão, mas a autoridade final continua no backend.

## 9. Componentes Core necessários

### CoreDetailModal

Responsável por:

- abrir detalhe/criação;
- buscar registro principal;
- controlar abas;
- salvar dados principais;
- orquestrar refresh;
- validar RBAC visual;
- renderizar erros.

### CoreTabbedDetail

Renderiza abas configuradas no manifesto.

### CoreRelatedGrid

Renderiza grid relacionado pelo `relation`.

### CoreInlineEditableCell

Renderiza o editor apropriado por tipo de campo.

### CoreRowAction

Executa ações declaradas por linha.

### CoreSummaryCards

Renderiza cards de resumo por fields e agregações relacionadas.

## 10. Compatibilidade

A implementação deve ser compatível com manifestos existentes.

- `collections[]` atual continua funcionando.
- `detailModal` é opcional.
- `list` é opcional.
- Sem `rowActions`, mantém ação padrão do Core.
- Sem `form.groups`, mantém formulário atual.

## 11. Critérios de aceite

- O manifesto consegue declarar a tela de Orçamentos/Projetos da SS Eventos sem página React customizada.
- A tela principal renderiza filtros, busca, grid e ação editar.
- A ação editar abre modal com abas.
- A aba Dados Principais salva o registro pai.
- A aba Itens carrega apenas filhos do pai selecionado.
- A aba Itens permite edição inline por linha.
- A aba Itens executa ação `Gerar pagamento` por linha.
- Após gerar pagamento, o item mostra badge de pagamento gerado.
- A aba Pagamentos recarrega automaticamente.
- A aba Resumo atualiza contadores/totais.
- RBAC visual respeita roles/permissions declaradas.
- Sem regressão em coleções simples.

## 12. Exemplo completo SS Eventos

```json
{
  "model": "OrcamentoProjeto",
  "mode": "dynamic",
  "path": "/orcamentos-projetos",
  "label": "Orçamentos/Projetos",
  "section": "Operação",
  "list": {
    "filters": [
      {
        "field": "tipoRegistro",
        "label": "Tipo",
        "type": "select",
        "options": [
          { "label": "Orçamentos e projetos", "value": "" },
          { "label": "Só orçamentos", "value": "Orçamento" },
          { "label": "Só projetos", "value": "Projeto" }
        ]
      }
    ],
    "columns": ["tipoRegistro", "codigo", "nome", "cliente", "status", "totalItens", "totalParaComImpostos", "lucroTotalEvento"],
    "rowActions": [
      { "type": "openDetailModal", "label": "Editar", "icon": "edit", "initialTab": "resumo" }
    ]
  },
  "relations": {
    "itens": { "model": "OrcamentoItem", "foreignKey": "projetoId", "parentKey": "_id" },
    "pagamentos": { "model": "Pagamento", "foreignKey": "projetoId", "parentKey": "_id" }
  },
  "detailModal": {
    "enabled": true,
    "titleField": "nome",
    "defaultTab": "resumo",
    "tabs": [
      {
        "id": "resumo",
        "label": "Resumo",
        "type": "summary",
        "cards": [
          { "label": "Itens", "source": "relatedCount", "relation": "itens" },
          { "label": "Pagamentos", "source": "relatedCount", "relation": "pagamentos" },
          { "label": "Total PARA", "field": "totalParaComImpostos", "format": "currency" },
          { "label": "Lucro", "field": "lucroTotalEvento", "format": "currency" }
        ]
      },
      {
        "id": "dados",
        "label": "Dados Principais",
        "type": "form",
        "groups": [
          { "label": "Identificação", "fields": ["tipoRegistro", "codigo", "nome", "status", "cliente"] },
          { "label": "Evento", "fields": ["dataEvento", "localEvento", "contato"] },
          { "label": "Totais", "fields": ["totalItens", "totalParaComImpostos", "lucroTotalEvento"] }
        ]
      },
      {
        "id": "itens",
        "label": "Itens",
        "type": "relatedGrid",
        "relation": "itens",
        "editable": true,
        "editMode": "inline",
        "columns": [
          { "field": "linhaPlanilha", "readonly": true },
          { "field": "categoria", "editable": true },
          { "field": "item", "editable": true },
          { "field": "fornecedorRazaoSocial", "editable": true },
          { "field": "status", "editable": true },
          { "field": "totalParaComImpostos", "editable": true, "format": "currency" },
          { "field": "formaPagamento", "editable": true },
          { "field": "pagamentoId", "label": "Pagamento", "readonly": true, "display": "badgeExists" }
        ],
        "rowActions": [
          {
            "id": "gerarPagamento",
            "label": "Gerar pagamento",
            "type": "apiAction",
            "method": "POST",
            "endpoint": "/api/ss-eventos/orcamentos-itens/:id/gerar-pagamento",
            "disabledWhen": { "field": "pagamentoId", "exists": true },
            "refresh": ["self", "pagamentos", "resumo", "parent"]
          }
        ]
      },
      {
        "id": "pagamentos",
        "label": "Pagamentos",
        "type": "readonlyGrid",
        "relation": "pagamentos",
        "columns": ["codigo", "descricao", "fornecedorRazaoSocial", "statusEsteira", "valorFechamento", "formaPagamento", "dataPagamento"]
      }
    ]
  }
}
```

## 11. Status implementado no Core

O `@oondemand/oon-core-front` implementa o contrato acima de forma genérica nos componentes `CoreDetailModal`, `CoreTabbedDetail`, `CoreSummaryCards`, `CoreRelatedGrid`, `CoreInlineEditableCell` e `CoreRowAction`.

Exemplo completo:

```json
{
  "model": "OrcamentoProjeto",
  "mode": "dynamic",
  "path": "/orcamentos-projetos",
  "label": "Orçamentos/Projetos",
  "section": "Operação",
  "list": {
    "filters": [{ "field": "tipoRegistro", "label": "Tipo", "type": "select", "options": [{ "label": "Todos", "value": "" }] }],
    "rowActions": [{ "type": "openDetailModal", "label": "Editar", "initialTab": "resumo" }]
  },
  "relations": {
    "itens": { "model": "OrcamentoItem", "foreignKey": "projetoId", "parentKey": "_id" },
    "pagamentos": { "model": "Pagamento", "foreignKey": "projetoId", "parentKey": "_id" }
  },
  "detailModal": {
    "enabled": true,
    "titleField": "nome",
    "defaultTab": "resumo",
    "tabs": [
      { "id": "resumo", "label": "Resumo", "type": "summary", "cards": [{ "label": "Itens", "source": "relatedCount", "relation": "itens" }] },
      { "id": "dados", "label": "Dados Principais", "type": "form", "groups": [{ "label": "Identificação", "fields": ["codigo", "nome", "status"] }] },
      { "id": "itens", "label": "Itens", "type": "relatedGrid", "relation": "itens", "editable": true, "editMode": "inline", "columns": ["item", "status"] },
      { "id": "pagamentos", "label": "Pagamentos", "type": "readonlyGrid", "relation": "pagamentos", "columns": ["codigo", "valorFechamento"] }
    ]
  }
}
```

`rowActions` do tipo `apiAction` suportam interpolação de `:id`, `:parentId`, `:fieldName` e `:parent.fieldName`, além de `confirm`, `disabledWhen`, `hiddenWhen` e `refresh` com `self`, `parent`, `all` ou o id de uma aba.

---

<!-- source: DO_AND_DONT.md -->

# Do and Don't

## Faça

- Use o Core antes de criar código novo.
- Modele o domínio com clareza.
- Prefira configuração e metadata.
- Escreva validações explícitas.
- Mantenha regras críticas no backend.
- Use esteiras para processos com status.
- Use conectores para integrações.
- Registre erros de forma operacional.
- Mantenha compatibilidade com atualização dos pacotes.
- Atualize `.ooncore/` com `npm run ooncore:docs`.

## Não faça

- Não recrie CRUD.
- Não recrie autenticação.
- Não duplique RBAC no frontend.
- Não criar um frontend inteiro se um override resolve.
- Não chamar APIs externas direto de qualquer lugar.
- Não hardcode tenant, app, usuário, URL sensível ou segredo.
- Não colocar regra crítica apenas no frontend.
- Não ignorar logs e rastreabilidade.
- Não editar `.ooncore/context.generated.md` manualmente.
- Não depender de documentação externa para codificar a arquitetura.

---

<!-- source: ERRORS.md -->

# Contrato de erros

Erros de domínio lançados com `GenericError` e `code` usam `{ message, error: { code, message, details?, requestId? } }` e status HTTP coerente. O App fornece mensagem/detalhes seguros; não há sanitização genérica de qualquer objeto externo. Respostas legadas/auth podem ter somente `message` e um 404 de proxy/Express pode ser HTML. Veja [PUBLIC_CONTRACTS.md](PUBLIC_CONTRACTS.md).

| Código | Significado |
|---|---|
| `LOCAL_RUNTIME_ENV_INVALID` | modo local fora de development |
| `LOCAL_RUNTIME_PLATFORM_IDENTITY` | identidade de plataforma/Kubernetes presente |
| `LOCAL_RUNTIME_BIND_FORBIDDEN` | bind fora de loopback |
| `LOCAL_HOST_FORBIDDEN` / `LOCAL_ORIGIN_FORBIDDEN` | acesso de rede recusado |
| `LOCAL_PROXY_FORBIDDEN` | tentativa de proxy no modo local |
| `LOCAL_BOOTSTRAP_INVALID` | código ausente, reutilizado ou expirado |
| `LOCAL_SESSION_INVALID` | cookie ausente, inválido ou expirado |
| `LOCAL_CSRF_INVALID` | mutação sem prova CSRF |
| `LOCAL_ROLE_NOT_DECLARED` | perfil fora do manifesto |
| `LOCAL_OPERATION_NOT_SUPPORTED` | recurso exclusivo da plataforma |

Não faça branching por texto de mensagem; use `code`. Logs e respostas nunca devem conter token, cookie, credencial, senha ou conteúdo sensível.

---

<!-- source: EXECUTABLE_EXAMPLE.md -->

# Exemplo integrado e diagnóstico de autoria

Disponível na release 0.7.8. Gere a base oficial seguindo [a entrada curta](OON_APP_AGENT_GUIDE.md). Na raiz da base limpa, com gerador instalado:

```bash
npx --no-install create-central-oon example
npm run dev
```

O comando instala model/CRUD/lista de Pessoas, formulário com rota privada, Tickets com transição de processo e consulta externa HTTPS. Inclui página `/jornada`, item **Primeira jornada** no menu e permissões no manifesto. `FIRST_JOURNEY.md` acompanha os arquivos e explica a execução. O comando verifica colisões e composição original antes de escrever; não sobrescreve trabalho existente. A base neutra continua sendo o padrão e o exemplo é opcional.

Use admin para validar a jornada; viewer comprova 403 sem reconfigurar a Plataforma. O segredo de integração fica exclusivamente na variável backend `INTEGRACAO_TOKEN`; `INTEGRACAO_URL` deve ser um destino HTTPS controlado pelo operador, sem credenciais na URL. Não envie token pela UI, não versione `.env`, não salve segredo pelo CRUD genérico. A rota `/integracao/testar` não armazena credenciais. A jornada adicional `/segredos` usa core.secrets V1 conforme [SECRETS.md](SECRETS.md), com cadastro em objeto, estado, uso e remoção. Não há fila ou retry genéricos. A página permanece visível para demonstrar a recusa e exibir diagnóstico; a proteção efetiva está nos endpoints.

Pessoa usa escopo tenant explícito. Ticket declarativo é restrito a single_tenant dedicado devido ao limite atual de propagação de escopo do domain manifest. O exemplo não é contrato para compartilhar essa model entre tenants.

## Uma entrada de checks

```bash
npm run check
npm run build --prefix frontend
```

O novo scaffold usa `create-central-oon doctor` em `check`. Para um App anterior, substitua seu comando equivalente, preservando testes próprios. Doctor inclui:

- mesma versão instalada de backend/frontend/gerador e correspondência entre package.json e lockfile;
- lockfiles npm v2/v3 separados, ou lock único de workspace com backend/frontend declarados;
- App manifest, manifestos opcionais de domínio/processo e conformidade;
- cache oficial e hashes; corrija com `npm run ooncore:docs`;
- módulos TS/ESM não autocarregáveis, sintaxe CommonJS e imports relativos de diretórios de autoload que escapam de backend/;
- indicação de cwd e mapeamento `/api` público para rota interna, conforme configuração do scaffold.

Saída JSON contém códigos/caminhos e retorna exit code 1 quando houver pendências. Doctor não executa código do App, não resolve imports dinâmicos, não prova configurações de proxy modificadas e não substitui HTTP autenticado nem validação da imagem. Veja [empacotamento](APP_PACKAGING.md).

## Provas no SDK

A suíte gera o App pela base oficial e instala esses mesmos arquivos. Com o Core real, MongoDB descartável e servidor HTTPS de teste, verifica execução do handler, validação, CRUD persistido, transição permitida/recusada, sessão/CSRF, 401/403, chamada externa e ausência do segredo em respostas/requestLog. Reinicia em outro processo com a estrutura backend/ + central.app.json, confirma persistência e testa cwd absoluto, relativo e diretório de execução backend.

`npm run check:authoring` no monorepo valida o gerador e compila a UI gerada após o build frontend. A suíte backend é executada separadamente uma única vez pelo CI e contém a jornada HTTP. Essas provas não afirmam que uma release já foi publicada, que uma imagem foi homologada ou que o emissor já foi atualizado. O 404 do emissor requer sua própria prova funcional em Dev.

## Aplicação dos recursos nativos

A página `/recursos` do exemplo demonstra fórmulas, validações, bindings, invariantes, documentos, dashboard e PDF. O serviço de e-mail é opt-in. Consulte [NATIVE_RESOURCES.md](NATIVE_RESOURCES.md) para o roteiro, helpers de escopo e limites reais de isolamento, auditoria e execução.

---

<!-- source: FRONTEND_API.md -->

# API pública do `@oondemand/oon-core-front`

O contrato principal do frontend é code-first.

## Bootstrap

- `defineOonApp`: define identidade, API, rotas, navegação, shell, layouts, páginas, componentes e temas.
- `startOonApp`: valida e monta o App React.
- `defineOonRoutes`, `defineOonNavigation`: helpers tipados para composição local.

## Subpaths públicos

- `/ui`: primitives, padrões e componentes de domínio;
- `/routing`: rotas, navegação e helpers;
- `/theme`: temas, tokens e seleção em runtime;
- `/hooks`: hooks de autenticação, tenant, API e metadata;
- `/testing`: utilitários de teste.

## Segurança

- `useOonAuth`, `can`, `PermissionGate`, `Can`: permissões resolvidas pelo backend;
- `useOonTenant`, `createTenantStorage`: contexto tenant quando aplicável;
- `useOonApi`, `useOonResource`, `useCoreMetadata`, `useModelSchema`: acesso padronizado;
- rotas reservadas e guards obrigatórios pertencem ao Core.

## Domínio e UI

Views declarativas continuam disponíveis como composição opcional dentro do
objeto App. Componentes, páginas e layouts locais podem ser usados em qualquer
`appKind`. Consulte `FRONTEND_CODE_FIRST.md`.

---

<!-- source: FRONTEND_CODE_FIRST.md -->

# Frontend code-first

O frontend de todo App Oon é composto em TypeScript/React. O `appKind` não
limita páginas, componentes, layouts ou temas locais.

```tsx
import { defineOonApp, startOonApp } from "@oondemand/oon-core-front";
import { defineOonNavigation, defineOonRoutes } from "@oondemand/oon-core-front/routing";
import { HomePage } from "./pages/HomePage";

const routes = defineOonRoutes([{ path: "/", element: <HomePage /> }]);
const navigation = defineOonNavigation([{ id: "home", label: "Início", to: "/" }]);

startOonApp(defineOonApp({
  app: { id: "meu-app", name: "Meu App" },
  api: { baseUrl: import.meta.env.VITE_API_URL },
  routes,
  navigation,
}));
```

Rotas aceitam `element`, `component`, `lazy`, `layout`, `permissions` e
`capabilities`. Rotas de autenticação e estados de ativação são reservadas.

Use os subpaths públicos:

- `@oondemand/oon-core-front/ui` para primitives e padrões;
- `@oondemand/oon-core-front/routing` para rotas e navegação;
- `@oondemand/oon-core-front/theme` para temas;
- `@oondemand/oon-core-front/hooks` para hooks;
- `@oondemand/oon-core-front/testing` para testes.

Não carregue código remoto, não desative guards, não exponha segredos no bundle
e não importe arquivos internos do pacote. Rode `npm run ooncore:conformance`.

---

<!-- source: FRONTEND_PATTERNS.md -->

# Padrões Frontend

O frontend do App é code-first. Shell, providers e guards pertencem ao
`@oondemand/oon-core-front`; rotas, navegação, páginas, componentes, layouts e
temas são compostos localmente com as APIs públicas do Core.

Para o contrato completo, use `FRONTEND_CODE_FIRST.md`.
Para UX avançada com abas e itens relacionados, use também `ADVANCED_UX_PATTERNS.md` e `DETAIL_MODAL_AND_RELATED_GRIDS.md`.

## Estrutura esperada

```txt
frontend/
└── src/
    ├── main.tsx
    ├── app/{app,routes,navigation,theme}.tsx
    ├── pages/
    ├── components/
    ├── features/
    └── layouts/
```

## Composição

Use o objeto criado por `defineOonApp` para compor:

- menu;
- coleções;
- campos exibidos;
- filtros;
- ações;
- formulários;
- documentos;
- esteiras;
- dashboards;
- agrupamentos;
- layout v2;
- páginas por blocos;
- renderers por chave;
- modais de detalhe;
- abas;
- relações;
- grids relacionados;
- edição inline;
- ações por linha.

Views e blocos declarativos continuam opcionais para telas simples, dentro do
objeto code-first. Componentes React são registrados diretamente em TypeScript.

## Padrão de tela operacional

A tela principal de uma coleção operacional deve ser simples:

```txt
Título
Filtros
Busca
Botão novo
Grid principal
Ações por linha
```

Ela não deve acumular detalhe de filhos, formulários longos ou fluxos complexos abaixo do grid. Use `detailModal` para concentrar a operação do registro.

## Padrão de detalhe avançado

Quando a operação envolve um registro principal e seus relacionamentos, use:

```txt
CoreDetailModal
├── Resumo
├── Dados Principais
├── RelatedGrid editável
└── ReadonlyGrid
```

Exemplos:

- Projeto -> Itens -> Pagamentos
- Pedido -> Produtos -> Entregas
- Contrato -> Parcelas -> Documentos
- Cliente -> Atividades -> Histórico

## Formulários agrupados

Campos longos devem ser agrupados por sentido de negócio:

- Identificação;
- Evento/Faturamento;
- Equipe;
- Regras;
- Totais;
- Observações.

Prefira `form.groups` em vez de criar uma tela customizada apenas para organizar campos.

## Grids relacionados

Quando o usuário precisa operar filhos do registro principal, use `relatedGrid`.

Regras:

- Relação deve usar `foreignKey` + `parentKey`.
- Edição inline deve ser usada para ajustes rápidos de muitos itens.
- Ação por linha deve ser declarada como `rowActions`.
- A regra de negócio da ação fica no backend da Central.
- O Core deve executar e atualizar a interface.

## Regras

- Não recrie layout completo se o Core já renderiza.
- Não duplique chamada REST manual se o SDK do Core já atende.
- Não coloque regra de permissão apenas no frontend.
- Não hardcode endpoints quando a metadata puder fornecer.
- Não crie variações visuais fora do padrão sem necessidade real.
- Use overrides pequenos, específicos e documentados.
- Não crie página React customizada para resolver apenas: filtro, modal, abas, agrupamento de campos, grid relacionado ou ação por linha.

## Overrides

Overrides são permitidos para:

- campo especial;
- ação específica;
- card customizado;
- cabeçalho customizado;
- dashboard customizado;
- integração visual pontual;
- aba customizada dentro de `detailModal`.

Overrides não devem virar uma reimplementação do Core.

## Experiência padrão

A Central deve manter o padrão OonCore:

- navegação consistente;
- datagrids densos;
- formulários claros;
- feedback visual;
- status por badges;
- ações rastreáveis;
- responsividade;
- edição inline quando melhora a produtividade;
- detalhe em modal quando o registro possui relações operacionais.

## Contrato avançado implementado

Para telas mestre-detalhe, declare `detailModal` diretamente na coleção. A aba `form` salva o registro principal, `relatedGrid` busca filhos por `foreignKey=parent[parentKey]` e permite edição inline quando `editable: true` e `editMode: "inline"`, e `readonlyGrid` lista relações sem edição. Use `refresh` nas ações para coordenar recarga de `self`, `parent`, `all` ou abas específicas.

---

<!-- source: LOCAL_DEVELOPMENT.md -->

# Desenvolvimento local desconectado

## Início

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
npm install
npm run dev
```

O orquestrador inicia backend em `127.0.0.1:4000`, frontend em `127.0.0.1:5173`, gera códigos aleatórios e independentes para navegador e automação/seed, e abre o navegador. O Vite encaminha `/api` ao backend para manter cookies e CSRF na mesma origem.

O primeiro acesso troca o código de uso único por:

- cookie de sessão `HttpOnly`, `SameSite=Strict`;
- cookie CSRF de double-submit;
- sessão local cujo banco armazena somente hashes e expiração.

O prazo padrão é 30 dias. Reiniciar o processo rotaciona o segredo sem ampliar o prazo. Excluir o banco local cria um novo período; essa limitação é aceita na linha 0.5.

A decisão vem de `LocalExecutionPolicyProvider`. A fonte embarcada funciona offline e permite 30 dias. Uma fonte HTTP assinada poderá ser adicionada futuramente para novas emissões/renovações sem transformar a plataforma em dependência obrigatória.

## Perfis

O banner permite selecionar apenas papéis declarados em `central.app.json`. A permissão é recalculada no backend. Convites e usuários reais não são criados. Apps com tenant usam o contexto virtual fixo `local:tenant`, sem criar um tenant persistente ou aceitar um tenant arbitrário do cliente.

## Integrações

Use dublês ou credenciais explicitamente fornecidas no `.env` local do projeto. O Core não busca secrets da plataforma e não cria Deployment/binding/entitlement.

## Encerramento

`Ctrl+C` encerra os dois processos. Nunca use `--host 0.0.0.0`; conformance e startup devem reprovar essa configuração.

---

<!-- source: LOCAL_SECURITY_BOUNDARY.md -->

# Fronteira de segurança local

## Garantias

- bind real em loopback;
- Host e Origin limitados a `localhost`, `127.0.0.1` e `::1`;
- cabeçalhos de proxy recusados;
- códigos independentes de navegador e automação/seed, aleatórios, curtos e consumidos uma vez;
- segredo de sessão em cookie HttpOnly e somente hashes no banco;
- logout revoga a sessão no backend e invalida cookies anteriores;
- CSRF obrigatório nas mutações;
- nenhum bearer local no bundle ou `localStorage`;
- nenhuma identidade operacional ou chamada silenciosa à plataforma;
- `operationalRequestHeaders` falha com `LOCAL_OPERATION_NOT_SUPPORTED`;
- produção, Kubernetes e bind externo falham fechado.
- o contexto virtual `local:tenant` isola dados locais sem criar recurso na plataforma.

`Secure` é adicionado aos cookies quando `OON_LOCAL_HTTPS=true`; em HTTP loopback o cookie mantém `HttpOnly` e `SameSite=Strict`.

## Limitações explícitas

Quem controla código, banco e relógio locais pode reiniciar ou alterar o prazo. Os 30 dias são uma regra de experiência, não licenciamento inviolável. Uma política remota futura pode afetar novas emissões/renovações, mas não revoga imediatamente sessão offline já emitida.

O objetivo de segurança é impedir exposição da máquina/rede e impedir que identidade local escape para o Ecossistema.

---

<!-- source: METADATA_CRUD_UI.md -->

# Contrato ponta a ponta de metadata, CRUD e UI

1. `central.domain.json` ou `defineModel` registra model, campos, CRUD, roles e metadata.
2. O backend expõe `/core/metadata`, `/core/models` e o router CRUD do `basePath`.
3. Escopo de tenant/usuário, validação, fórmulas, referência, auditoria e triggers são aplicados no servidor.
4. O objeto code-first do App compõe coleções, formulários, filtros, relações, esteiras, documentos e dashboards.
5. O frontend consulta metadata e monta componentes do Core.

O CRUD padrão inclui listagem paginada, leitura, criação, atualização parcial, exclusão e import/export quando habilitados. Use rota customizada somente quando a operação não puder ser representada por CRUD, ação declarativa ou processo.

Campos calculados são exibidos reativamente no frontend e recalculados no backend. Campos de escopo são internos e imutáveis. Referências devem usar os filtros declarados; não faça consultas sem escopo.

---

<!-- source: NATIVE_RESOURCES.md -->

# Recursos nativos: usar por tarefa, com fronteiras claras

Release **0.7.8**. Esta é uma demonstração opcional, não uma migração obrigatória. Instale o exemplo em uma base limpa com `npx --no-install create-central-oon example`; abra **Primeira jornada** (`/jornada`) e **Recursos nativos** (`/recursos`). O App existente pode adotar somente a parte necessária. As fontes ficam em `examples/first-journey` do gerador instalado e são copiadas para o App; os testes do SDK executam esses mesmos arquivos com Core e MongoDB reais.

## O que usar e o que continua no App

| Necessidade | Recurso público demonstrado | Fronteira |
|---|---|---|
| Cadastro/lista/formulário | `defineModel`, `fields`, CRUD, metadata e `CoreCollection` | Regras de negócio são declaradas pelo App; não salvar segredos no CRUD genérico |
| Regras do próprio registro | `central.domain.json`: validações e `computed` | AST fechada; backend recalcula e recusa adulteração, prévia na UI não concede autoridade |
| Etapas e bloqueios | `central.process.json`: workflow; `CorePipeline` em `/jornada` | PATCH direto também precisa satisfazer a regra; esconder botão não protege dado |
| Valores relacionados | bindings `lookup`, `aggregate`, `expression` | Dependências e filtros devem estar declarados; não é sincronização com Omie |
| Limite concorrente | `relatedSumLteParentField` | Transação MongoDB exige replica set; protege mutações da model filha, não toda mudança arbitrária no pai |
| Documentos | `CoreDocument` com model `Documento` | Cadastro de textos; não promete upload, aprovação ou assinatura. Essas operações exigem contratos próprios |
| Indicadores | `CoreDashboard`: count, sum, groupCount | Agrega no backend; exemplo usa apenas models do banco single-tenant dedicado |
| UX específica | Página React local, `useOonApi`, componentes públicos | Composição code-first; não substituir shell, sessão, RBAC ou guards |
| Rota/dado autorizado | `defineRoutes`, `req.accessContext`, helpers de escopo | Contexto vem da autenticação; não de tenant/app/roles enviados livremente |
| Rastreabilidade | Auditoria do CRUD, `audit`, requestLog e `sensitiveBody` | Nenhum desses recursos cifra automaticamente os dados de domínio |
| PDF/e-mail | `capabilities.pdf.render`, `capabilities.transactionalEmail.send` | Capabilities existentes, declaradas/configuradas separadamente; não são fila genérica de integração |

## Roteiro de domínio e processo

Em **Contratos**, crie título `Exemplo`, quantidade `2`, valor unitário `50`. A metadata gera o formulário; o backend calcula `total=100`. A validação ilustrativa limita total a 1000. Enviar total adulterado pelo PATCH é recusado. A regra comercial e os valores são apenas didáticos.

Em **Parcelas**, selecione esse contrato e informe 40. O lookup preenche `tituloContrato`; o agregado atualiza `pago=40`; a expressão produz `saldo=60`. Renomeie o contrato enquanto aberto: o lookup é recalculado assincronamente. Reabra/atualize a lista para ver o estado persistido; não há promessa de push em tempo real.

Feche o contrato antes de continuar as parcelas. `lockedFieldsByStage` impede alterar título, quantidade e valor unitário; não é permitido voltar para Aberto. Uma parcela de 61 é recusada pela invariável. Duas requisições simultâneas de 40 disputando saldo 60 resultam em uma inclusão e uma recusa. A exclusão do contrato com parcelas também é bloqueada.

**Limite do exemplo:** a invariável está na model filha. Não garante que reduzir o total de um pai aberto preserve a soma anterior. A aplicação real precisa definir sua política para alteração/reabertura do pai; fechar o contrato estabiliza as entradas neste roteiro. O exemplo não é um módulo financeiro pronto.

`Contrato`, `Parcela` e `Ticket` são restritos ao App **single_tenant dedicado**: o domain manifest desta linha não propaga `scope`/`tenancy` para as models. Não adicionar campos inventados ao JSON nem adotar esses exemplos para isolamento de linhas multi-tenant. `Pessoa` e `Documento` usam `defineModel({ scope: "tenant" })` explicitamente.

O dashboard desta release aplica `crud.permissions.read` (com fallback legado de roles) e os helpers de escopo a todas as agregações. Models `legacy` continuam sem filtro de linha: a declaração correta do escopo permanece necessária. O exemplo demonstra Contrato no banco dedicado e a suíte comprova que Pessoa com escopo tenant não conta nem agrupa registros de outro tenant.

Referências sob demanda: [domínio](BACKEND_DOMAIN_MANIFEST.md), [fórmulas](REACTIVE_DOMAIN_FORMULAS.md), [processo](BACKEND_PROCESS_MANIFEST.md), [coleções/esteiras](COLLECTIONS_AND_PIPELINES.md).

## Rotas e helpers de escopo

O `defineModel` público devolve a entrada da model, com `definition` e `mongooseModel`. O exemplo exporta essa entrada de `src/models/Pessoa.js`. A rota `GET /recursos/pessoas/contagem` exige `pessoas.read` e usa:

```js
const { mergeScopedFilter } = require("@oondemand/oon-core-back");
const pessoa = require("../models/Pessoa");
// Dentro de um handler privado já autenticado/autorizado:
const filter = mergeScopedFilter(pessoa, {}, req.accessContext);
const total = await pessoa.mongooseModel.countDocuments(filter);
```

| Helper | Assinatura | Uso |
|---|---|---|
| `scopeFilter` | `(entryOrDefinition, accessContext)` | Filtro obrigatório de tenant/usuário |
| `mergeScopedFilter` | `(entryOrDefinition, filter, accessContext)` | Acrescenta escopo confiável a filtros de negócio permitidos |
| `scopedIdFilter` | `(entryOrDefinition, id, accessContext)` | Busca por ID dentro do escopo |
| `scopeMutation` | `(entryOrDefinition, data, accessContext)` | Impõe identidade confiável ao payload |

Os helpers não autenticam, não concedem permissão e não validam regras de domínio. Para `scope: "tenant"`, contexto sem tenant é recusado; `legacy`/`system` não produzem filtro de isolamento. Nunca repasse `req.query`/operadores Mongo arbitrários. `createAccessContext` estrutura uma identidade **já verificada**: não verifica um token nem autentica um body. Prefira `req.accessContext` nas rotas do App. Mutação direta pelo Mongoose não substitui o pipeline de validação, processo e auditoria do CRUD; a demonstração customizada é somente leitura.

## Auditoria e segredos

CRUD oficial registra mutações bem-sucedidas em `ControleAlteracao`. Rotas privadas customizadas podem declarar `audit: { entidade: "MinhaEntidade", acao: "alterado" }`; a auditoria captura dados da resposta. Isso não equivale a uma trilha imutável de todas as tentativas ou a um histórico completo antes/depois. Não inclua credenciais no resultado auditado.

`requestLog` registra requisições não-GET; `sensitiveBody: true` em mutações privadas omite corpo de entrada e resposta naquele log, inclusive nas recusas. Não cifra banco; não mascara console, URL, query string, cabeçalhos, logs de integração, auditoria nem mensagens de erro. GET não ganha proteção adicional com essa opção. A rota de PDF usa corpo sensível; o exemplo externo da Entrega 2 mantém segredo exclusivamente no ambiente backend. Persistência cifrada de credenciais é responsabilidade de um contrato disponível ou do App. [Contrato completo](PUBLIC_CONTRACTS.md).

## PDF e e-mail sem infraestrutura paralela

A página PDF chama `POST /recursos/pdf`, exige `pdf.render` e utiliza `capabilities.pdf.render(input, context)` com contexto autorizado, correlação e cancelamento. Sem capability resolvida retorna `PDF_RENDERING_UNAVAILABLE`. Para usar no ambiente publicado, acrescente a declaração de `oon.deploy.json` conforme [PDF_RENDERING.md](PDF_RENDERING.md); não configure endpoint/credencial de infraestrutura no App. O teste injeta transporte de PDF apenas no processo de teste, nunca no exemplo distribuído.

E-mail é **opt-in separado**, para não enviar mensagens nem exigir configuração ao iniciar o exemplo. O serviço `backend/src/services/confirmacao.js` demonstra o contrato público. Chame-o de uma ação privada autorizada depois de resolver destinatário e evento de negócio no backend. A chave `eventId` deve ser estável na repetição da mesma operação; não gere uma nova chave a cada retry. O resultado `accepted`/`duplicate` indica aceite, não entrega.

Para habilitar, preserve o manifesto e adicione `core.transactional-email` ao array `capabilities`, com estas configurações:

```json
{
  "capabilitySettings": {
    "core.transactional-email": {
      "enabled": true,
      "scopePolicy": "tenant_override",
      "retentionDays": 30,
      "attachmentsPolicy": { "allowed": false },
      "templates": [{ "code": "confirmacao", "definition": "./backend/emails/confirmacao.json", "initialStatus": "active" }]
    }
  }
}
```

O caminho acima parte do `central.app.json` na raiz e aponta para o asset já instalado **dentro de backend/**, que acompanha o empacotamento. Se o manifesto ficar dentro de backend, use `./emails/confirmacao.json`. Configure o provedor no painel `CoreTransactionalEmail`, registrando página, menu e as permissões necessárias conforme [TRANSACTIONAL_EMAIL.md](TRANSACTIONAL_EMAIL.md). Não ponha credenciais em JSON. Sem declaração o serviço recusa com `EMAIL_CAPABILITY_NOT_DECLARED`; sem configuração não há garantia de envio. Não habilite envio real em testes.

## Limites de execução

`recalculate: "async"` e `drainProcessJobs()` atendem recálculos do processo; a fila interna não é um contrato público durável de enqueue/claim/retry. A fila transacional de e-mail é específica de e-mail. Integrações Omie, mapeamentos fiscais, idempotência de efeitos externos, tickets e recuperação de negócio continuam no App ou em biblioteca de domínio compatível. Novas Capacidades têm acompanhamento independente e não bloqueiam a POC.

## Evidências e aceite local

`check:authoring` gera a base, instala o exemplo, sincroniza/verifica o cache oficial e valida typecheck/build. A jornada HTTP do backend cobre fórmulas, adulteração, validação, lookup, agregado, recálculo assíncrono, transição/bloqueio, exclusão protegida, concorrência transacional, metadata, dashboard, escopo da consulta própria, auditoria, 401/403 e PDF indisponível/transport de teste. E-mail sem declaração falha fechado; a suíte própria da capability cobre envio/idempotência com dublês. Nenhum teste envia e-mail real. Build, release npm, publicação e homologação do App são estados distintos.

---

<!-- source: OON_APP_AGENT_GUIDE.md -->

# Criar e customizar um Oon App com um Agent

Roteiro da release **0.7.8**. Comece por uma jornada pequena: uma pessoa abre uma página, executa uma ação e vê o resultado ou um erro útil. A árvore gerada e suas referências públicas devem ser suficientes.

## 1. Gerar

```bash
npx --yes --package @oondemand/create-central-oon@0.7.8 create-central-oon meu-app --no-install
cd meu-app
npm install
npm install --prefix backend
npm install --prefix frontend
```

Use sempre o gerador oficial. Preserve o `AGENTS.md` próprio do projeto. Não copie outro App como base.

## 2. Executar

Requer Node compatível com os pacotes instalados e MongoDB local disponível. Configure `MONGO_URI` no arquivo abaixo para um banco de desenvolvimento.

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
npm run dev
```

O comando inicia back/front em loopback e abre uma sessão técnica local. Não é necessário cadastrar o App na Plataforma para essa execução. PDF e outras operações de plataforma podem falhar fechado; detalhes sob demanda em [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md).

## 3. Implementar a primeira jornada

Escolha uma intenção em [TASK_INDEX.md](TASK_INDEX.md). Para começar com página + ação + endpoint, use o exemplo de [PUBLIC_CONTRACTS.md](PUBLIC_CONTRACTS.md). Ajuste o domínio em `backend/src`, a experiência em `frontend/src` e as permissões em `central.app.json`.

Não antecipe lista completa de funcionalidades, múltiplos épicos ou matriz final de perfis. Para uma POC controlada, use o admin já declarado e mantenha as verificações de backend. Registre próximas funções em um backlog curto.

Se faltar informação, registre a lacuna, use extensão pública adequada no App e continue o que for independente. Não invente assinatura, leia internals como contrato ou remova controles de acesso para avançar.

## 4. Validar

```bash
npm run check
npm run build --prefix frontend
```

`check` executa doctor, que reúne versões, lockfiles, manifestos, docs check e conformance; não é necessário repeti-los. Execute testes do App quando houver script e os testes relevantes da jornada. O scaffold neutro não cria `npm test` na raiz.

Prove ação, resultado e erro pela UI/API; para mutações, confirme persistência e acesso indevido recusado. Teste local não comprova integração externa nem publicação. `context.generated.md` fica disponível apenas para referência, sem leitura integral obrigatória.

## 5. Publicar e validar em Dev

Versione código, manifestos, lockfiles e o cache `.ooncore`. Publique pelo fluxo já existente do Workspace/Plataforma e confira a jornada pelo endereço público autenticado de Dev. Registre o commit publicado e o resultado. Consulte [APP_PACKAGING.md](APP_PACKAGING.md) somente para detalhes de empacotamento.

Identidade, tenancy, licenciamento, publicação e promoção são serviços homologados consumidos pelo App. Não os reimplemente nem reabra sua homologação global. Necessidade de nova Capacidade é um escopo separado. Build aprovado, publicado e homologado são estados distintos.

---

<!-- source: OONCORE_ARCHITECTURE.md -->

# Arquitetura OonCore

O OonCore é a base para criar Centrais operacionais sob demanda com arquitetura padronizada, segura e evolutiva.

A Central gerada não deve nascer como um sistema completo do zero. Ela deve nascer como uma camada de domínio que consome os recursos do Core.

## Separação de responsabilidades

```txt
Central
├── backend/   domínio, regras, validações, integrações e esteiras
└── frontend/  declaração de telas, coleções, documentos e overrides

OonCore Back
├── boot Express
├── Mongo/Mongoose
├── autenticação
├── RBAC
├── CRUD metadata-driven
├── auditoria
├── triggers/hooks
└── APIs padrão

OonCore Front
├── shell React
├── providers
├── roteamento
├── menu
├── datagrid
├── formulários
├── documentos
├── esteiras
└── SDK REST
```

## Modelo mini-monolítico

Cada Central começa como um mini-monolito de negócio: pequeno, coeso, isolado e capaz de entregar valor rapidamente. Quando uma parte do domínio se tornar reutilizável, crítica ou independente, ela pode evoluir para conector, serviço compartilhado ou micro-serviço.

## Fonte de verdade

- Dados e regras ficam no backend.
- Metadata operacional é exposta pelo backend.
- Frontend renderiza a experiência a partir da metadata.
- Permissões são decididas no backend.
- Integrações são tratadas como conectores, mappings, triggers e esteiras de integração.

## Objetivo dos Agents

O Agent deve acelerar a construção da Central usando a arquitetura existente. O objetivo não é gerar um app genérico, mas completar a camada de domínio com segurança e aderência ao Core.

---

<!-- source: PDF_RENDERING.md -->

# Renderização de PDF

Use esta capability para transformar HTML em um `Buffer` PDF sem conhecer endpoint, credencial ou implementação do serviço. Requer OonCore `0.6.0` ou superior.

## Declaração

Declare a dependência de infraestrutura em `oon.deploy.json`:

```json
{
  "capabilities": {
    "pdfRendering": {
      "required": true,
      "minVersion": "1.0.0"
    }
  }
}
```

Não adicione URL, usuário, senha ou implementation reference. O runtime resolve esses valores na publicação. Esta declaração não pertence ao array `capabilities` de `central.app.json`.

## API pública do backend

```js
const {
  capabilities,
  defineRoutes,
  GenericError,
} = require("@oondemand/oon-core-back");

defineRoutes("/pdf", (router) => {
  router.private.post(
    "/render",
    { permission: "pdf.render" },
    async (req, res) => {
      if (typeof req.body?.html !== "string" || !req.body.html.trim()) {
        throw new GenericError("Informe o HTML.", {
          statusCode: 422,
          code: "PDF_HTML_REQUIRED",
        });
      }

      const controller = new AbortController();
      const abort = () => controller.abort();
      req.once("aborted", abort);
      res.once("close", abort);

      try {
        const pdf = await capabilities.pdf.render(
          {
            html: req.body.html,
            format: req.body.format || "A4",
            printBackground: true,
          },
          {
            ...req.accessContext,
            correlationId: req.correlationId,
            environment: process.env.APP_ENVIRONMENT,
            signal: controller.signal,
          },
        );

        res.type("application/pdf");
        res.set("Content-Disposition", 'attachment; filename="documento.pdf"');
        res.send(pdf);
      } finally {
        req.off("aborted", abort);
        res.off("close", abort);
      }
    },
  );
});
```

Declare `pdf.render` em `rbac.permissions` e conceda-a somente aos papéis necessários. O backend continua sendo a autoridade de permissão e tenant.

A assinatura é:

```ts
capabilities.pdf.render(input, context): Promise<Buffer>
```

| Campo de `input` | Tipo | Regra/default |
|---|---|---|
| `html` | string | obrigatório; máximo padrão de 2 MiB |
| `format` | `A3 \| A4 \| A5 \| Letter \| Legal` | `A4` |
| `landscape` | boolean | `false` |
| `marginTop`, `marginBottom`, `marginLeft`, `marginRight` | number | polegadas, de 0 a 4; `0.39` |
| `printBackground` | boolean | `true` |
| `timeoutMs` | number | mínimo 1.000 ms; padrão 30.000 ms; máximo do runtime, padrão 60.000 ms |

O `context` pode carregar `tenantId`, `appCode`, `environment`, `operationId`, `correlationId`/`requestId`, `signal` e, somente em testes, `fetchImpl`. A saída deve começar com `%PDF-` e tem limite padrão de 20 MiB.

## Preview e download no frontend

Preview do HTML deve usar iframe sem privilégios:

```tsx
<iframe title="Prévia" sandbox="" srcDoc={html} />
```

Para gerar e baixar usando o cliente autenticado do Core:

```tsx
import { useOonApi } from "@oondemand/oon-core-front";

function DownloadPdfButton({ html }: { html: string }) {
  const { http } = useOonApi();

  async function download() {
    const response = await http.post(
      "/pdf/render",
      { html, format: "A4" },
      { responseType: "blob" },
    );
    const url = URL.createObjectURL(response.data);
    const link = document.createElement("a");
    link.href = url;
    link.download = "documento.pdf";
    link.click();
    URL.revokeObjectURL(url);
  }

  return <button onClick={download}>Gerar PDF</button>;
}
```

Nunca envie a geração diretamente a um endpoint de infraestrutura pelo navegador.

## Erros

`PdfRenderingError` expõe `code`, `statusCode`, `retryable` e detalhes sanitizados.

| Código | Retry | Significado |
|---|---:|---|
| `PDF_RENDERING_INVALID_INPUT` | não | HTML vazio ou acima do limite |
| `PDF_RENDERING_INVALID_OPTIONS` | não | formato, margem ou opção inválida |
| `PDF_RENDERING_UNAVAILABLE` | sim | capability não resolvida no ambiente |
| `PDF_RENDERING_CREDENTIAL_UNAVAILABLE` | sim | credencial interna não injetada |
| `PDF_RENDERING_IMPLEMENTATION_ERROR` | sim | implementação respondeu com falha |
| `PDF_RENDERING_TIMEOUT` | sim | prazo excedido ou sinal abortado |
| `PDF_RENDERING_SATURATED` | sim | concorrência/fila excedida |
| `PDF_RENDERING_TRANSPORT_ERROR` | sim | falha transitória de transporte |
| `PDF_RENDERING_INVALID_OUTPUT` | sim | saída inválida ou acima do limite |

Use retentativas apenas quando `error.retryable === true`, com backoff e idempotência na operação chamadora.

## Segurança e runtime local

- trate HTML do usuário como não confiável; sanitize no App e use interpolação escapada;
- prefira HTML autocontido; recursos remotos tornam o resultado não determinístico e podem ser bloqueados;
- nunca inclua segredos, tokens ou credenciais no HTML;
- não registre HTML nem bytes do PDF; registre correlação, duração, tamanhos e código de erro;
- propague cancelamento do request por `AbortSignal`;
- no runtime local, a capability falha fechado com `PDF_RENDERING_UNAVAILABLE` quando não resolvida;
- em testes automatizados, um transport fake pode ser injetado por `capabilities.configurePdfRendering` e deve devolver bytes iniciados por `%PDF-`; não gere um “PDF” textual falso no código do App.

---

<!-- source: PORTAL_COCKPIT_PATTERNS.md -->

# Portais e cockpits code-first

Portais e cockpits usam o mesmo contrato de frontend dos demais Apps. Defina o
App com `defineOonApp`, componha rotas com `defineOonRoutes` e inicialize com
`startOonApp`.

Use páginas locais para jornadas transversais e components do Core para
autenticação, autorização, tenant, shell, estados e acesso HTTP. O `appKind` não
cria uma exceção arquitetural nem restringe customização local.

Para jornadas multi-tenant, passe o tenant específico da operação ao cliente
HTTP. A seleção visual nunca substitui a autorização do backend.

Consulte `FRONTEND_CODE_FIRST.md`, `FRONTEND_API.md` e `RBAC_SECURITY.md`.

---

<!-- source: PUBLIC_CONTRACTS.md -->

# Contratos públicos para a primeira jornada

Piso verificado: OonCore 0.7.4. Imports backend vêm de `@oondemand/oon-core-back`; frontend de `@oondemand/oon-core-front` e seus subpaths públicos. [Índice](TASK_INDEX.md) e [API completa](BACKEND_API.md).

## Bootstrap e prefixos

- `npm run dev` na raiz usa o orquestrador oficial; `npm start --prefix backend` usa o CLI com o diretório do backend.
- No bootstrap programático, `await start({ cwd: caminhoAbsolutoDoBackend, listen: false })` devolve `{ app }`; com escuta, devolve `{ app, server }`. `createApp()` monta o Express a partir do registro existente, mas não carrega o domínio nem conecta o banco sozinho.
- `cwd` determina `central.config.js`, `central.domain.json`, `central.process.json` e `src/`. O App manifest é descoberto no backend ou em seu diretório pai.
- São autocarregados recursivamente arquivos `.js`/`.cjs` de `src/models`, `validations`, `triggers`, `routes`, `pipelines`, `documents` e `hooks`. Serviços e assets entram pelos imports dessas extensões. Não é preciso exportar uma função de registro: execute `defineRoutes` no módulo carregado.
- O bootstrap carrega domínio/processo antes dos módulos JS. Models usadas em um process manifest devem existir no domain manifest. Não duplique sua definição em JS.

| Camada | Exemplo da mesma operação |
|---|---|
| Registro no backend | `defineRoutes("/demo", ...)` + `router.private.post("/saudacao", options, handler)` |
| Backend direto | `POST /demo/saudacao` |
| URL pública / proxy Vite | `POST /api/demo/saudacao` |
| `useOonApi` com baseUrl `/api` | `http.post("/demo/saudacao", body)` |

O proxy existente remove `/api`; não registre esse prefixo novamente nem o duplique na chamada do cliente. Preserve a configuração fornecida pelo scaffold/delivery. Para diferenças entre checkout e imagem, consulte [APP_PACKAGING.md](APP_PACKAGING.md).

## Rotas privadas

```js
const { defineRoutes } = require("@oondemand/oon-core-back");

defineRoutes("/integracao", (router) => {
  router.private.put("/credencial", {
    permission: "integracao.config.write",
    sensitiveBody: true,
  }, async (req, res) => {
    // Neste exemplo de assinatura, nenhuma credencial é persistida.
    res.status(501).json({ message: "Implemente a persistência cifrada no App." });
  });
});
```

Assinatura: `router.private[METHOD](path, options, handler)`, com `get`, `post`, `put`, `patch`, `delete`. Há forma curta `(path, handler)`, porém ela não declara uma permissão de negócio; prefira opções explícitas.

- `permission: "dominio.acao"` é a forma recomendada. `permissions: ["a.read", "b.read"]` aceita **qualquer uma** das permissões; não significa exigir todas. Evite declarar ambos.
- `roles` é compatibilidade legada, não uma substituição da política RBAC declarada.
- `audit` configura auditoria de mutação quando necessária; não coloque dados secretos nela.
- **Não** passe `requirePermission(...)` como segundo argumento e o handler como terceiro. Antes da validação introduzida nesta entrega, uma função nessa posição era interpretada como o próprio handler, descartando o terceiro argumento. Na release 0.7.8, essa assinatura lança OON_ROUTE_REGISTRATION_INVALID no registro. O wrapper não é a assinatura variádica do Express. `requirePermission` é um middleware público para composições compatíveis, não uma opção de `router.private`.
- `router.public` não deve ser usado para evitar autenticação de uma operação privada.

Declare a permissão em `central.app.json` → `rbac.permissions` (array de strings) e conceda-a em `rbac.roles[].permissions`. Preserve os demais campos/papéis. O admin do scaffold já tem `permissions: ["*"]`; isso não dispensa a declaração de permissões nem o contexto autorizado no backend. Operações com dados próprios devem usar `req.accessContext` e os helpers de escopo documentados em [BACKEND_API.md](BACKEND_API.md).

## Corpo sensível e erros

`sensitiveBody: true` em `post`, `put`, `patch` ou `delete` privado omite entrada e resposta no `requestLog` para o método/caminho, inclusive em erro. Não cifra banco, não mascara seletivamente campos, não cobre automaticamente CRUD, GET, console, logs de integração, auditoria ou payload de exceções. Credenciais pertencem a um armazenamento protegido do App ou a um contrato público disponível na release; nunca ao frontend/manifesto/URL.

Lance `new GenericError(mensagemSegura, { statusCode, code, details })`. O envelope de domínio com `code` é:

```json
{
  "message": "Informe um nome de até 80 caracteres.",
  "error": {
    "code": "DEMO_NAME_INVALID",
    "message": "Informe um nome de até 80 caracteres.",
    "requestId": "correlacao-quando-disponivel"
  }
}
```

`details` e `requestId` são opcionais. O Core não sanitiza arbitrariamente o conteúdo que o App coloca em `message`/`details`; normalize erros externos antes de lançá-los. Respostas legadas e recusas de auth podem conter somente `message`; 404 do proxy/Express pode ser HTML. Não trate erro de rede/404 como sucesso vazio. Veja [ERRORS.md](ERRORS.md).

## Primeira jornada executável

No App gerado, adicione `"demo.execute"` a `rbac.permissions`. Mantenha o admin existente. Crie `backend/src/routes/demo.js`:

```js
const { defineRoutes, GenericError } = require("@oondemand/oon-core-back");

defineRoutes("/demo", (router) => {
  router.private.post("/saudacao", { permission: "demo.execute" }, async (req, res) => {
    const nome = typeof req.body?.nome === "string" ? req.body.nome.trim() : "";
    if (!nome || nome.length > 80) {
      throw new GenericError("Informe um nome de até 80 caracteres.", {
        statusCode: 422, code: "DEMO_NAME_INVALID",
      });
    }
    res.json({ message: `Olá, ${nome}!` });
  });
});
```

Substitua `frontend/src/pages/HomePage.tsx`. A rota `/` e o item Início já são registrados pelo scaffold:

```tsx
import { useState, type FormEvent } from "react";
import { useOonApi } from "@oondemand/oon-core-front";

export function HomePage() {
  const { http } = useOonApi();
  const [nome, setNome] = useState("");
  const [resultado, setResultado] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    try {
      const response = await http.post("/demo/saudacao", { nome });
      setResultado(response.data.message);
    } catch (error: unknown) {
      const response = (error as { response?: { status?: number; data?: {
        message?: string; error?: { code?: string; message?: string };
      } } }).response;
      setResultado(response?.data?.error?.message || response?.data?.message
        || `Não foi possível executar a ação (HTTP ${response?.status ?? "indisponível"}).`);
    } finally { setBusy(false); }
  }
  return <form onSubmit={submit}>
    <h1>Primeira jornada</h1>
    <label>Nome <input value={nome} onChange={event => setNome(event.target.value)} /></label>
    <button type="submit" disabled={busy}>Executar</button>
    <p role="status">{resultado}</p>
  </form>;
}
```

Reinicie `npm run dev` após incluir o módulo, abra Início com admin e execute com nome válido e vazio (422). Selecione viewer, sem `demo.execute`, e confirme a recusa (403). O cliente do Core cuida de sessão e CSRF; não crie token fixo. A saudação é uma ação sem persistência; para um cadastro, siga [TASK_EXAMPLES.md](TASK_EXAMPLES.md). Estes blocos são exemplos documentais copiáveis, não uma suíte integrada de homologação do SDK.


A release 0.7.8 também diagnostica a raiz do App passada como cwd com OON_BACKEND_CWD_INVALID. Caminhos relativos são resolvidos antes do autoload. Use `create-central-oon example` em uma base limpa para instalar a jornada integrada descrita em [EXECUTABLE_EXAMPLE.md](EXECUTABLE_EXAMPLE.md).

---

<!-- source: RBAC_SECURITY.md -->

# RBAC e Segurança

A segurança da Central deve ser aplicada no backend. O frontend pode ocultar ou exibir ações, mas não é a fonte de decisão.

## Regras obrigatórias

- Toda operação sensível deve validar usuário autenticado.
- Toda alteração de dados deve validar permissão.
- Toda ação de integração deve validar permissão e contexto.
- Nunca confiar em `tenantId`, `appId`, `perfil` ou `roles` enviados livremente pelo frontend.
- Segredos devem vir de variáveis de ambiente ou vault equivalente.
- Logs não devem expor tokens, senhas, app keys ou dados sensíveis desnecessários.

## RBAC

Use o RBAC do Core para:

- controlar acesso por app;
- controlar perfis;
- controlar ações;
- filtrar funcionalidades;
- proteger rotas;
- permitir evolução de permissões sem reconstruir telas.

## Catálogo canônico de perfis

```http
GET /core/role-catalog
```

Resposta:

```json
{
  "schemaVersion": 1,
  "appCode": "central-compras",
  "enabled": true,
  "roles": [
    {
      "code": "viewer",
      "name": "Consulta",
      "description": "Somente leitura.",
      "admin": false
    }
  ]
}
```

Use esse endpoint para montar seletores e validar grants por App. Não mantenha códigos de perfil paralelos no frontend ou no Control Plane. O consumidor deve validar versão e App, bloquear redirects e destinos de rede privados, revalidar o perfil no backend e tratar catálogo inválido como indisponível. O endpoint usa cache público de cinco minutos. Desde 0.7.1, pode incluir `commercialPermissions` com permissões funcionais declaradas; não publica wildcards literais nem namespaces operacionais reservados. Esse catálogo não concede autorização; a decisão efetiva continua no App.

## Checklist de segurança para Agents

Antes de concluir uma alteração, confirme:

- Existe validação de entrada?
- Existe validação de permissão no backend?
- Existe tratamento de erro?
- A operação gera rastreabilidade?
- Algum segredo foi colocado no código?
- Algum dado sensível foi exposto no frontend?
- O comportamento funciona para múltiplos usuários e múltiplos apps?

---

<!-- source: REACTIVE_DOMAIN_FORMULAS.md -->

# Fórmulas reativas nos formulários OonCore

A partir do contrato declarativo de domínio, campos com `computed` são recalculados imediatamente nos formulários padrão do `@oondemand/oon-core-front`.

O App não precisa repetir a fórmula no frontend nem criar componentes React específicos. A declaração continua existindo uma única vez no `central.domain.json` do backend.

## Fluxo

1. O backend carrega e valida o `central.domain.json`.
2. A metadata da model expõe `readonly` e `computed`.
3. O frontend interpreta a mesma AST fechada para apresentar uma prévia imediata.
4. Campos calculados e readonly são removidos do payload enviado pelo formulário.
5. O backend recalcula novamente, executa as validações e persiste o valor autoritativo.
6. Depois da resposta, o formulário passa a exibir o registro devolvido pelo servidor.

> O cálculo no navegador melhora a experiência do usuário. Ele nunca substitui o cálculo, a proteção readonly ou a validação do backend.

## Formulários atendidos

- formulário dinâmico de coleções (`DynamicForm`);
- formulário principal em modal com abas (`CoreTabbedDetail`);
- criação e edição;
- formulários derivados integralmente da metadata;
- formulários com apresentação local, desde que a model continue sendo carregada pela metadata do Core.

## Exemplo

A declaração permanece somente no domínio:

```json
{
  "subtotal": {
    "kind": "currency",
    "computed": {
      "precision": 2,
      "expression": {
        "op": "multiply",
        "args": [
          { "field": "quantidade" },
          { "field": "diarias" },
          { "field": "valorUnitario" }
        ]
      }
    }
  }
}
```

Ao alterar quantidade, diárias ou valor unitário, o campo subtotal é atualizado na tela. Ao salvar, subtotal não é enviado pelo cliente: o backend calcula novamente e devolve o valor persistido.

## Paridade da AST

O frontend suporta o mesmo vocabulário do backend:

- aritméticos: `add`, `subtract`, `multiply`, `divide`, `min`, `max`, `abs`, `negate`, `coalesce`;
- comparação: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`;
- lógicos e presença: `and`, `or`, `not`, `present`, `in`;
- nós de valor: `{ "value": ... }`;
- referências: `{ "field": "nomeDoCampo" }`.

Os testes de caracterização usam cadeias financeiras equivalentes às do backend para reduzir o risco de divergência sem permitir execução de JavaScript arbitrário no navegador.

## Tratamento de erros

Erros de prévia, como divisão por zero ou valor não numérico, aparecem associados ao campo calculado. O usuário pode corrigir as entradas imediatamente.

A decisão final continua no backend, que retorna `DomainRuleError` com status 422 quando a mutação viola o contrato.

## Extensões locais

Não crie funções de cálculo em componentes da Central para campos já descritos por `computed`.

Use código local apenas quando a regra:

- não puder ser representada pela AST;
- depender de consulta externa;
- exigir agregação de registros relacionados;
- ainda não possuir contrato declarativo no OonCore.

Nesses casos, mantenha o backend como fonte de verdade e registre a lacuna para evolução do Core.

---

<!-- source: releases/0.3.41.md -->

# OonCore 0.3.41 — Manifesto declarativo de domínio

Versão destinada à homologação do primeiro contrato declarativo completo de domínio no backend.

## Recursos incluídos

- carregamento automático de `central.domain.json`;
- declaração versionada de models e campos;
- validação estrutural agregada;
- fórmulas declarativas sem execução de JavaScript arbitrário;
- campos calculados no servidor;
- ordenação de dependências e detecção de ciclos;
- proteção de campos `readonly` em criação, atualização e importação;
- validações declarativas entre campos;
- atualização parcial com consolidação e recálculo;
- compatibilidade com `defineValidation` durante a migração gradual.

## Objetivo da homologação

Validar o contrato em uma Central de teste antes da conversão dos models e regras da SS-Eventos.

A homologação deve confirmar:

1. criação e carregamento do manifesto;
2. geração de metadata e CRUD;
3. recálculo de campos em `POST`, `PUT` e `PATCH`;
4. rejeição de adulteração em campos controlados pelo servidor;
5. mensagens de validação associadas ao campo correto;
6. compatibilidade com models e validações JavaScript ainda não migrados.

## Fora do escopo

- fórmulas reativas no frontend;
- índices compostos;
- triggers e transições declarativas;
- engine genérica de integrações;
- migração da SS-Eventos.

---

<!-- source: releases/0.5.0.md -->

# OonCore 0.5.0

## Mudança principal

Runtime de desenvolvimento local desconectado, com sessão automática por até 30 dias, loopback obrigatório e documentação canônica distribuída para IA/Agents.

## Migração obrigatória

- alinhar back, front e create-central em `0.5.x`;
- usar `OON_RUNTIME_MODE=local` apenas com `NODE_ENV=development`;
- remover `DEV_TOKEN`, `VITE_DEV_TOKEN` e o valor `dev-local`;
- usar Vite em `127.0.0.1` com proxy `/api`;
- sincronizar `.ooncore/` e preservar o `AGENTS.md` raiz;
- usar o código dedicado de automação para seed, preservando o bootstrap do navegador;
- atualizar compatibilidade do App para `>=0.5.0 <0.6.0` após homologação.

## Segurança

Local não emite nem reutiliza identidade operacional. Rotas de plataforma são bloqueadas; cookies/CSRF substituem bearer local. Apps com tenant usam apenas `local:tenant`. Reiniciar processos não renova uma sessão expirada; reset do banco reinicia o prazo e permanece uma limitação conhecida.

O manifesto documental inclui hash dos documentos e dos entrypoints gerados (`AGENTS.md`, `CODEX.md` e `context.generated.md`).

## Compatibilidade

`DEV_TOKEN` explícito permanece temporariamente apenas para testes/CI legados fora de `OON_RUNTIME_MODE=local`; novos scaffolds não o geram.

---

<!-- source: releases/0.6.0.md -->

# OonCore 0.6.0

A linha 0.6 substitui o bootstrap orientado a manifesto por uma API pública code-first, preservando a governança da Plataforma Oon.

## Destaques

- bootstrap com `defineOonApp` e `startOonApp`;
- rotas, menus, páginas, componentes e temas tipados;
- scaffold único e neutro em `_base`;
- `central.app.json` schema v2;
- remoção integral dos templates selecionáveis, Omie e provider genérico de integrações;
- resolução de capabilities técnicas pela Plataforma Oon, sem expor detalhes de implementação aos Apps;
- documentação distribuída atualizada para desenvolvimento assistido por Agents.

## Upgrade

- alinhe `@oondemand/oon-core-back`, `@oondemand/oon-core-front` e `@oondemand/create-central-oon` na linha `0.6.x`;
- declare compatibilidade `>=0.6.0 <0.7.0`;
- migre o frontend para `defineOonApp`/`startOonApp`;
- remova flags e módulos legados;
- execute docs check, conformance, typecheck, testes e smoke offline antes da publicação.

A versão 0.6 é incompatível com os contratos removidos da linha 0.5.

---

<!-- source: releases/0.7.0.md -->

# OonCore 0.7.0 — Novo Ecossistema Oon

Esta linha é o marco de compatibilidade com a identidade operacional por deployment e a autorização comercial single-tenant do novo ecossistema.

Atualize Core Back, Core Front e create-central-oon juntos. Declare compatibilidade `>=0.7.0 <0.8.0` após validar a migração e sincronize `.ooncore`.

A abertura por `oon_launch` valida a nova sessão antes de persistir token e tenant. Seleção anterior não acompanha o handshake; logout ou login posterior cancelam a troca pendente. A Central continua sendo a autoridade para tenant, licença, grant, ambiente e deployment.

Nenhuma regra de licenciamento deve ser implementada no domínio do App. Após atualizar as dependências, execute docs check, conformance, typecheck e testes; publique e homologue o runtime consumidor com a Central compatível. A atualização do pacote não publica nem migra automaticamente Apps.

---

<!-- source: ROUTES_HOOKS_WORKERS.md -->

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

---

<!-- source: RUNTIME_MODES.md -->

# Modos de runtime

| Contrato | `local` | `platform` |
|---|---|---|
| Configuração | `NODE_ENV=development`, `OON_RUNTIME_MODE=local` | ambiente publicado |
| Bind | somente loopback | contrato da infraestrutura |
| Identidade | principal técnico local | usuário/tenant/Deployment reais |
| Ativação | `ativa_local` | estados da plataforma |
| Sessão | cookie HttpOnly, TTL de até 30 dias | auth/SSO configurado |
| RBAC | simula somente papéis do manifesto | acessos reais |
| Plataforma | nenhuma chamada obrigatória | conforme capability |
| Publicar/promover | bloqueado | por contratos autorizados |

`local` não é o ambiente publicado `desenvolvimento`. Ele não possui `deploymentId`, `instanceId`, `bindingId`, `entitlementId`, licença ou credencial operacional.

O Core falha no startup local quando encontra produção, Kubernetes, identidade operacional, bind não-loopback ou `PUBLIC_APP_URL` externa.

---

<!-- source: SECRETS.md -->

# core.secrets V1

Contrato público a partir da release 0.7.6. Backend: `const { capabilities } = require("@oondemand/oon-core-back")`. Exclusivo para `single_tenant` + `dedicated`. Nenhum endpoint/CRUD automático expõe a coleção técnica. Adoção é opt-in; não migra e-mail nem Apps existentes.

```json
{
  "capabilities": ["core.secrets"],
  "capabilitySettings": { "core.secrets": { "enabled": true } }
}
```

Mescle a declaração no manifesto existente. Nunca coloque valores ou chave em manifesto, frontend, repositório ou imagem. O Publisher transmite somente a declaração. Core e executor precisam da release com V1; versão anterior deve recusar a publicação opt-in.

```js
const options = { name: "omie", context: req.accessContext, correlationId: crypto.randomUUID() };
await capabilities.secrets.put({ ...options, value: { appKey, appSecret } });
const state = await capabilities.secrets.status(options);
await capabilities.secrets.use(options, async credential => {
  // Serviço do App controla URL, timeout, redirects e sanitização do retorno.
  await omie.call(credential);
});
await capabilities.secrets.remove(options);
```

`context` é o contexto autorizado do Core; nunca copie identidade do body/header. Rotas do App exigem autenticação, permissão de negócio e `sensitiveBody: true`. A V1 verifica App, tenant e usuário; a autorização da operação é da rota. Não oferece execução anônima/sistema nem contorno de RBAC.

- Nome: `[a-z][a-z0-9._-]{0,63}`, definido pelo backend. Dois nomes são independentes.
- Valor: objeto JSON não vazio, até 16 KiB serializado. Substituição atômica do objeto inteiro; não há merge parcial, histórico ou compare-and-swap. Última gravação concluída prevalece.
- `put` retorna apenas `{state:"available"}`; valor incompatível exige `replace: true` explícito. Chave indisponível impede gravação inclusive com replace.
- `status` retorna `absent`, `available` ou `reentry_required`. `reason:key_unavailable`/`action:restore_provisioning` exige intervenção antes do recadastro; `incompatible_or_unreadable`/`replace` permite substituição autorizada. Erro de banco retorna erro sanitizado, nunca “ausente”.
- `use(options, callback)` aguarda o callback e **descarta seu retorno**. Erros do callback tornam-se `SECRETS_USE_FAILED`, sem mensagem/cause externa. Código do App deve decidir quais resultados sanitizados expor.
- `remove` é idempotente e não precisa decifrar o valor.
- Correlação opcional: 1–128 caracteres alfanuméricos, `:`, `_` ou `-`; gere no backend. Auditoria técnica registra tentativa de operação, ator, escopo, nome, correlação e instante, sem valor/envelope/chave. Não é confirmação transacional do efeito.

AES-256-GCM, chave aleatória de 32 bytes, IV novo de 12 bytes por gravação. Envelope v1 autenticado com AAD que inclui App, identidade canônica do runtime dedicado (appId + namespace), ambiente, tenant e nome. Uma chave por namespace/ambiente. As coleções `oon_secrets` e `oon_secret_audit` são técnicas, não registradas em CRUD/metadata/export.

`use` não é sandbox: código consumidor pode copiar/logar strings ou exfiltrá-las. Nunca registre payload, headers, erros de SDK externo ou resposta remota sem sanitização. Limpeza dos buffers não garante apagar todas as cópias de strings do heap. A criptografia protege valores em repouso separados da chave; um processo backend comprometido pode acessar os valores.

## Provisionamento e recadastro

O helper de delivery cria Secret imutável `oon-core-secrets` por `create` atômico; concorrentes releem o vencedor. Erro de leitura não gera chave. A chave não passa em argumentos CLI, logs, contexto de publicação ou evidência. `secretKeyRef` monta somente OON_SECRETS_KEY do ambiente alvo, opcional para permitir que funções independentes iniciem mesmo se a chave desaparecer. Campos extras de um Secret restaurado não são injetados. Identidade/tenant não secretos permanecem no runtime base; nenhuma operação de segredo ignora a falta da chave. Um Secret marcador imutável `oon-core-secrets-initialized` guarda apenas o vínculo público e impede recriação silenciosa se a chave desaparecer. Não há serviço de cofre. O RBAC do Publisher recebe somente leitura nominal dos dois Secrets; criação de Secrets já existe.

Republicação, reinício e réplica reutilizam Secret/coleção. Promoção transporta declaração/imagem; provisiona chave independente no destino, sem copiar dados ou chave da origem.

1. Para valor incompatível com chave íntegra: usuário autorizado informa o objeto completo e confirma `replace: true`.
2. Se a chave estiver ausente: operador restaura o Secret correspondente, sem imprimir/exportar sua chave para diagnósticos. O provisionamento normal recusa perda ou corrupção.
3. Sem chave recuperável: operador interrompe o runtime alvo, confirma identidade/ambiente e aceita a perda dos valores antigos. Remove **somente** o Secret e marcador daquele ambiente por procedimento operacional autorizado e reexecuta provisionamento. Depois republica/reinicia todas as réplicas e solicita recadastro explícito. Não há endpoint do App para trocar chave.
4. Exclusão do namespace/ambiente ou restauração de banco sem a chave correspondente pode exigir recadastro. Não há recuperação, rotação ou migração transparente nesta V1.

## Prova gerada e desenvolvimento local

`create-central-oon sample --no-install` seguido de `create-central-oon example` instala `/segredos`, menu, permissão `segredos.manage` e rotas públicas do SDK. O exemplo opt-in já declara a capacidade. Configure no **ambiente do backend**, persistindo de forma segura entre reinícios: `OON_SECRETS_KEY` (32 bytes base64 padrão), `OON_SECRETS_INSTANCE=local:sample`, `OON_SECRETS_TENANT=local:tenant`, `APP_ENVIRONMENT=desenvolvimento`. Nunca use a chave local na Plataforma.

`INTEGRACAO_URL` é endpoint HTTPS controlado pelo operador, que receberá POST do objeto de prova; não é implementação fiscal/Omie. Sem chave, outras páginas continuam operacionais. Use credenciais sintéticas no teste. A suíte HTTP gera o App, usa Core/Mongo reais e HTTPS de teste, cobre autorização, dois nomes, cifra, adulteração, recadastro, concorrência, erros/logs e reinício empacotado. Isso não substitui release npm nem homologação Dev pública.

---

<!-- source: TASK_EXAMPLES.md -->

# Exemplos por tarefa

Piso verificado: 0.7.4. Execute no App gerado seguindo [o roteiro](OON_APP_AGENT_GUIDE.md). Estes exemplos são blocos copiáveis para as tarefas; a suíte integrada e o exemplo instalável estão descritos em [EXECUTABLE_EXAMPLE.md](EXECUTABLE_EXAMPLE.md). Preserve o manifesto existente e acrescente apenas os campos indicados.

## Cadastro e lista

Adicione `pessoas.read` e `pessoas.write` a `rbac.permissions` de `central.app.json`; use admin na POC. Crie `backend/src/models/Pessoa.js`:

```js
const { defineModel, fields } = require("@oondemand/oon-core-back");

defineModel({
  name: "Pessoa", singular: "pessoa", basePath: "/pessoas", scope: "tenant",
  schema: { nome: fields.string({ required: true, label: "Nome" }) },
  crud: { enabled: true, permissions: { read: "pessoas.read", write: "pessoas.write" } },
});
```

Substitua `frontend/src/pages/HomePage.tsx`; a rota e o menu Início existentes tornam o cadastro acessível:

```tsx
import { CoreCollection } from "@oondemand/oon-core-front";

export function HomePage() {
  return <CoreCollection model="Pessoa" label="Pessoas" endpoint="/pessoas" />;
}
```

Reinicie `npm run dev`. Em Início, crie uma pessoa, consulte a lista e recarregue para confirmar persistência. Nome ausente deve ser recusado; viewer sem as permissões não pode ler/gravar. O formulário é derivado da metadata. Não use esse CRUD para armazenar segredos: `sensitiveBody` de rota customizada não é aplicado aqui.

## Esteira

Restrito ao App `single_tenant` com banco dedicado gerado pelo scaffold. O domain manifest desta versão não propaga `scope`/`tenancy` para a model: não use este exemplo como isolamento de linhas multi-tenant. Registre essa lacuna se precisar combinar processo declarativo com esse escopo; não invente campos de manifesto. Para cadastro com isolamento explícito, use `defineModel({ scope: "tenant", ... })` do exemplo anterior.

Este exemplo independente usa `backend/central.domain.json` (não crie outra model `Ticket` em JS):

```json
{
  "schemaVersion": 1, "name": "Exemplo de tickets",
  "models": [{
    "name": "Ticket", "singular": "ticket", "basePath": "/tickets",
    "crud": { "enabled": true, "permissions": { "read": "tickets.read", "write": "tickets.write" } },
    "fields": {
      "titulo": { "kind": "string", "required": true },
      "etapa": { "kind": "enum", "values": ["Aberto", "Concluido"], "default": "Aberto" }
    }
  }]
}
```

Crie `backend/central.process.json`:

```json
{
  "schemaVersion": 1,
  "models": {
    "Ticket": { "workflow": {
      "stageField": "etapa", "initialStages": ["Aberto"], "defaultStage": "Aberto",
      "transitions": [{ "from": "Aberto", "to": "Concluido" }]
    } }
  }
}
```

Declare `tickets.read` e `tickets.write` em `rbac.permissions` e use admin. Substitua `frontend/src/pages/HomePage.tsx`:

```tsx
import { CorePipeline } from "@oondemand/oon-core-front";

export function HomePage() {
  return <CorePipeline model="Ticket" label="Tickets" endpoint="/tickets"
    titleField="titulo" stageField="etapa" create={{ enabled: true, defaultStage: "Aberto" }}
    defaultActions={{ workStatus: false }}
    stages={[{ id: "Aberto", label: "Aberto" }, { id: "Concluido", label: "Concluído" }]} />;
}
```

Reinicie, crie um ticket em Aberto e mova para Concluído; o retorno para Aberto deve ser recusado pelo backend. A esteira não executa chamadas externas automaticamente. Consulte [BACKEND_PROCESS_MANIFEST.md](BACKEND_PROCESS_MANIFEST.md) para bindings/invariantes.

## Integração

Não existe contrato genérico de “integration runtime” nesta release. Uma consulta externa pode usar uma rota privada e um serviço no App. Para executar o exemplo, configure `INTEGRACAO_URL` (endpoint HTTPS controlado por você) e `INTEGRACAO_TOKEN` no ambiente do backend; nunca versione o token. Ele usa Bearer, portanto adapte o mapeamento ao contrato do sistema externo.

Crie `backend/src/routes/integracao.js` e declare `integracao.test` em `rbac.permissions`:

```js
const { defineRoutes, GenericError } = require("@oondemand/oon-core-back");

defineRoutes("/integracao", (router) => {
  router.private.post("/testar", { permission: "integracao.test", sensitiveBody: true }, async (req, res) => {
    const url = process.env.INTEGRACAO_URL;
    const token = process.env.INTEGRACAO_TOKEN;
    if (!url || !token) throw new GenericError("Configure a integração.", {
      statusCode: 409, code: "INTEGRATION_NOT_CONFIGURED",
    });
    let target;
    try { target = new URL(url); } catch { /* tratado abaixo */ }
    if (!target || target.protocol !== "https:" || target.username || target.password) {
      throw new GenericError("Configure um endpoint HTTPS sem credenciais na URL.", {
        statusCode: 422, code: "INTEGRATION_URL_INVALID",
      });
    }
    let response;
    try {
      response = await fetch(target, {
        headers: { Authorization: `Bearer ${token}` },
        signal: AbortSignal.timeout(10000), redirect: "error",
      });
    } catch {
      throw new GenericError("O serviço externo não respondeu no prazo ou está indisponível.", {
        statusCode: 502, code: "INTEGRATION_TRANSPORT_ERROR",
      });
    }
    await response.body?.cancel();
    if (!response.ok) throw new GenericError("O serviço externo recusou a consulta.", {
      statusCode: 502, code: "INTEGRATION_REMOTE_REJECTED", details: { remoteStatus: response.status },
    });
    res.json({ message: "Consulta externa concluída." });
  });
});
```

Para uma página utilizável, reutilize o `HomePage` de [PUBLIC_CONTRACTS.md](PUBLIC_CONTRACTS.md) e troque a chamada por `http.post("/integracao/testar", {})`; o input nome pode ser removido. Reinicie e teste sucesso, configuração ausente e rejeição externa. O exemplo apenas consulta: não cadastra credenciais, não comprova uma operação fiscal nem oferece retry/persistência de jobs. Credenciais recebidas pela UI exigem armazenamento cifrado próprio e respostas sanitizadas.

## Diagnóstico

Após publicar, consulte (substitua o host pelo endereço real de Dev):

```bash
curl --fail-with-body https://SEU-APP-DEV/api/health/ready
curl --fail-with-body https://SEU-APP-DEV/api/health/version
```

Para uma ação privada, reproduza pela página com `useOonApi` autenticado e registre método, caminho, status, código e correlação sem segredos. Confira se `/api` foi acrescentado apenas na URL pública, se o módulo está em `backend/src/routes` e se o commit é o publicado. HTML 404 indica investigar rota/proxy/empacotamento; não é prova de rejeição da API externa. Readiness não prova execução do handler de domínio.

---

<!-- source: TASK_INDEX.md -->

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

---

<!-- source: TESTING_CONFORMANCE.md -->

# Testes e conformidade

## App consumidor

```bash
npm run check
npm run build --prefix frontend
```

No scaffold, `check` executa `doctor`, que inclui docs check e conformance, versões instaladas, lockfiles e diagnóstico de composição. Rode também os testes relevantes declarados pelo App; a base neutra não cria um script raiz `test`. Prove a jornada com acesso permitido/recusado, validação de entrada, resultado e persistência quando aplicável. Não duplique verificações sem uma mudança ou risco concreto.

A homologação global da Plataforma e os testes de segurança do runtime pertencem ao SDK/Plataforma. O App preserva os contratos e comprova sua integração específica. Se alterar uma fronteira de segurança, cubra explicitamente essa mudança.

## Manutenção do SDK

Alterações no runtime exigem as provas pertinentes: loopback, sessão/CSRF, expiração, perfis, isolamento, recusa de identidade operacional local e ausência de chamadas à Plataforma. Esses cenários não são pré-requisito repetido para cada página de um App.

## Documentação distribuída

`create-central-oon docs check` valida fonte, versão, schema, entrada, hashes e arquivos. `docs sync` regenera o cache a partir da fonte do pacote. O tarball deve conter docs, templates e schemas. Verifique links e exemplos alterados; build, publicação e homologação são evidências diferentes.


No monorepo, `npm run check:authoring` executa os testes do gerador uma vez e verifica typecheck/build da base com o exemplo integrado. Execute após o build do SDK frontend. A suíte backend inclui HTTP real e MongoDB descartável para a mesma jornada; não simula router. No CI essas entradas substituem os checks duplicados.

---

<!-- source: TRANSACTIONAL_EMAIL.md -->

# E-mail transacional

A capability `core.transactional-email` fornece configuração protegida, templates versionados, preview, envio idempotente, fila, retentativas e painel administrativo. Requer OonCore `0.6.0` ou superior.

## Declaração funcional

Em `central.app.json`:

```json
{
  "capabilities": ["core.transactional-email"],
  "capabilitySettings": {
    "core.transactional-email": {
      "enabled": true,
      "scopePolicy": "tenant_override",
      "retentionDays": 30,
      "attachmentsPolicy": { "allowed": false },
      "templates": [
        {
          "code": "confirmacao",
          "definition": "./emails/confirmacao.json",
          "initialStatus": "active"
        }
      ]
    }
  }
}
```

`scopePolicy` aceita `app_only`, `tenant_required` ou `tenant_override`. `retentionDays` aceita 1 a 90. Nesta linha do Core, anexos não são permitidos.

A definição referenciada contém:

```json
{
  "code": "confirmacao",
  "name": "Confirmação",
  "subject": "Olá, {{nome}}",
  "htmlContent": "<p>Olá, {{nome}}.</p>",
  "textContent": "Olá, {{nome}}.",
  "variablesSchema": {
    "type": "object",
    "additionalProperties": false,
    "required": ["nome"],
    "properties": { "nome": { "type": "string" } }
  },
  "locale": "pt-BR",
  "initialStatus": "active",
  "attachmentsPolicy": { "allowed": false }
}
```

Templates usam somente interpolação Handlebars escapada. Blocos, helpers, subexpressões, triple-stache e conteúdo remoto executável não são aceitos.

## Envio no backend

```js
const { capabilities } = require("@oondemand/oon-core-back");

async function enviarConfirmacao({ email, nome, idempotencyKey }, req) {
  return capabilities.transactionalEmail.send(
    {
      templateCode: "confirmacao",
      to: email,
      variables: { nome },
      idempotencyKey,
      correlationId: req.correlationId,
      maxAttempts: 5,
    },
    {
      ...req.accessContext,
      userId: req.accessContext?.userId,
    },
  );
}
```

`idempotencyKey` é obrigatória. O retorno é `{ dispatchId, status, correlationId }`; `status` é `accepted` ou `duplicate`. Não trate `accepted` como entrega confirmada.

Outras operações públicas do namespace `capabilities.transactionalEmail` incluem preview e versionamento de templates, consulta de dispatches e retry de dead letter. Para administração interativa, prefira o componente do Core.

## Painel administrativo

```tsx
import { CoreTransactionalEmail } from "@oondemand/oon-core-front";

export function EmailPage() {
  return <CoreTransactionalEmail />;
}
```

Proteja a rota e declare/conceda apenas as permissões necessárias:

- `transactional-email.config.read`
- `transactional-email.config.manage`
- `transactional-email.templates.read`
- `transactional-email.templates.manage`
- `transactional-email.dispatches.read`
- `transactional-email.dispatches.retry`

O componente usa as rotas autenticadas em `/core/transactional-email/*`. Credenciais são inseridas pela tela protegida e armazenadas pelo Core; nunca as coloque no manifesto, frontend, repositório ou log.

## Segurança e operação

- o backend resolve app e tenant a partir do contexto validado;
- `tenant_required` exige tenant; `tenant_override` usa configuração do tenant quando houver e recua para a do App;
- destinatários e variáveis são validados antes de enfileirar;
- payload protegido tem retenção limitada; listagens não retornam o payload protegido;
- erros usam `TransactionalEmailError` e códigos `EMAIL_*` sanitizados;
- no runtime local, falhe fechado até a capability e seu secret store/configuração estarem disponíveis;
- testes devem substituir a fronteira externa; não envie e-mail real e não grave credenciais de teste.

---

<!-- source: TROUBLESHOOTING.md -->

# Troubleshooting

| Sintoma | Verificação | Correção |
|---|---|---|
| `LOCAL_RUNTIME_ENV_INVALID` | `NODE_ENV` | use `development` |
| bind proibido | `HOST`, Vite `server.host` | use `127.0.0.1` |
| bootstrap inválido | URL antiga/reutilizada | reinicie `npm run dev` e use a nova URL |
| 401 local | cookie apagado/expirado | abra a URL de bootstrap atual |
| `LOCAL_SESSION_EXPIRED` no startup | prazo local de 30 dias encerrado | exclua os dados locais para iniciar o período aceito na linha 0.5 |
| seed invalida o navegador | código incorreto usado no script | use exclusivamente o código **Automação/seed** |
| 403 CSRF | frontend não está na mesma origem/proxy | use `/api` pelo proxy Vite |
| docs desatualizados | versão/hash | `npm run ooncore:docs` |
| perfil ausente | `central.app.json.rbac.roles` | declare o papel e sincronize/reinicie |
| operação de plataforma bloqueada | código `LOCAL_OPERATION_NOT_SUPPORTED` | use dublê/credencial local ou homologue publicado |
| Mongo indisponível | `MONGO_URI`, replica set quando exigido | inicie Mongo local conforme o projeto |
| porta ocupada | 4000/5173 | encerre processo conflitante; não exponha outra interface |

Nunca resolva erro local adicionando token fixo, `0.0.0.0`, proxy externo ou credencial de Deployment.
