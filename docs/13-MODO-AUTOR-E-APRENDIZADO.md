# Modo Autor

A FORJA não precisa ser uma ponte para o Claude Code. Se você quer criar o software por conta própria, use:

```bash
PYTHONPATH=. python3 -m forja_core autor
```

Você responde perguntas naturais e recebe um kit de construção com:

- visão do problema;
- requisitos e blueprint;
- `NEXT_STEP.md` com uma única tarefa pequena;
- ciclo teste → falha → implementação → prova;
- `BUILD_LOG.md` para registrar seus aprendizados.

A FORJA **não escreve o produto no seu lugar** nesse modo. Ela organiza o terreno, ensina o próximo passo e verifica seus contratos. Isso preserva autoria e aprendizado.

## Método diário

1. Escolha apenas uma tarefa pequena.
2. Escreva o teste antes do código.
3. Execute e observe a falha.
4. Implemente o menor comportamento possível.
5. Rode a prova.
6. Faça commit.
7. Registre o que aprendeu.
8. Só então escolha a próxima tarefa.

## Divisão de responsabilidades

| Você | FORJA |
|---|---|
| decide o produto | organiza requisitos |
| escreve e entende o código | cria contratos e critérios |
| escolhe o design | bloqueia inconsistências |
| aprende com os erros | executa provas |
| faz a revisão final | registra limites |

Esse é o caminho correto se o objetivo é se tornar capaz de criar software, não apenas pedir que uma IA o produza.
