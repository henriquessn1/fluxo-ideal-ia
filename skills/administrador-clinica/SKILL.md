---
name: administrador-clinica
description: A "planta baixa" da clínica no Fluxo Ideal — configurar a identidade do estabelecimento (dados, contato, endereço, branding/white-label), cadastrar e gerir os profissionais (especialidades, registros de conselho, grade de horários, vínculos, documentos), os convênios aceitos, o catálogo de especialidades e o site público. Use para "cadastra a Dra. X", "adiciona esse convênio", "quais médicos temos?", "veste a marca da clínica", "monta o estabelecimento novo". Criar login/acesso (IAM) fica FORA.
audience: [ia, humano]
depends_on: [identidade-clinica, profissionais, especialidades, convenios, salas-recursos]
version: 0.2.1
updated: 2026-07-13
---

# Administrador da clínica

Configurar e conhecer a **estrutura** da clínica: a identidade do estabelecimento, o corpo de
profissionais, os convênios aceitos e as especialidades. É a **planta baixa** que as outras áreas
consomem — quem precifica usa os convênios que saem daqui; quem agenda usa os profissionais e suas
especialidades. Este papel **monta, mantém e consulta** esse alicerce (o profissional como **dado
cadastral**, o convênio institucional, o site público); **não** opera agenda, paciente, preço nem
comportamento de agentes, e **não cria login/acesso** (isso é IAM, fica fora).

## Quando usar
- "Quais profissionais a clínica tem?", "me fala sobre a Dra. X", "quem faz odontologia?",
  "o CRM dela está vigente?", "em quais unidades o Dr. Y atende?".
- **Cadastrar / editar um profissional** como **dado** — especialidades, registros de conselho,
  grade-modelo de horários, vínculo com unidade(s), documentos. (Criar o **login/acesso** dele é IAM,
  fora daqui.)
- "Quais convênios a clínica aceita?" e **cadastrar / ativar / desativar** um convênio institucional.
- Configurar a **identidade / branding** do estabelecimento (nome, cores, logos, tema, contato,
  **endereço**, textos legais) — white-label do portal do paciente.
- Configurar o **site público** da clínica e o **catálogo de especialidades**.
- **Onboarding** de uma clínica nova: criar o registro do estabelecimento e vesti-lo com a marca.

## Quando NÃO usar
- Preço, catálogo, tabelas, orçamento e o **preço por convênio** → skill `precificador`. Aqui se
  cadastra o convênio **institucional** (a lista de planos aceitos); o **preço** dele é lá.
- **Convênio/carteirinha do paciente** (vincular um plano a uma pessoa) → skill `secretaria`. A
  **configuração TISS** do convênio → `faturamento-convenio`. Aqui é o convênio como **entidade da clínica**.
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
- **Convênios aqui são o catálogo institucional** — a lista de planos que a clínica aceita, que este
  papel **cadastra, ativa e desativa**. O **preço** por convênio é de `precificador`; a **carteirinha
  do paciente** é de `secretaria`; a **config TISS** é de `faturamento-convenio`. Aqui é o convênio
  como **entidade da clínica**.
- **Profissional é uma pessoa que este papel cadastra e mantém** (como **dado**, não como acesso):
  especialidades (uma **principal**), registros de conselho (CRM/CRO — números **públicos**), os
  **estabelecimentos** onde atua, uma **grade-modelo** de horários (template de disponibilidade,
  **não** a agenda real — de `secretaria`) e **documentos**.
- **Cadastrar o profissional ≠ dar-lhe acesso.** Este papel cria/edita o **registro** do profissional;
  **criar login, senha ou papel de acesso (IAM)** é ato privilegiado à parte e **fica fora** (nunca a
  gestão de acessos). Montar a pessoa é aqui; deixá-la **entrar no sistema** é outro papel.
- **CPF é write-only.** Ao cadastrar/editar um profissional você **pode informar** o CPF, mas as
  leituras **nunca o devolvem** — some da projeção. Você configura sem PII sensível vazar de volta.
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

**Profissionais**
- **Ler:** listar os profissionais (por nome/username, ativos/inativos) → busca de profissionais
  (**enxuta**, **sem CPF**); ver **um** em detalhe → detalhe do profissional, expandindo sob demanda
  **especialidades** (com a principal), **grade-modelo de horários** (template, não a agenda real),
  **estabelecimentos** onde atua e **registros de conselho** (CRM/CRO — números públicos).
- **Cadastrar/editar (como dado):** criar ou atualizar o profissional, sua **grade de horários** e seus
  **documentos** → ferramentas de gestão de profissional. CPF é **write-only** (pode informar; nunca
  volta na leitura). **Não** cria login/acesso — isso é IAM, fora.

**Convênios**
- **Ler:** quais a clínica aceita (e ativos) → listagem de convênios.
- **Cadastrar/editar:** criar, ativar/desativar e editar um convênio **institucional** → ferramenta de
  gestão de convênio. É a lista de planos aceitos — o **preço** é `precificador`, a **carteirinha** é
  `secretaria`, a **config TISS** é `faturamento-convenio`.

**Especialidades**
- Manter o **catálogo de especialidades** (nome, cor, ícone) → ferramenta de gestão de especialidade.

