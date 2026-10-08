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
