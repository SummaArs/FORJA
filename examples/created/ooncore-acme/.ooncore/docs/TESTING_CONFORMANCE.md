# Testes e conformidade

## App consumidor

```bash
npm run check
npm run build --prefix frontend
```

No scaffold, `check` executa `doctor`, que inclui docs check e conformance, versões instaladas, lockfiles e diagnóstico de composição. Rode também os testes relevantes declarados pelo App; a base neutra não cria um script raiz `test`. Prove a jornada com acesso permitido/recusado, validação de entrada, resultado e persistência quando aplicável. Não duplique verificações sem uma mudança ou risco concreto.

A homologação global da Plataforma e os testes de segurança do runtime pertencem ao SDK/Plataforma. O App preserva os contratos e comprova sua integração específica. Se alterar uma fronteira de segurança, cubra explicitamente essa mudança.

## Manutenção do SDK

Alterações no runtime exigem as provas pertinentes: loopback, sessão/CSRF, expiração, perfis, isolamento, recusa de identidade operacional local e ausência de chamadas à Plataforma. Esses cenários não são pré-requisito repetido para cada página de um App.

## Documentação distribuída

`create-central-oon docs check` valida fonte, versão, schema, entrada, hashes e arquivos. `docs sync` regenera o cache a partir da fonte do pacote. O tarball deve conter docs, templates e schemas. Verifique links e exemplos alterados; build, publicação e homologação são evidências diferentes.


No monorepo, `npm run check:authoring` executa os testes do gerador uma vez e verifica typecheck/build da base com o exemplo integrado. Execute após o build do SDK frontend. A suíte backend inclui HTTP real e MongoDB descartável para a mesma jornada; não simula router. No CI essas entradas substituem os checks duplicados.
