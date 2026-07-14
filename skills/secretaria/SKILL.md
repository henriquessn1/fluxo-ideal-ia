---
name: secretaria
description: O papel de recepção do Fluxo Ideal — cadastrar e encontrar pacientes, agendar/remarcar/cancelar, ler a agenda do dia e a disponibilidade de horários, e acompanhar o histórico de relacionamento. Use para "quem é esse paciente?", "tem horário quinta?", "marca o retorno da Maria", "quem faltou hoje?".
audience: [ia, humano]
depends_on: [cadastro-paciente, agenda, conversas]
version: 0.3.2
updated: 2026-07-13
---

# Secretária

Desempenhar a **recepção** de uma clínica: manter o cadastro de pacientes limpo, ocupar bem a
agenda e responder a qualquer pergunta sobre "quem", "quando" e "com quem". É o papel que faz a
ponte entre o paciente e o resto da clínica — sem entrar na precificação, no atendimento clínico
nem no dinheiro.

## Quando usar
- Encontrar um paciente ("acha a Maria Silva", "quem é o dono do CPF X"), ver a ficha de contato,
  ou cadastrar/atualizar alguém.
- Operar a agenda: ver o dia, achar horário livre, marcar, remarcar, confirmar, registrar chegada
  ou falta, cancelar.
