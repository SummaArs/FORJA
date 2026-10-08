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
