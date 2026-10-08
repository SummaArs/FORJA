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
