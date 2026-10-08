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
