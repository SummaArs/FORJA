# Método FORJA

## F — Fronteira

Escreva o que entra, o que sai e o que está fora. Um sistema empresarial não pode depender de uma capacidade que ninguém autorizou.

Perguntas:

- qual decisão o software ajuda a tomar?
- qual sistema é a fonte da verdade?
- que dado nunca pode ser inventado?
- o que exige uma pessoa?

## O — Objetos e invariantes

Modele estados, não apenas telas. Para cada entidade, escreva invariantes falsificáveis.

Exemplo do Forja Ledger:

- valor é inteiro em centavos;
- uma chave idempotente representa uma única intenção;
- repetir a mesma intenção não cria duas linhas;
- evento inválido não altera o banco;
- auditoria existe para cada mutação;
- reconciliação compara origem e destino.

## R — Risco proporcional

Para cada afirmação material:

1. o que está sendo afirmado?
2. o que pode dar errado?
3. qual é o impacto?
4. qual evidência mínima fecha a afirmação?

Baixo risco pede teste reproduzível. Alto risco pede sistema real, falha, recuperação e aceitação humana.

## J — Jornada comprovável

Construa o menor caminho completo, da entrada à fonte da verdade. Não construa dez telas antes de provar uma operação.

A jornada precisa incluir:

- caminho feliz;
- entrada duplicada;
- falha antes do commit;
- falha depois do commit;
- dado inválido;
- reconciliação;
- leitura humana do resultado.

## A — Ataque e auditoria

O autor não pode ser a única pessoa mentalmente envolvida. Separe papéis:

- **Dora**: problema real;
- **Aníbal**: fronteira e dependências;
- **Teo**: implementação;
- **Vera**: falhas e adversários;
- **Íris**: experiência do operador;
- **Rui**: operação e reversão.

A troca de chapéu não cria uma segunda pessoa. Por isso a prova precisa tocar o sistema, usar entradas não triviais e plantar um defeito.

## A lei mais importante

> Pode haver salto de trabalho. Não pode haver salto de confiança.

Uma feature pode nascer como experimento. Só pode ser chamada de capacidade validada depois que sua evidência foi executada e registrada.
