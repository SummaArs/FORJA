# Adaptadores de criação: Local, OonCore e Odoo Community

A FORJA agora separa **o raciocínio empresarial** do **destino técnico**. Você descreve o que precisa criar e escolhe onde o resultado vai viver.

## 1. Local

Use para prototipar ou criar um sistema independente:

```bash
PYTHONPATH=. python3 -m forja_core create local ./cliente-acme --name "Central Acme" --owner Gustavo --apply
```

## 2. OonCore

O adaptador usa o scaffold oficial `@oondemand/create-central-oon` em versão fixa. O pacote público auditado é o `0.7.8`.

Primeiro veja o plano:

```bash
PYTHONPATH=. python3 -m forja_core create ooncore ./acme-central --name "Acme Central"
```

Depois crie a base oficial:

```bash
PYTHONPATH=. python3 -m forja_core create ooncore ./acme-central \
  --name "Acme Central" --ooncore-version 0.7.8 --apply
```

O resultado esperado é a estrutura oficial com:

```text
.ooncore/
central.app.json
oon.deploy.json
backend/
frontend/
package.json
```

A FORJA não inventa APIs internas do OonCore. O projeto deve seguir a documentação autocontida em `.ooncore/` e validar com os comandos oficiais do scaffold:

```bash
npm run check
npm run build --prefix frontend
```

## 3. Odoo Community

A FORJA cria um addon padrão, sem exigir que o servidor Odoo esteja instalado no computador de criação:

```bash
PYTHONPATH=. python3 -m forja_core create odoo ./addons/acme_operacao \
  --name "Operação Acme" --apply
```

Ele gera:

```text
acme_operacao/
├── __init__.py
├── __manifest__.py
├── models/
├── security/ir.model.access.csv
├── views/
└── README.md
```

Isso é um scaffold real, mas ainda precisa ser validado no Odoo Community alvo. A FORJA não afirma compatibilidade universal entre versões sem executar o addon no ambiente correspondente.

## Fluxo recomendado

```text
problema do cliente
    ↓
manifesto FORJA
    ↓
plano somente leitura
    ↓
escolha do destino
    ├── local
    ├── OonCore
    └── Odoo Community
    ↓
criação do scaffold
    ↓
implementação da jornada
    ↓
provas do destino
    ↓
homologação
    ↓
publicação
```

A mesma jornada pode ter um adaptador OonCore e outro Odoo, mas as afirmações empresariais e os critérios de aceitação permanecem os mesmos.
