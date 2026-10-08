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
