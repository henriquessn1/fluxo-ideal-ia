---
name: conversas
description: A operação do atendimento ao paciente no Fluxo Ideal via tickets e filas — abrir/atribuir/transferir/resolver o ciclo de uma conversa (com CSAT no fechamento), observar (acompanhar), comentar por dentro, marcar a timeline, buscar conversas e histórico, e detectar conversas frustradas (risco de churn). Use para "atende esse ticket", "passa pra recepção", "resolve isso", "quem está insatisfeito?".
audience: [ia, humano]
depends_on: [conversas, tickets, filas, observadores]
version: 0.1.0
updated: 2026-07-10
---

# Conversas

Operar o **relacionamento em andamento** com o paciente: pegar uma conversa, dar a ela um
dono, movê-la entre filas de equipe, comentar por dentro para a equipe, acompanhar até um
desfecho, encerrar com registro de satisfação, e enxergar quem está insatisfeito antes que
vire cancelamento. É o papel de quem **conduz o atendimento** — não de quem redige a
mensagem, nem de quem só lê a conversa para ter contexto.

## Quando usar
- Assumir/encaminhar um atendimento: "pega esse ticket", "atribui pra mim", "passa pra
  recepção", "manda pro financeiro".
- **Encerrar** um atendimento concluído (com a pesquisa de satisfação que dispara junto) —
  ou **cancelá-lo** quando não houve resolução (engano, spam, paciente sumiu).
- Deixar **rastro interno** numa conversa (nota que a equipe vê e o paciente nunca).
- **Acompanhar** uma conversa até um marco (ex.: até o agendamento acontecer) sem ser o dono.
- **Achar** conversas por critério e ver o **histórico** de relacionamento do paciente.
- Descobrir **quem está frustrado/insatisfeito** ("quem está prestes a cancelar?").
- Anotar um **marco na linha do tempo** da clínica (início de campanha, aviso, feriado).

## Quando NÃO usar
- **Escrever/enviar a mensagem** que vai ao paciente (texto do lembrete, e-mail, HSM,
  disparo) → skill `designer-mensageria`. Aqui você cuida do **thread e do estado**; lá,
  do **conteúdo**.
- Só **ler** a conversa para dar contexto num atendimento telefônico, sem operar o ciclo →
  skill `secretaria` (ela lê; esta **opera**).
- Agenda, cadastro de paciente, marcar/remarcar → `secretaria`.
- Pesquisa de satisfação/NPS como instrumento (montar perguntas, resultados) → skill de
  `pesquisas`. Aqui o CSAT é só **consequência de resolver** um ticket.
- Conteúdo clínico, preço/orçamento, dinheiro → `auxiliar-medico` / `precificador` /
  `financeiro`.

## Modelo mental

A peça central é a distinção entre **conversa** e **ticket**:

```
   CONVERSA (a thread — é ETERNA: 1 paciente/canal, uma linha só pra sempre)
      │
      ├──── TICKET #1 (um EPISÓDIO de atendimento: abre → dono → encerra)
      │        estados:  não-atribuída → em atendimento ⇄ aguardando paciente ⇄ pausada
      │                        │                                    │
      │              (encerramento)──────────────┬─────────────┬────┘
      │                        ▼                 ▼             ▼
      │                    RESOLVIDA          CANCELADA     EXPIRADA
      │                  (dispara CSAT)     (sem resolução)  (inatividade)
      │
      └──── TICKET #2 ...  (o paciente volta depois → abre um ticket NOVO, não reabre)

   quem toca o ticket:  DONO (responsável, 1 só) · FILA (sem dono, a equipe pega) ·
                        OBSERVADORES (acompanham, não são donos)
```

Ideias que sustentam tudo:

- **Conversa ≠ ticket.** A **conversa** é a thread inteira com o paciente — nunca some. O
  **ticket** é um **episódio** de atendimento dentro dela (abre, ganha dono, encerra). Quando
  o paciente volta com um assunto novo depois de um episódio encerrado, abre-se um **ticket
  novo** — não se "reabre" o antigo. Isso dá fronteiras limpas para métricas e privacidade.
