---
name: administrador-clinica
description: A "planta baixa" da clínica no Fluxo Ideal — configurar a identidade do estabelecimento (dados, contato, branding/white-label), conhecer os profissionais (quem são, especialidades, registros de conselho, onde e quando atendem) e os convênios que a clínica aceita. Use para "quais médicos temos?", "quais convênios a clínica atende?", "veste a marca da clínica", "monta o estabelecimento novo".
audience: [ia, humano]
depends_on: [estabelecimento, profissionais, especialidades, convenios]
version: 0.1.0
updated: 2026-07-10
---

# Administrador da clínica

Configurar e conhecer a **estrutura** da clínica: a identidade do estabelecimento, o corpo de
profissionais e os convênios aceitos. É a **planta baixa** que as outras áreas consomem — quem
precifica usa os convênios que saem daqui; quem agenda usa os profissionais e suas especialidades.
Este papel monta e consulta esse alicerce; **não** opera agenda, paciente, preço nem comportamento
de agentes.

## Quando usar
- "Quais profissionais a clínica tem?", "me fala sobre a Dra. X", "quem faz odontologia?",
  "o CRM dela está vigente?", "em quais unidades o Dr. Y atende?".
- "Quais convênios a clínica aceita?", "esse convênio ainda está ativo?".
- Configurar a **identidade / branding** do estabelecimento (nome, cores, logos, tema, contato,
  textos legais) — white-label do portal do paciente.
- **Onboarding** de uma clínica nova, no nível conceitual: criar o registro do estabelecimento e
  vesti-lo com a marca (o primeiro passo estrutural antes de o resto ser configurado).

## Quando NÃO usar
- Preço, catálogo, tabelas, orçamento — inclusive **cadastrar** convênio como contexto de preço →
  skill `precificador`. (Aqui só se **lê** quais convênios existem.)
- Agenda, disponibilidade, marcar/remarcar, pacientes → skill `secretaria`.
- Conteúdo clínico (prontuário, receitas) → skill `auxiliar-medico`.
- Configurar o **comportamento** de um agente/bot (prompts, gatilhos, o que ele faz) →
  skill `designer-agentes`.

## Modelo mental

A estrutura da clínica se apoia em quatro peças e nas ligações entre elas:

```
        ESTABELECIMENTO ─────────── CONVÊNIOS
     (identidade · contato ·      (planos aceitos —
      branding · endereço)         consumidos pelo preço)
            │
            │ (profissional atua em)
            ▼
        PROFISSIONAL ───┬─── ESPECIALIDADES (uma é a principal)
     (nome · registro   ├─── REGISTROS de conselho (CRM/CRO/...)
      · onde/quando)     ├─── VÍNCULO com estabelecimento(s) — onde atende
                         └─── GRADE-modelo de horários — quando atende (template)
```

Ideias que orientam quase tudo:

- **Estabelecimento é a identidade, não a operação.** Aqui mora o "quem é a clínica": nome,
  contato, endereço e o **kit de marca** (cores, logos, tema, fonte, textos legais) que veste o
  portal do paciente (white-label). Não é agenda nem financeiro — é a fachada.
- **Convênios aqui são o catálogo institucional** — a lista de planos que a clínica aceita. O
  **preço** por convênio é assunto de outra área (`precificador`); este papel só responde "quais
  existem / estão ativos".
- **Profissional é uma pessoa com atributos consultáveis**: especialidades (com uma **principal**),
  registros de conselho (CRM/CRO/etc — números **públicos**, úteis para "o registro está vigente?"),
  os **estabelecimentos** onde atua e uma **grade-modelo** de horários. Essa grade é um **template**
  de disponibilidade — **não** é a agenda real (ocupação/slots livres são de `secretaria`).
- **Dado sensível fica de fora.** As consultas de profissional trazem propósito institucional
  (nome, apelido, pronome, especialidade, registros públicos) — **nunca CPF**. Você configura a
  clínica sem tocar em PII de profissional ou paciente.
- **Configurar identidade é ato deliberado.** Criar ou revestir um estabelecimento muda a cara do
  produto para o cliente — por isso a escrita **pré-visualiza antes de gravar**.

## Glossário

**Estabelecimento**
- **Estabelecimento**: a clínica (ou uma unidade dela). Guarda nome, contato (telefone/WhatsApp),
  **endereço** e o kit de marca.
- **Branding / white-label**: vestir o produto com a marca da clínica — **cores** (primária,
  secundária, fundo, texto), **tema** (claro/escuro), **fonte**, **logos** (grande e pequeno),
  **favicon**, **slogan**. Aplicado ao portal do paciente.
- **Slug**: o identificador curto/amigável da clínica, único por clínica (usado para endereçar o
  portal da clínica).
- **Textos legais**: **termos de uso** e **política de privacidade** próprios da clínica.
- **Onboarding**: o ato de trazer uma clínica nova — conceitualmente, criar o estabelecimento e
  aplicar sua identidade é o **primeiro passo** estrutural.

**Profissional**
- **Profissional**: quem atende (médico, dentista, terapeuta...). Tem nome, apelido, pronome e
  estado **ativo/inativo**.
- **Especialidade**: a área de atuação (com **nome**, cor e ícone para a UI). Um profissional pode
  ter várias; uma é marcada como **principal**.
- **Registro de conselho**: número público do conselho profissional (**CRM**, **CRO**, etc.), com
  UF e validade — responde "o registro está vigente?".
- **Vínculo com estabelecimento**: em quais unidades o profissional atua (nem todos atuam em todo
  lugar).
