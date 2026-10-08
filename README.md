# FORJA

## Criar e operar qualquer artefato empresarial com lógica, provas e custo zero

A **FORJA** é um sistema operacional de criação empresarial. Ela começou como um método para criar software confiável e agora governa qualquer artefato que possa sustentar uma decisão: software, processo, produto, documento, política, operação, análise, experimento ou decisão.

Ela transforma uma ideia em um resultado que pode responder, com evidência:

- o que o software afirma;
- o que pode dar errado;
- como a falha é detectada;
- como o sistema evita duplicidade;
- como ele recupera depois de cair;
- como outra pessoa reproduz a prova;
- o que ainda **não** foi verificado.

O mesmo contrato serve para um sistema financeiro, um processo de atendimento, um produto de diagnóstico, uma política de aprovação, uma migração, um relatório ou um experimento.

> **A FORJA não promete que toda IA gratuita substitui um engenheiro. Ela cria um processo que impede que a IA esconda incerteza.**

## O exemplo incluído

Este repositório constrói do zero o **Forja Ledger**, uma pequena central de lançamentos empresariais:

```text
evento de origem → validação → gravação idempotente → auditoria → reconciliação
```

Ele não usa API paga, banco pago, framework pago ou dependência externa. Usa somente:

- Python 3.11+;
- SQLite incluído no Python;
- biblioteca padrão;
- Git e GitHub;
- qualquer agente gratuito opcional.

O exemplo demonstra:

- valores em centavos inteiros;
- chave idempotente por intenção;
- transação atômica;
- trilha de auditoria;
- falha fechada para dados inválidos;
- reconciliação contra a fonte de origem;
- testes adversariais;
- simulação de queda antes e depois do commit.

## Comece em três comandos

```bash
python3 -m unittest discover -s tests -v
./prove.sh
python3 -m forja_ledger demo
```

Para criar um sistema novo com uma frase:

```bash
PYTHONPATH=. python3 -m forja_core new "Minha Loja" --target ooncore
```

A FORJA cria a pasta, os requisitos e uma primeira planta verificável. Depois você só abre `requirements.json` e explica o que o sistema deve fazer.

## Criar conversando

Se você não quer escrever script ou JSON, use:

```bash
PYTHONPATH=. python3 -m forja_core conversar
```

A FORJA fará perguntas em português, aceitará respostas naturais, mostrará o que entendeu e só criará o projeto depois da sua confirmação. Ela procura ferramentas gratuitas como Ollama, Gemini CLI, Aider e OpenCode; se nenhuma estiver disponível, usa um assistente local determinístico sem enviar dados.

## Resultado esperado

```text
FORJA PROOF: PASS
checks=42 violations=0
```

## Os cinco passos da FORJA

1. **Definir** — escrever o problema, as afirmações materiais e a definição de pronto.
2. **Modelar** — transformar a operação em estados, invariantes e contratos.
3. **Forjar** — implementar o menor sistema que pode ser provado.
4. **Atacar** — plantar defeitos, simular queda, duplicidade, atraso e dados inválidos.
5. **Reconferir** — comparar o resultado com a fonte da verdade, publicar limites e só então evoluir.

## Enterprise OS

```bash
PYTHONPATH=. python3 -m forja_core check examples/enterprise-portfolio.json
```

O manifesto universal bloqueia artefatos validados sem evidência e artefatos de alto risco sem gatilho de reabertura. Veja [FORJA Enterprise OS](docs/07-ENTERPRISE-OS.md).

## Uso natural

Para começar um cliente novo sem decorar a arquitetura:

```bash
PYTHONPATH=. python3 -m forja_core init ./cliente-acme --name "Acme" --owner Gustavo
```

Para conectar um OonCore existente, a FORJA aceita um caminho local ou URL e faz apenas descoberta de leitura:

```bash
PYTHONPATH=. python3 -m forja_core connect --workspace ./cliente-acme --repo /caminho/para/ooncore --name ooncore
```

Veja o [guia natural e OonCore](docs/08-USO-NATURAL-E-OONCORE.md). O repositório correto do OonCore ainda precisa ser informado; a FORJA não inventa origem, versão ou permissões.

## Criar de verdade: três destinos

```bash
PYTHONPATH=. python3 -m forja_core create local ./cliente --name "Cliente" --apply
PYTHONPATH=. python3 -m forja_core create ooncore ./cliente-central --name "Cliente Central" --apply
PYTHONPATH=. python3 -m forja_core create odoo ./addons/cliente --name "Cliente" --apply
```