- **No máximo um ticket aberto por conversa.** Um episódio de cada vez. Se há assunto em
  aberto, ele é o ticket; encerrá-lo é o que libera a conversa.
- **Dono vs. fila.** Um ticket ou tem **um responsável** (a pessoa/agente que está cuidando)
  ou está numa **fila** (sem dono, esperando a equipe do setor pegar). Atribuir dá dono;
  transferir para fila **tira** o dono e devolve o episódio ao grupo.
- **Encerrar tem três sabores, e só um vira "satisfação".** **Resolver** = o assunto se
  concluiu → dispara a **pesquisa de satisfação (CSAT)**. **Cancelar** = encerrou **sem**
  resolução (engano, spam, duplicada, paciente sumiu) → **não** dispara CSAT nem conta como
  resolvido. **Expirar** = o sistema fecha por inatividade prolongada. Não confunda: cancelar
  para fugir de nota baixa deixa rastro auditável.
- **Observar ≠ ser dono ≠ ter acesso.** Um **observador** acompanha os eventos de uma
  conversa sem ser responsável por ela (um gestor de olho num VIP, um agente esperando um
  marco). Inscrever-se **não** concede leitura de conteúdo — o observador ainda precisa do
  próprio acesso. Observação pode ser **temporária** (some sozinha quando o marco chega).
- **Comentar é por dentro.** Uma nota interna fica **só para a equipe** e **nunca** vai ao
  paciente. É o lugar de justificar uma transição, registrar o que foi decidido, ou passar
  contexto para quem assumir. Para falar **com** o paciente, é `designer-mensageria`.
- **Marcador de timeline é global, não do paciente.** Um marco (início de campanha, aviso)
  aparece sobreposto na linha do tempo de **todos** os pacientes cuja janela pegar aquela
  data — é um recado da clínica, não um evento de uma pessoa.

## Glossário

**Thread e episódio**
- **Conversa**: a thread de relacionamento com um paciente num canal (ex.: WhatsApp). É a
  **fonte da verdade** e **não termina** — o paciente sempre volta na mesma linha.
- **Ticket / atendimento**: um **episódio** dentro da conversa — abre, ganha dono, encerra.
  "Ticket" é o termo aqui para não confundir com o atendimento **clínico** (outro domínio).
- **Fronteira de episódio**: o encerramento de um ticket. O próximo contato do paciente abre
  um ticket **novo**; não se reabre um episódio já fechado (a não ser reabertura pontual de
  um recém-resolvido, quando a equipe percebe que ficou algo pendente).

**Estados do ticket**
- **Não-atribuída**: aberto, ainda sem dono (na fila de entrada).
- **Em atendimento**: alguém (pessoa ou agente) está cuidando.
- **Aguardando paciente**: a bola está com o paciente (esperando resposta).
- **Pausada**: parada temporariamente.
- **Resolvida**: concluída com desfecho → **dispara CSAT**. Estado terminal.
- **Cancelada**: encerrada **sem** resolução (engano/spam/duplicada/paciente sumiu). **Não**
  dispara CSAT, **não** conta como resolvido. Terminal.
- **Expirada**: fechada automaticamente por **inatividade** prolongada. Terminal.

**Papéis sobre o ticket**
- **Dono / responsável**: quem está com o atendimento (um só por vez). Pode ser uma **pessoa**
  ou um **agente**.
- **Fila / setor**: destino sem dono — a equipe daquela fila pega o ticket pelo inbox.
  Transferir para fila é o **handoff** para humanos (ou entre setores).
- **Observador**: quem **acompanha** a conversa sem ser dono. Pode ser pessoa ou agente. A
  inscrição pode **expirar** (acompanhar só até um marco). Observar **não** dá acesso ao
  conteúdo por si só.

**Registros**
- **Comentário / nota interna**: texto que **só a equipe** vê; nunca sai para o paciente.
  Serve de rastro, justificativa de transição, ou contexto para o próximo.
