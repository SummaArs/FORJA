# Stack 100% gratuita

## Núcleo

| Necessidade | Ferramenta |
|---|---|
| Código | Python, Node.js ou TypeScript |
| Banco local | SQLite |
| Versionamento | Git |
| Repositório | GitHub Free |
| Testes | unittest, pytest opcional, Vitest/Jest quando necessário |
| CI | GitHub Actions no limite gratuito |
| API local | Python stdlib, FastAPI opcional |
| Dados locais | CSV, JSON, SQLite |
| Container local | Docker opcional |

## IA gratuita ou local

- **Gemini CLI**: agente terminal com cota gratuita pessoal publicada pelo fornecedor; confirme limites atuais antes de depender deles.
- **Aider**: interface Git-first conectável a APIs gratuitas, OpenRouter e modelos locais.
- **OpenCode**: agente open source com múltiplos provedores e modelos locais.
- **Ollama**: servidor local para modelos open-weight; custo monetário zero, mas exige hardware e energia próprios.
- **Modelos locais**: úteis para documentação, testes, refactors e tarefas repetitivas; não presumir que igualem modelos de fronteira em arquitetura difícil.

## Estratégia econômica

1. usar modelo gratuito para exploração e tarefas pequenas;
2. usar modelo local para dados sensíveis e trabalho repetitivo;
3. usar um modelo mais forte apenas para decisões arquiteturais e debugging difícil;
4. sempre executar testes localmente;
5. nunca deixar a IA declarar sucesso sem o comando de prova;
6. limitar escopo por branch e commit.

## Regra de custo zero

“Gratuito” nesta FORJA significa **sem comprar APIs, hospedagem ou licença para reproduzir o tutorial**. Isso não promete que toda cota externa será eterna, nem elimina custo de energia, internet ou hardware do computador.