Sem `--apply`, a FORJA apenas mostra o plano. Consulte [os adaptadores Local, OonCore e Odoo](docs/09-ADAPTADORES-LOCAL-OONCORE-ODOO.md).

## Compilar um sistema empresarial

A FORJA também compila uma especificação de negócio em contratos de frontend, backend, governança e aceitação:

```bash
PYTHONPATH=. python3 -m forja_core blueprint \
  examples/enterprise-spec-receivables.json \
  examples/generated/receivables --apply
```

Veja [Blueprint empresarial e prova](docs/10-BLUEPRINT-EMPRESARIAL-E-PROVA.md).

## Construir frontend e backend

Depois de revisar uma especificação, mostre primeiro o plano:

```bash
PYTHONPATH=. python3 -m forja_core build examples/enterprise-spec-receivables.json /tmp/receivables
```

Quando estiver de acordo, autorize a materialização:

```bash
PYTHONPATH=. python3 -m forja_core build examples/enterprise-spec-receivables.json /tmp/receivables --apply
```

A FORJA cria um frontend responsivo, um backend local sem dependências pagas, contratos, testes, `run.sh` e relatório de limites. A prova é executada automaticamente; rede e instalação de pacotes ficam desativadas por padrão. Consulte [Executor conversacional](docs/14-EXECUTOR-CONVERSACIONAL.md).

## Companheira do Claude Code

Para economizar contexto e tokens, prepare apenas os arquivos relevantes:

```bash
PYTHONPATH=. python3 -m forja_core companheiro \
  "corrigir o fluxo de pagamentos e adicionar testes" \
  --repo ./meu-projeto
```

A FORJA cria `.forja/companion/CLAUDE_CONTEXT.md` com seleção de arquivos, estado Git, restrições e comando de prova. O Claude Code recebe esse pacote em vez do repositório inteiro. Veja [Companheiro Claude Code e tokens](docs/12-COMPANHEIRO-CLAUDE-CODE-E-TOKENS.md).

## Criar por conta própria

Se o objetivo é você aprender e construir o software, use o modo Autor:

```bash
PYTHONPATH=. python3 -m forja_core autor
```

A FORJA faz perguntas, cria a visão, o blueprint e um `NEXT_STEP.md` com uma única tarefa. Ela não escreve o produto no seu lugar: você implementa, testa e aprende; a FORJA organiza e verifica. Veja [Modo Autor e aprendizado](docs/13-MODO-AUTOR-E-APRENDIZADO.md).

## Documentação

- [Método FORJA](docs/01-METODO-FORJA.md)
- [Tutorial do zero](docs/02-TUTORIAL-DO-ZERO.md)
- [HOROCUM incorporado](docs/03-HOROCUM.md)
- [Criação de software incorporada](docs/04-CRIACAO-DE-SOFTWARE.md)
- [Stack 100% gratuita](docs/05-STACK-GRATUITA.md)
- [Protocolo empresarial](docs/06-PROTOCOLO-EMPRESARIAL.md)
- [FORJA Enterprise OS](docs/07-ENTERPRISE-OS.md)
- [Adaptadores Local, OonCore e Odoo](docs/09-ADAPTADORES-LOCAL-OONCORE-ODOO.md)
- [Criações reais da FORJA](examples/CREATIONS.md)
- [Blueprint empresarial e prova](docs/10-BLUEPRINT-EMPRESARIAL-E-PROVA.md)
- [Conversa natural e IA gratuita](docs/11-CONVERSA-NATURAL-E-IA-GRATUITA.md)
- [Companheiro Claude Code e tokens](docs/12-COMPANHEIRO-CLAUDE-CODE-E-TOKENS.md)
- [Modo Autor e aprendizado](docs/13-MODO-AUTOR-E-APRENDIZADO.md)
- [Relatório da prova](evidence/first-proof.md)

## Status honesto

**Núcleo educacional validado localmente.** O Forja Ledger não é ainda um ERP, não foi homologado em ambiente de cliente e não deve receber dados reais sem revisão, backup, autenticação e implantação apropriada. O Enterprise OS governa artefatos; ele não transforma automaticamente uma hipótese em negócio validado.

A FORJA mede progresso por evidência, não por quantidade de arquivos:

- Definição: 100%
- Exemplo executável: 100%
- Governança universal local: 100%
- Prova local: 100%
- Governança universal local: será registrada após a prova
- Produção empresarial: 0% até homologação real

## Licença

MIT para o código e a documentação deste repositório, exceto quando uma fonte externa for explicitamente indicada.
