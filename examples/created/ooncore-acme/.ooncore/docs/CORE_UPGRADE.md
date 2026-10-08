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
