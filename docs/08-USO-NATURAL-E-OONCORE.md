# Uso natural da FORJA e conexão com OonCore

## Como começar um cliente novo

Em vez de decorar comandos, diga para si mesmo:

> “Vou preparar o espaço, entender o problema, registrar o que importa e só depois construir.”

No terminal:

```bash
PYTHONPATH=. python3 -m forja_core init ./cliente-acme --name "Acme" --owner Gustavo
```

A FORJA cria a pasta `forja/` e deixa uma próxima pergunta simples:

```text
Qual problema empresarial precisa mudar?
```

Depois você preenche o manifesto com o artefato real: software, processo, produto ou qualquer outro resultado.

## Conectar OonCore

A conexão foi desenhada como **descoberta somente leitura**. A FORJA não presume qual é o repositório, não executa scripts do OonCore e não altera seus arquivos.

### Repositório local

```bash
PYTHONPATH=. python3 -m forja_core connect \
  --workspace ./cliente-acme \
  --repo /caminho/para/ooncore \
  --name ooncore
```

### Repositório remoto

```bash
PYTHONPATH=. python3 -m forja_core connect \
  --workspace ./cliente-acme \
  --repo https://github.com/ORGANIZACAO/ooncore.git \
  --name ooncore
```

O registro salvo em `cliente-acme/forja/connection-ooncore.json` informa:

- origem do repositório;
- se é referência local ou remota;
- presença de Git;
- presença de README;
- instruções de agentes;
- sinais de testes ou prova;
- se é seguro continuar a descoberta.

## O que ainda precisa ser passado

Para uma integração real, ainda é necessário fornecer o repositório correto do OonCore ou seu caminho local. Sem isso, a FORJA só pode oferecer o conector genérico. Ela não deve inventar o repositório, a versão, as permissões ou os contratos da plataforma.

Depois que o repositório for informado, a próxima etapa será uma auditoria de compatibilidade:

1. ler o README e o template oficial;
2. localizar comandos de prova;
3. identificar o contrato de extensão;
4. mapear arquivos que podem ser alterados;
5. registrar divergências;
6. propor um adaptador;
7. executar primeiro em modo somente leitura;
8. pedir confirmação apenas antes de qualquer operação mutável.

## Filosofia

Você não precisa pensar “qual comando técnico devo lembrar?”. Pense:

```text
qual problema existe?
qual artefato vou produzir?
qual afirmação precisa ser verdadeira?
como provo?
qual é o próximo menor passo?
```

A CLI existe para carregar a burocracia; você continua concentrado no raciocínio do negócio.