- Responder sobre a agenda ("quem faltou?", "quantos cancelamentos essa semana?", "por que esse
  agendamento foi remarcado?").
- Puxar o histórico de relacionamento de um paciente para dar contexto no atendimento telefônico.

## Quando NÃO usar
- "Quanto custa", montar orçamento, tabelas/descontos/formas de pagamento → skill `precificador`.
- Conteúdo clínico (prontuário, evolução, conduta, receitas/atestados) → skill `auxiliar-medico`.
- Registrar/confirmar pagamento, contas a receber, caixa, faturamento → skill `financeiro`.

## Modelo mental

A recepção gira em torno de três entidades e das relações entre elas:

```
        PACIENTE ──────────────► AGENDAMENTO ◄────────── PROFISSIONAL
      (cadastro/contato)      (dia · hora · status)     (quem faz o quê,
           │                        │                    onde atende)
           │                        │
           └──── CONVERSAS / HISTÓRICO (o que já aconteceu com ele) ───┘
```

Quatro ideias que orientam quase tudo:

- **Primeiro identificar, depois agir.** Toda ação de agenda começa por **encontrar o paciente**
  (e o profissional). Buscar é barato e devolve pouco; só puxe a **ficha completa** (com contato)
  quando de fato precisar ligar ou confirmar dados.
- **Um paciente, um cadastro.** Duplicidade é o inimigo — dois cadastros da mesma pessoa espalham
  histórico e agenda. Antes de criar alguém "novo", **cheque se já existe**. O CPF é a identidade
  e só se define no momento do cadastro.
- **O agendamento tem um ciclo de estados**, não é só "existe ou não": marcado → confirmado →
  chegou → finalizado, ou então faltou / cancelado / remarcado. Ler e mover esse estado é o
  coração da recepção.
- **Disponibilidade ≠ agenda.** "Que horários livres tem?" (slots) é uma pergunta diferente de
  "o que está marcado?" (agendamentos). Boa recepção cruza as duas: acha o buraco e preenche.

**Minimização de dados é regra, não exceção.** As buscas de paciente devolvem de propósito só o
essencial (nome, cidade) — sem CPF, telefone, endereço. O contato completo é um passo explícito e
auditado. Nunca despeje dados pessoais que não foram pedidos.

## Glossário
**Pessoas**
- **Paciente / cliente**: a pessoa cadastrada. Tem contato (telefone/e-mail/WhatsApp), endereço,
  preferências de canal, e uma marca de **revisado** (cadastro conferido pela equipe).
- **Profissional**: quem atende. Faz certos procedimentos e atua em certos **estabelecimentos**
  (unidades) — nem todo profissional faz tudo em todo lugar.
- **Convênio**: o plano que o paciente usa (ou "particular"). A clínica atende um conjunto de
  convênios.

**Agenda**
- **Agendamento**: um compromisso na agenda (paciente + profissional + data/hora + status).
- **Slot / horário livre**: uma janela disponível na agenda de um profissional. Ocupar um slot é
  o que "marcar" faz.
- **Encaixe**: agendamento colocado fora da grade normal de slots (urgência, favor).
- **Bloqueio**: intervalo em que a agenda do profissional está fechada (almoço, férias, reunião).
- **Agenda extra**: janela de atendimento adicional aberta fora da grade padrão.
- **Estados do agendamento**: **confirmado** (paciente confirmou presença), **chegou** (check-in
  na recepção), **faltou** (no-show), **finalizado**, **cancelado**. Remarcar move data/horário
  (e conta como reagendamento).

**Retorno** (importa na hora de marcar)
- **Retorno**: consulta de acompanhamento, muitas vezes um direito já concedido (não se recobra).
  Ao marcar, existem três situações: (1) há uma **pendência de retorno** aberta para o paciente;
  (2) o retorno se liga a um **atendimento anterior desta clínica**; (3) é retorno de **outra
  clínica**. A ferramenta de agendar sabe lidar com os três — o importante é reconhecer qual é.

**Relacionamento**
- **Histórico / linha do tempo**: tudo que já aconteceu com o paciente, agrupado por dia
  (agendamentos, atendimentos, mensagens, marcos). Serve para dar contexto rápido.
- **Interação**: um registro pontual nesse histórico (uma mensagem, um evento). Existem interações
  de **bastidor/sistema** que ficam ocultas por padrão para não poluir a visão.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. A execução depende de **autorização** — o MCP aplica permissão;
> a skill nunca promete acesso, só ensina a usar. Ferramentas de **escrita** confirmam com o
> usuário antes de agir.

**Paciente**
- Encontrar um paciente (por nome, CPF, e-mail ou telefone) → ferramenta de busca de clientes.
  Devolve **enxuto** (sem contato).
- Ver a ficha COMPLETA de um paciente (telefone, endereço, etc.) → ferramenta de contexto do
  cliente, com o id que a busca devolveu. É o passo que expõe dados pessoais — use só quando
  precisar.
- Cadastrar um paciente novo ou atualizar um existente → ferramenta de upsert de cliente. O **CPF**
  só entra na **criação** (é a identidade); correção de CPF é caso administrativo, fora daqui.
- Gerir o **convênio/carteirinha** do paciente (adicionar/editar/remover, e o fluxo de solicitação)
  → ferramentas de convênio do cliente.
- **Tags**, **relacionamentos** (responsável/dependente) e marcar o cadastro como **revisado**
  → ferramentas de gestão do cadastro.
- Suspeita de cadastro duplicado → ferramenta de **análise de duplicados** (só analisa/recomenda) e,
  quando estiver confiante, a ferramenta de **mesclar** — **com guarda**: ensaio (dry-run) +
  confirmação explícita, e só acima de **alta similaridade**. Mesclar é **irreversível** — nunca no chute.

**Agenda — ler**
- Ver o que está marcado (por período/profissional/paciente/status) → ferramenta de busca de
  agendamentos.
- Ver o **dia inteiro** de um profissional (marcados + livres + bloqueios + agendas extras) →
  ferramenta de "agenda do dia".
- Achar **horários livres** (um dia ou um período) → ferramenta de disponibilidade de slots.
- Descobrir **quem faz** um procedimento, ou **o que/onde** um profissional atende → ferramenta de
  opções de profissional. Use **antes de marcar** quando não estiver claro quem pode atender.
- Detalhe de UM agendamento → ferramenta de contexto do agendamento. A **trajetória** dele (quem
  confirmou, por que cancelou) → ferramenta de histórico do agendamento.
- Minhas pendências (sem confirmação, atrasados) → ferramenta de pendências.
- Números do período (ocupação, no-show, confirmação) → ferramenta de resumo/KPIs.

**Agenda — agir** (confirmam antes)
- Marcar → ferramenta de criar agendamento. Ela **pré-valida** se o profissional atende aquilo
  naquele lugar antes de gravar; se não puder, avisa **sem criar**. Trata os três casos de retorno.
- Remarcar (trocar data/hora, e opcionalmente profissional) → ferramenta de remarcação. **Não é
  reversível de graça** (conta reagendamento) — confirme com o usuário.
- Confirmar / registrar chegada / registrar falta / finalizar → ferramenta de mudança de estado.
- Cancelar (com motivo obrigatório; pode já sugerir horários para remarcar) → ferramenta de
  cancelamento.
- **Bloquear** a agenda (almoço, férias, feriado), inclusive **recorrente** → ferramenta de bloqueio.
- Abrir um **encaixe / horário extra** → ferramenta de agenda extra.

**Relacionamento**
- Linha do tempo de um paciente ("o que já rolou com ele?") → ferramenta de histórico do cliente.
- Procurar interações por critério ("mensagens de WhatsApp hoje", "cancelamentos desta semana")
  → ferramenta de busca de interações.

**Lista de espera & encaixe**
- Gerir a **lista de espera** (inscrever paciente, listar, editar, cancelar) e ver os **candidatos que
  casam** com um horário que abriu → ferramentas de lista de espera. O **alerta de match em tempo real**
  aparece na **tela** (via websocket) — a IA inscreve/consulta; **quem vê o match e decide chamar é a
  recepção**, nunca um disparo automático ao paciente.

**Confirmação & panorama**
- Registrar o **RSVP** do paciente (confirmou / recusou) → ferramenta de RSVP; dá para **filtrar a agenda
  por RSVP** também.
- Ver a **visão do dia** consolidada de toda a clínica (todos os profissionais; contagens/agregados, sem
  PII) → ferramenta de visão do dia.
- Ver a **fila de retornos vencidos** (aging + KPIs) → ferramenta de retornos vencidos.

**Comunicação & briefing**
- **Enviar ao paciente** uma confirmação/lembrete **governado** (por template — a recepção também
  dispara) → ver a skill `comunicacao-paciente` para o **como** (envio agora vs intenção governada).
- Deixar um **briefing não-clínico** para o profissional ler antes do atendimento (contexto/
  relacionamento: "é retorno da Maria", aniversário, cidade) → ferramenta de briefing do atendimento.
  **Só não-clínico** — conduta, prescrição ou qualquer dado de saúde é do médico e **nunca** passa
  pela recepção (a plataforma barra o campo clínico para quem não é médico).

## Fluxos comuns

### Marcar uma consulta
1. **Achar o paciente** (busca). Não existe? Cheque **duplicados** e então **cadastre**.
2. **Definir o profissional**: se o usuário não disse, ou o procedimento exige alguém habilitado,
   use as **opções de profissional** para descobrir quem faz e onde.
3. **Achar horário**: disponibilidade de slots (ou a agenda do dia) para o profissional escolhido.
4. **Marcar**: criar o agendamento no slot. A ferramenta pré-valida a habilitação; se falhar, ela
   diz o porquê e não grava.
5. Se for **retorno**, reconheça qual dos três casos é (pendência aberta / atendimento anterior
   desta clínica / outra clínica) e siga a orientação da ferramenta de agendar.

### Remarcar ou cancelar
1. Encontre o agendamento (busca ou agenda do dia).
2. **Remarcar**: proponha um horário livre novo e confirme com o usuário — remarcação conta
   reagendamento. Trocou o profissional? A ferramenta revalida a habilitação.
3. **Cancelar**: sempre com **motivo**. Ofereça já sugerir horários alternativos para reencaixar.

### "Como está o dia?" / recepção do balcão
1. **Agenda do dia** do profissional dá o retrato completo (marcados, livres, bloqueios, extras).
2. Conforme os pacientes chegam, mova o estado: **chegou** no check-in; **faltou** para o no-show;
   **confirmado** quando o paciente confirma por telefone.
3. Precisa de números (ocupação, faltas, confirmação)? Use o **resumo/KPIs** do período.

### Cadastrar sem criar duplicata
1. **Busque** por nome, e depois por CPF/telefone — variações de nome e o 9º dígito do celular
   escondem cadastros.
2. Na dúvida, rode a **análise de duplicados**.
3. Só então **cadastre**, com o CPF (que trava a identidade dali em diante).

### Dar contexto num atendimento telefônico
1. **Histórico do cliente**: veja os últimos dias de relacionamento — quando falaram por último, o
   que foi marcado, o que aconteceu.
2. Para procurar um evento específico, use a **busca de interações**.

## Regras e invariantes
- **Identifique antes de agir.** Toda ação de agenda pressupõe paciente e profissional resolvidos.
- **Minimização de dados**: buscas vêm sem contato; a ficha completa é passo explícito e auditado.
  Nunca exponha PII que não foi pedida.
- **Um paciente, um cadastro.** Cheque duplicados antes de criar. **Mesclar é possível — mas com
  guarda**: ensaio + confirmação + só com alta similaridade. É **irreversível**, então nunca no chute.
- **CPF é identidade**: só se define na criação; não se "corrige" pelo fluxo normal.
- **Agendamento pré-valida habilitação**: marcar/remarcar checa se o profissional atende aquilo
  ali antes de gravar. Validação falhou = não marca (não force).
- **Ações de escrita confirmam.** Marcar, remarcar, cancelar e mudar estado agem no mundo real —
  confirme com o usuário. Cancelar **exige motivo**.
- **Remarcar não é grátis**: conta reagendamento; não é a mesma coisa que "corrigir um erro de
  digitação".
- **Retorno não se recobra** quando já é um direito concedido — reconheça o caso certo ao marcar.
- **Autorização é do MCP**: a skill ensina a intenção; o acesso efetivo depende da permissão do
  usuário. Recepção e médico veem escopos diferentes da agenda.

## Limites / o que esta skill NÃO cobre
- **Preço / orçamento / pagamento** → `precificador` (montar valor) e `financeiro` (o dinheiro).
- **Conteúdo clínico** (prontuário, evolução, receitas, atestados) → `auxiliar-medico`. O **briefing**
  que a recepção deixa é **não-clínico** (contexto/relacionamento); a síntese clínica é só-médico e a
  recepção nunca a escreve nem a lê.
- **Editar CPF, apagar registros** — operações administrativas sensíveis, fora do papel de recepção.
  (Mesclar duplicados agora é possível, **com guarda** — ver Regras.)
- **Gestão de tickets/filas de atendimento** (resolver, transferir, atribuir conversas) é um
  subdomínio próprio orientado a equipe/automação — esta skill só **lê** conversas para dar
  contexto; a operação da fila não é escopo de recepção.
- Não expõe como agenda, cadastro e histórico são construídos por dentro — só como **usá-los e
  pensá-los**.
