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
