# FORJA como companheira do Claude Code

## Problema

Um agente de código desperdiça contexto quando recebe o repositório inteiro: dependências, builds, caches, documentação irrelevante e arquivos fora da tarefa. Isso aumenta custo, latência e chance de decisões ruins.

## Solução

A FORJA funciona como uma camada anterior ao agente:

```text
pedido humano
  ↓
seleção lexical de arquivos relevantes
  ↓
limite de contexto
  ↓
estado Git e regras de trabalho
  ↓
CLAUDE_CONTEXT.md
  ↓
Claude Code ou outro agente
  ↓
./prove.sh
```

## Uso

```bash
PYTHONPATH=. python3 -m forja_core companheiro \
  "corrigir o fluxo de pagamentos e adicionar testes" \
  --repo ./meu-projeto \
  --out ./meu-projeto/.forja/companion
```

Depois, no Claude Code, abra o repositório e peça para ler:

```text
Leia .forja/companion/CLAUDE_CONTEXT.md. Trabalhe somente com a tarefa descrita, inspecione dependências quando necessário e execute a prova do projeto antes de concluir.
```

## Estratégias

- seleção por termos da tarefa;
- priorização de README, contratos, testes e código-fonte;
- exclusão de `.git`, `node_modules`, builds e caches;
- orçamento explícito de contexto;
- fingerprint para saber se o pacote mudou;
- estado Git incluído;
- instrução de prova obrigatória;
- nenhum envio automático de código para a nuvem.

## Métrica

A FORJA registra:

- tamanho estimado do repositório em caracteres;
- tamanho incluído;
- redução estimada;
- arquivos selecionados;
- fingerprint do pacote.

Essa redução é uma estimativa de entrada, não uma contagem oficial de tokens do Claude. A contagem real depende do tokenizer e das mensagens do agente.

## Limite honesto

A FORJA não torna automaticamente um modelo gratuito tão capaz quanto Claude Code. Ela reduz contexto irrelevante, melhora o handoff e obriga a prova. É uma camada de engenharia de contexto e verificação, não um modelo de linguagem.