**Estabelecimento (identidade / branding / site)**
- **Ler:** dados do estabelecimento → detalhe/listagem do estabelecimento.
- **Configurar:** criar um estabelecimento novo, revestir a **marca** (cores, logos, tema, fonte,
  textos legais) e o **endereço/contato** → gestão do estabelecimento; e ligar/ajustar o **site
  público** → gestão do site. Ambas **pré-visualizam** antes de gravar e aplicam **parcial** (só o que
  muda) — persiste só após confirmar.

**Salas / equipamentos / recursos**
- **Ler:** listar/filtrar as salas, consultórios e equipamentos (por unidade, tipo, ativo) → ferramenta de
  busca de recursos.
- **Cadastrar/editar:** criar, editar ou remover uma sala/consultório/equipamento (tipo, capacidade,
  ativo) → ferramenta de gestão de recurso (**pré-visualiza** antes de gravar). É **cadastro** institucional,
  sem PII. *Agendar por sala* (alocar num agendamento e bloquear dupla-ocupação) é do domínio da agenda —
  ainda em construção.

## Fluxos comuns

### "Quem atende aqui?" / conhecer o corpo clínico
1. **Busca de profissionais** (ativos, opcionalmente por nome). Peça expansão de **especialidades**
   para saber quem faz o quê.
2. Para um específico, use o **detalhe** e expanda o que precisar — se a pergunta é "o registro
   está vigente?", traga os **registros de conselho** (têm UF e validade).
3. "Em quais unidades ele atende?" → expanda **estabelecimentos**. "Quando ele atende?" → a
   **grade-modelo de horários** dá o template (para vaga real, é `secretaria`).

### Convênios: consultar e cadastrar
1. **Listar** os convênios; filtre por **ativos** para os aceitos hoje.
2. Para **adicionar / ativar / desativar** um convênio institucional → **gestão de convênio**
   (pré-visualiza, confirma, aplica).
3. "Quanto o convênio paga / preço por convênio" é `precificador`; "carteirinha do paciente" é
   `secretaria`; "faturar TISS" é `faturamento-convenio`. Aqui é a **entidade** convênio.

### Cadastrar um profissional novo (como dado)
1. Crie o **registro** do profissional (nome/atributos) — pré-visualize, confirme, aplique.
2. Complete: **especialidades** (marque a principal), **registros de conselho** (CRM/CRO com UF/validade),
   **vínculo** com a(s) unidade(s), a **grade-modelo de horários** e **documentos**. CPF é write-only.
3. Dar-lhe **login/acesso** ao sistema é **IAM** — outro papel, fora daqui.

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
- **CPF é write-only.** Pode ser informado ao cadastrar/editar um profissional, mas a **leitura nunca
  o devolve** — as consultas são de propósito institucional e a PII sensível não volta na projeção.
- **Cadastrar ≠ dar acesso.** Criar/editar o profissional é cadastro de **dado**; criar login/senha/
  papel de acesso é **IAM** e fica **fora** (nunca a gestão de acessos).
- **Registro de conselho é público.** CRM/CRO/etc podem ser mostrados (com UF/validade); servem
  para conferir vigência.
- **Grade-modelo ≠ agenda.** O horário do profissional aqui é um **template** de disponibilidade,
  não a ocupação real — não o confunda com slots livres.
- **Especialidade tem uma principal.** Ao ler, distinga a principal das demais.
- **Escrita de identidade pré-visualiza.** Criar/revestir estabelecimento mostra o payload antes de
  gravar; só aplique após confirmar. Ao atualizar, é **parcial** — campos não enviados permanecem.
- **Convênio aqui é a entidade institucional (cadastro), não o preço nem a carteirinha.** Criar/ativar/
  desativar o convênio da clínica é escopo; "quanto paga" é `precificador`, "carteirinha do paciente" é
  `secretaria`, "TISS" é `faturamento-convenio`.
- **Autorização é do MCP.** A skill ensina a intenção; o acesso efetivo depende da permissão do
  usuário — configurar identidade e apenas consultar são níveis diferentes.

## Limites / o que esta skill NÃO cobre
- **Preço, catálogo, tabelas, orçamento** — inclusive cadastrar convênio como contexto comercial →
  `precificador`. Aqui só se **lê** a lista de convênios.
- **Agenda, disponibilidade, pacientes, marcar/remarcar** → `secretaria`. A grade-modelo de
  horários daqui é template, não a agenda real.
- **Conteúdo clínico** (prontuário, receitas, atestados) → `auxiliar-medico`.
- **Comportamento de agentes/bots** (prompts, gatilhos, o que o agente faz) → `designer-agentes`.
- **Login / acesso (IAM)** — criar usuário, senha, papel de acesso, reset de senha — é administração de
  identidade privilegiada e fica **fora** (nunca a gestão de acessos). Este papel cadastra o profissional como
  **dado** (registro, especialidades, horários, documentos), mas **não** cria nem gere o **acesso** dele
  ao sistema.
- **Agendar por sala** (alocar um recurso num agendamento e bloquear dupla-ocupação) ainda **não** existe —
  o **cadastro** de salas/equipamentos é aqui, mas a **agenda por recurso** é capacidade futura (domínio da agenda).
- **Excluir um estabelecimento** é irreversível e fica fora deste papel.
- Não expõe como estabelecimento, profissionais e convênios são armazenados por dentro — só como
  **configurá-los, consultá-los e pensá-los**.