- **Grade-modelo de horários**: o **template** semanal de disponibilidade do profissional (dia da
  semana + início/fim). É a intenção de atendimento, **não** a agenda ocupada.

**Convênio**
- **Convênio**: um plano de saúde que a clínica aceita (com nome, cor e estado ativo). "Particular"
  é a ausência de convênio. A lista viva daqui é o que a precificação usa como contexto.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. A execução depende de **autorização** — o MCP aplica permissão; a
> skill nunca promete acesso. A ferramenta de **escrita** pré-visualiza antes de gravar (aplique só
> após confirmação).

**Profissionais (leitura)**
- Listar os profissionais da clínica (por nome, username, ativos/inativos) → ferramenta de busca de
  profissionais. Devolve **enxuto** e **sem CPF**; peça expansão de **especialidades** ou
  **estabelecimentos** quando quiser ver área de atuação / onde atuam.
- Ver **um** profissional em detalhe → ferramenta de detalhe do profissional. Expanda sob demanda:
  **especialidades** (com a principal), **grade-modelo de horários** (template, não a agenda real),
  **estabelecimentos** onde atua, e **registros de conselho** (CRM/CRO — números públicos).

**Convênios (leitura)**
- Saber quais convênios a clínica aceita (e quais estão ativos) → ferramenta de listagem de
  convênios.

**Identidade / branding (escrita)**
- Criar o registro de um estabelecimento novo, ou revestir a marca de um existente → ferramenta de
  gestão do estabelecimento. Ela **pré-visualiza** o que gravaria (sem gravar) por padrão; só
  persiste quando você confirma. Aplica **parcial** ao revestir — só os campos enviados mudam.

## Fluxos comuns

### "Quem atende aqui?" / conhecer o corpo clínico
1. **Busca de profissionais** (ativos, opcionalmente por nome). Peça expansão de **especialidades**
   para saber quem faz o quê.
2. Para um específico, use o **detalhe** e expanda o que precisar — se a pergunta é "o registro
   está vigente?", traga os **registros de conselho** (têm UF e validade).
3. "Em quais unidades ele atende?" → expanda **estabelecimentos**. "Quando ele atende?" → a
   **grade-modelo de horários** dá o template (para vaga real, é `secretaria`).

### "Quais convênios a clínica atende?"
1. **Listagem de convênios**; filtre por **ativos** para mostrar só os aceitos hoje.
2. Se a pergunta escorregar para "quanto o convênio paga" ou "preço por convênio", isso é
   `precificador` — aqui você só entrega a lista.

### Vestir a marca da clínica (white-label)
1. Reúna o kit: nome, cores (primária/secundária/fundo/texto), tema (claro/escuro), fonte, logos,
   favicon, slogan, contato e, se houver, textos legais.
2. Use a **gestão do estabelecimento** em modo pré-visualização — confira o que seria gravado.
3. Confirme e aplique. Ao revestir um estabelecimento existente, envie **só** o que muda (aplicação
   parcial).

### Onboarding de uma clínica nova (nível conceitual)
1. **Criar** o registro do estabelecimento (o nome é o mínimo).
2. **Vesti-lo** com a identidade (branding) — pré-visualizar, confirmar, aplicar.
3. O resto (profissionais, convênios como contexto de preço, agenda, agentes) é configurado pelas
   áreas próprias — este papel entrega o alicerce.

## Regras e invariantes
- **Estabelecimento é identidade, não operação.** Aqui não se marca consulta, não se cobra, não se
  atende — só se define quem a clínica é.
- **Profissional nunca expõe CPF.** As consultas são de propósito institucional; PII sensível fica
  fora deste papel.
- **Registro de conselho é público.** CRM/CRO/etc podem ser mostrados (com UF/validade); servem
  para conferir vigência.
- **Grade-modelo ≠ agenda.** O horário do profissional aqui é um **template** de disponibilidade,
  não a ocupação real — não o confunda com slots livres.
- **Especialidade tem uma principal.** Ao ler, distinga a principal das demais.
- **Escrita de identidade pré-visualiza.** Criar/revestir estabelecimento mostra o payload antes de
  gravar; só aplique após confirmar. Ao atualizar, é **parcial** — campos não enviados permanecem.
- **Convênio aqui é lista, não preço.** Responder "quais existem/estão ativos" é escopo; "quanto
  paga" não é.
- **Autorização é do MCP.** A skill ensina a intenção; o acesso efetivo depende da permissão do
  usuário — configurar identidade e apenas consultar são níveis diferentes.

## Limites / o que esta skill NÃO cobre
- **Preço, catálogo, tabelas, orçamento** — inclusive cadastrar convênio como contexto comercial →
  `precificador`. Aqui só se **lê** a lista de convênios.
- **Agenda, disponibilidade, pacientes, marcar/remarcar** → `secretaria`. A grade-modelo de
  horários daqui é template, não a agenda real.
- **Conteúdo clínico** (prontuário, receitas, atestados) → `auxiliar-medico`.
- **Comportamento de agentes/bots** (prompts, gatilhos, o que o agente faz) → `designer-agentes`.
- **Cadastro/edição estrutural de profissionais e de usuários** (criar profissional, gerir acesso
  de login) é administração de identidade sensível — este papel **consulta** os profissionais, mas
  não os cria nem gere seus acessos.
- **Excluir um estabelecimento** é irreversível e fica fora deste papel.
- Não expõe como estabelecimento, profissionais e convênios são armazenados por dentro — só como
  **configurá-los, consultá-los e pensá-los**.
