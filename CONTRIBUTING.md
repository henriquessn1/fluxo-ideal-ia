# Como escrever e manter uma skill

Este repositório é **público**. Cada skill deve **ensinar uma IA a raciocinar sobre o domínio e a
trabalhar com as ferramentas** disponíveis — **sem** expor como o sistema opera por dentro. Estas
regras são o contrato.

## A linha de corte (o teste de sanitização)

Antes de publicar/editar uma skill, pergunte por cada frase: _"isto ensina a **usar** o produto ou
revela **como ele é construído**?"_

**PODE entrar (ensina a usar):**
- Conceitos e vocabulário de domínio (o que é uma "tabela de preço", "coparticipação", "no-show").
- Modelo mental de como as coisas se relacionam no nível do negócio.
- **Ferramentas orientadas a tarefa**: "para consultar o preço de um item, use a ferramenta de busca
  de preços do MCP" — o _nome público_ da tool e _quando_ usá-la, task-first.
- Fluxos comuns ("como precificar um procedimento coberto parcialmente por convênio").
- Regras e invariantes de negócio ("no-show pode gerar multa configurável").

**NÃO pode entrar (revela a operação):**
- Endpoints/rotas HTTP internas, paths, prefixos, portas.
- Strings de permissão RBAC (`recurso:ação`), nomes de roles, seeds.
- Modelo de dados sensível: nomes de tabelas/colunas, migrations, chaves, campos LGPD.
- IPs, hosts, domínios de infra, nomes de stacks, variáveis de ambiente, segredos.
- Topologia interna ("o serviço X chama o Y via stream Z"), filas, nomes de eventos internos.
- A própria estrutura da documentação interna do produto (nomes/arquivos/mecanismos internos).
- Qualquer conteúdo de risco / "o que não expor" da documentação interna.
- Parâmetros exatos, payloads e formatos de request/response das ferramentas.

Regra de ouro: se um leitor de fora consegue **atacar** o sistema ou **clonar comercialmente** o
produto a partir da skill, corte. Se ele só entende **como usar** e **como o domínio pensa**, mantenha.

## Ensinar as ferramentas sem vazar

- Referencie a ferramenta pelo **papel** ("a ferramenta que lista convênios"), não por assinatura.
  O nome público da tool pode aparecer como rótulo, mas **não** documente params/permissões/erros.
- Foque em **quando** e **por quê** usar cada uma, e em que ordem — não em **como** ela é implementada.
- Deixe explícito que a _execução_ depende de **autorização** (o MCP aplica permissão); a skill nunca
  promete acesso, só ensina a intenção.

## Formato (Agent Skills)

Cada skill vive em `skills/<nome>/SKILL.md` com frontmatter:

```yaml
---
name: <kebab-case>
description: <1 linha — usada por IAs para decidir relevância>
audience: [ia, humano]
depends_on: [<serviços de domínio que a skill cobre>]   # rastreia o gatilho de atualização
version: <semver da skill>
updated: <AAAA-MM-DD>
---
```

Estrutura recomendada do corpo: **Quando usar / Quando NÃO usar → Modelo mental → Glossário →
Ferramentas (tarefa→ferramenta) → Fluxos comuns → Regras e invariantes → Limites**. Comece pelo
esqueleto em [`skills/_template/SKILL.md`](skills/_template/SKILL.md).

## Fonte da verdade e atualização

- As skills são **derivadas e sanitizadas** da documentação interna do produto (privada). A skill
  **não** copia a fonte interna; **reinterpreta** só a parte segura para uso externo.
- **Gatilho:** quando o comportamento de negócio de uma área em `depends_on` muda (novo fluxo, nova
  capacidade), **revise as skills que a cobrem** e faça bump de `version`/`updated`.
- **Skill desatualizada é pior que ausente** — quem lê toma decisão errada. Prefira remover a manter
  mentira.
- Publicação é **permanente** (indexação/cache/treinamento). Trate cada merge como irreversível:
  na dúvida sobre uma frase, ela **não** entra.