- **CSAT**: a pesquisa de satisfação que a resolução dispara — a nota do paciente sobre aquele
  atendimento. É **efeito** de resolver, não algo que se dispara à mão daqui.
- **Marco de timeline**: um recado **global** da clínica (campanha, aviso, feriado) que
  aparece sobreposto na linha do tempo de todos os pacientes na janela da data.
- **Histórico / linha do tempo do paciente**: tudo que já aconteceu com ele, agrupado por dia
  (mensagens, agendamentos, atendimentos, marcos). Contexto rápido.
- **Conversa frustrada**: uma conversa que a análise de experiência do cliente sinalizou como
  insatisfeita/em risco. É um **conceito de CX** (leitura sobre o relacionamento), usado para
  priorizar quem precisa de atenção — não um veredito automático de cancelamento.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. A execução depende de **autorização** — a plataforma aplica
> permissão; a skill nunca promete acesso. Ações que mudam o estado do atendimento ou tocam o
> paciente **confirmam com o usuário** antes.

**Ler / achar**
- Achar conversas/interações por critério ("no WhatsApp hoje", "com humor negativo", busca
  textual) → ferramenta de **busca de interações**.
- Ver a **linha do tempo** de UM paciente (o que já rolou, quando falaram por último) →
  ferramenta de **histórico do cliente**.
- Descobrir **quem está frustrado/insatisfeito** (risco de churn) → ferramenta de **conversas
  frustradas** (dado comportamental de CX — uso legítimo é melhorar o atendimento ao titular).

**Operar o ciclo do ticket** (mudam o mundo — confirmam antes)
- **Assumir / passar a posse** de um atendimento → ferramenta de **atribuir ticket** (dar dono;
  o próprio agente pode assumir para o ticket não ficar órfão).
- **Passar para uma fila** (handoff para humanos ou outro setor; o atendimento **continua
  aberto**, sai sem dono) → ferramenta de **transferir para fila**.
- **Encerrar** um atendimento concluído (dispara a pesquisa de satisfação) → ferramenta de
  **resolver ticket**. Se ainda precisa de um humano, **transfira** em vez de resolver.
- **Deixar uma nota interna** (rastro só da equipe, nunca ao paciente) → ferramenta de
  **comentar**.

**Acompanhar sem ser dono**
- **Inscrever** um observador (pessoa ou agente) para acompanhar a conversa até um marco →
  ferramenta de **observar**. Lembre: inscrição **não** é acesso.
- **Desinscrever** quando o marco chegou ou o acompanhamento acabou → ferramenta de
  **desobservar** (o par oposto).

**Marcar a timeline da clínica**
- Registrar um **marco global** (campanha, aviso, feriado) → ferramenta de **marco na
  timeline**. ⚠️ Aparece na linha do tempo de **todos** os pacientes na janela da data —
  confirme com o usuário antes.

**Ordem mental para "cuida dessa conversa":** achar/abrir a conversa → entender o estado do
ticket → agir (assumir · comentar · transferir · resolver) → se for acompanhar, observar (e
desobservar no fim).

## Fluxos comuns

### Assumir e resolver um atendimento
1. **Ache** a conversa (busca de interações) e entenda o estado do ticket.
2. **Atribua** o ticket (a si ou a um operador) para dar dono e evitar que fique órfão.
3. Trabalhe o assunto; deixe **notas internas** (comentar) do que foi decidido — nunca vai ao
   paciente.
4. Concluído, **resolva** o ticket. Isso encerra o episódio e **dispara o CSAT**. Confirme com
   o usuário antes (é uma ação de fechamento).

### Passar para um humano / outro setor (handoff)
1. Reconheça que o caso é sensível, fora do seu escopo, ou o paciente pediu uma pessoa.
2. **Transfira para a fila** de destino (ex.: recepção, financeiro). O atendimento **continua
   aberto**, agora **sem dono** — a equipe da fila o pega pelo inbox.
3. Deixe uma **nota de handoff** (comentar) explicando o contexto para quem assumir.
4. **Transferir ≠ resolver**: se você transfere, o episódio segue vivo; não marque como
   resolvido "de brinde".

