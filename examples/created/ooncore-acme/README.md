# Ooncore Acme

App Oon code-first gerado com `create-central-oon`. Comece pela entrada curta `.ooncore/AGENTS.md` e pelo roteiro `.ooncore/docs/OON_APP_AGENT_GUIDE.md`; escolha referências em `.ooncore/docs/TASK_INDEX.md` conforme a tarefa. Não é necessário ler o contexto consolidado nem fonte privada.

## Executar

Requer Node compatível com os pacotes e MongoDB local. Ajuste `MONGO_URI` para um banco de desenvolvimento.

```bash
npm install
npm install --prefix backend
npm install --prefix frontend
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
npm run dev
```

O runtime local funciona em loopback com sessão técnica; não cadastra recursos na Plataforma. Capabilities dependentes da Plataforma falham fechado quando indisponíveis.

## Entregar a primeira jornada

Implemente página, navegação, endpoint e permissão usando `.ooncore/docs/PUBLIC_CONTRACTS.md`. Domínio fica em `backend/src`; `backend/central.domain.json` é opcional. Composição de UX fica em `frontend/src/app` e `frontend/src/pages`. `central.app.json` declara identidade e acesso; `oon.deploy.json` declara requisitos de publicação.

```bash
npm run check
npm run build --prefix frontend
```

`check` inclui cache documental e conformance. Execute os testes relevantes quando declarados; a base neutra não contém script raiz `test`. Prove a jornada, versione código/manifestos/lockfiles/cache e publique pelo fluxo existente do Workspace/Plataforma. Registre o commit e a validação autenticada em Dev. Build, publicação e homologação são estados distintos.

Lacuna documental: registre, use extensão pública adequada no App e continue as partes independentes; não invente APIs nem remova autenticação, autorização ou isolamento. POC não exige roadmap completo nem matriz final de perfis. Não reimplemente nem homologue novamente os serviços já homologados da Plataforma.

`.ooncore/` é cache gerado: atualize a fonte do pacote e use `npm run ooncore:docs`; nunca edite manualmente. Upgrade coordenado está em `.ooncore/docs/CORE_UPGRADE.md`.
