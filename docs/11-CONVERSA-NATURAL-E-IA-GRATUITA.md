# Conversa natural e IA gratuita

## Começar sem script

```bash
PYTHONPATH=. python3 -m forja_core conversar
```

A FORJA faz seis perguntas em linguagem comum:

1. Como chamar o sistema?
2. Que problema ele resolve?
3. Quem vai usar?
4. O que precisa ser guardado?
5. O que as pessoas precisam fazer?
6. Há dinheiro, saúde, segurança ou outra parte importante?

Você responde como fala normalmente. Não precisa escrever JSON, código ou comando.

No fim, a FORJA mostra o que entendeu e pergunta **“Está certo?”**. Só cria arquivos depois de você responder `sim`.

## O que é criado

- `requirements.json`: interpretação estruturada da conversa;
- `CONVERSA.md`: memória legível das respostas;
- `blueprint/`: rotas, domínio, governança e aceitação;
- `forja/`: identidade e manifesto do projeto.

## Provedores gratuitos

A FORJA detecta, sem instalar ou fingir que existe:

- Ollama: IA local, sem custo por requisição;
- Gemini CLI: opção de cota gratuita, sujeita aos limites da conta;
- Aider: agente de terminal, dependendo do modelo escolhido;
- OpenCode: agente de terminal, dependendo do modelo escolhido.

Exemplo explícito:

```bash
PYTHONPATH=. python3 -m forja_core conversar --provider ollama
```

Se nenhum estiver instalado, a FORJA usa o assistente determinístico local. Nesse modo não há custo, login, envio de dados ou dependência externa.

## Estratégia contra dependência

A IA não é a autoridade. Ela pode ajudar a resumir, sugerir código e explicar erros, mas a FORJA permanece responsável por:

- validar o contrato;
- bloquear campos ausentes;
- separar frontend e backend;
- exigir autorização;
- exigir controles para alto risco;
- executar testes;
- registrar o que não foi provado.

## Limite honesto

A FORJA não é automaticamente equivalente ao Claude Code em capacidade de modelo. Claude Code é um produto de agente com modelos de alta capacidade. A FORJA compete em outra camada: fluxo guiado, contratos, reprodutibilidade, escolha de provedores gratuitos e gates de qualidade.

Para competir em execução, a evolução é usar um modelo local ou gratuito detectado pela FORJA, mas nunca declarar qualidade do modelo sem benchmark e nunca enviar código privado sem autorização.