### Encerrar sem resolução (cancelar)
1. Se a conversa foi **engano/spam/duplicada** ou o **paciente sumiu**, o encerramento certo é
   **cancelar** — não resolver. Cancelar **não** dispara CSAT nem conta como atendimento
   resolvido.
2. Registre o **motivo** (é o que alimenta a auditoria). Cancelar para escapar de nota baixa
   deixa rastro — não é atalho.

### Acompanhar até um marco (observar)
1. **Inscreva** o observador (você/agente ou um gestor) na conversa, idealmente com um marco em
   mente (ex.: acompanhar até o agendamento confirmar).
2. Lembre que **observar não dá acesso**: quem observa ainda precisa do próprio direito de
   abrir a conversa.
3. Quando o marco chega (ou o acompanhamento não é mais necessário), **desobserve**. Se a
   inscrição já tinha prazo, ela some sozinha.

### Achar quem está insatisfeito (risco de churn)
1. Use a ferramenta de **conversas frustradas** para listar quem a análise de CX sinalizou.
2. Priorize: puxe o **histórico** do paciente para contexto, **assuma** o ticket e trate — ou
   **transfira** para quem tem alçada.
3. Trate como **sinal de atenção ao relacionamento**, não como veredito — a decisão do que
   fazer é humana.

### Marcar a linha do tempo da clínica
1. Para registrar um evento amplo (início de campanha de retorno, aviso de feriado), use o
   **marco na timeline**.
2. **Confirme antes**: o marco é **global** — aparece na linha do tempo de todos os pacientes
   cuja janela pegar a data. Não é um evento de um paciente só.

## Regras e invariantes
- **Conversa é eterna; ticket é episódio.** Encerrar um ticket não apaga a conversa; um novo
  contato abre um **ticket novo**, não reabre o antigo.
- **Um ticket aberto por conversa.** Um episódio de cada vez.
- **Resolver dispara CSAT; cancelar e expirar não.** Escolha o encerramento certo — cancelar é
  para "sem resolução" (com motivo), não para fugir da nota.
- **Transferir mantém aberto; resolver fecha.** Não misture handoff com fechamento.
- **Atribuir dá dono; transferir para fila tira o dono.** São movimentos opostos.
- **Nota interna nunca vai ao paciente.** Comentar é rastro de equipe; falar com o paciente é
  `designer-mensageria`.
- **Observar não é autorizar.** Inscrição só direciona eventos; o acesso ao conteúdo depende do
  próprio direito do observador (anti-vazamento). Observação pode expirar.
- **Marco de timeline é global.** Confirme antes — impacta a visão de todos os pacientes na
  janela.
- **Frustração é leitura de CX, não sentença.** Serve para priorizar atenção ao titular; a
  ação é decidida por gente.
- **Ações de estado e de contato confirmam.** Resolver, cancelar, transferir, atribuir e criar
  marco agem no mundo real — confirme com o usuário. A autorização efetiva é da plataforma.

## Limites / o que esta skill NÃO cobre
- **Escrever ou enviar a mensagem ao paciente** (texto, e-mail, HSM, disparo, checar entrega)
  → `designer-mensageria`. Esta skill cuida do **thread/fila/estado**, não do **conteúdo**.
- **Só ler a conversa para contexto**, sem operar o ciclo → `secretaria` (lê); esta **opera**.
- **Agenda e cadastro de paciente** (marcar, remarcar, ficha) → `secretaria`.
- **Pesquisa de satisfação/NPS** como instrumento (montar, reenviar, resultados) → skill de
  `pesquisas`. Aqui o CSAT é só efeito de resolver.
- **Conteúdo clínico / preço / dinheiro** → `auxiliar-medico` / `precificador` / `financeiro`.
- **Mesclar conversas/contatos duplicados**, apagar mensagens, reconfigurar filas/observação
  automática (VIP) e outras operações estruturais são administração da clínica — fora deste
  papel.
- Não expõe **como** conversas, tickets, filas e observação são construídos ou entregues por
  dentro — só **como operá-los e pensá-los**.
