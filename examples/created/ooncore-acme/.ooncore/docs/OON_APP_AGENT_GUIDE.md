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

