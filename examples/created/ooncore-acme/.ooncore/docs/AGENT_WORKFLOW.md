# Fluxo de trabalho para Agents

1. Gere a base oficial e execute: [OON_APP_AGENT_GUIDE.md](OON_APP_AGENT_GUIDE.md).
2. Escolha a jornada e consulte somente a intenção em [TASK_INDEX.md](TASK_INDEX.md).
3. Implemente domínio e experiência pelos contratos públicos, preservando permissões, contexto e segredos.
4. Valide com `npm run check`, build e testes relevantes disponíveis; prove a jornada.
5. Publique pelo fluxo existente e registre commit e evidência em Dev.

A documentação desta release é 0.7.8, linha 0.7.x. Para coordenar os três pacotes, consulte [CORE_UPGRADE.md](CORE_UPGRADE.md).

Se faltar assinatura, declaração, exemplo ou limite, registre a lacuna e continue partes independentes com extensões públicas documentadas no App. Apenas a operação sem contrato seguro fica pendente. Nunca use internals como API, invente contratos ou crie autoridade de autenticação/RBAC paralela.

Não exija leitura integral do contexto consolidado, planejamento completo nem homologação global da Plataforma para começar. Consulte referências detalhadas sob demanda.
