---
name: comunicacao-paciente
description: O envio GOVERNADO de mensagens ao paciente no Fluxo Ideal — usar um template pronto para mandar um e-mail pontual agora, ou emitir uma INTENÇÃO governada (a plataforma decide quando entregar, com quiet-hours, teto diário e idempotência), e checar se chegou. É o operador da comunicação: usa os templates, não os cria. Use para "manda a confirmação pro paciente", "programa o lembrete do dia", "esse e-mail chegou?".
audience: [ia, humano]
depends_on: [mensagens, entrega, canais]
version: 0.2.0
updated: 2026-11-21
---

# Comunicação com o paciente

Operar o **canal de saída** da clínica para o paciente: pegar um **template pronto** e efetivamente
**mandar** — um e-mail pontual agora, ou uma mensagem **automática** que a plataforma entrega na hora
certa — e depois **conferir a entrega**. É o **operador** da mensageria: usa a "voz" que o
`designer-mensageria` desenhou; não redige nem cria template. Fala com o paciente **só por template
aprovado**, nunca por texto livre.

## Quando usar
- **Enviar um e-mail agora** ao paciente com um template pronto (confirmação, um aviso pontual).
- **Programar uma mensagem automática** (lembrete de consulta, aniversário, aviso) sem duplicar.
- **Checar a entrega** — "o lembrete da Maria saiu?", "por que aquele e-mail falhou?".
- Descobrir **qual template** usar e **quais variáveis** ele espera, antes de disparar.

## Quando NÃO usar
- **Escrever/ajustar o texto** de um template, criar/ativar um, gerir canais ou HSM → skill
  `designer-mensageria` (a autoria). Aqui você **usa** o template pronto; lá se **desenha**.
- **Conduzir a conversa** (thread, ticket, atribuir/transferir/resolver, nota interna) → skill
  `conversas`. Aqui é o **disparo governado de saída**, não o diálogo.
- **Convite de pesquisa** (reenviar/antecipar) → skill `pesquisas-satisfacao` (tem o próprio disparo).
- O **conteúdo do documento** que a mensagem carrega (receita, orçamento em PDF) → `designer-documentos`.
- Notificação **interna** in-app à equipe — aqui é comunicação **ao paciente**.

## Modelo mental

Há **duas formas de falar** com o paciente, e a **entrega é sempre assíncrona**:

```
        ESCOLHER O TEMPLATE (pronto, com {{variaveis}})
                     │
        ┌────────────┴─────────────┐
        ▼                          ▼
   ENVIAR AGORA               INTENÇÃO GOVERNADA
   (e-mail imediato)          (a plataforma decide QUANDO)
   destinatário + template    para mensagens AUTOMÁTICAS
   + variáveis → sai já       (lembrete, aniversário, aviso):
   NÃO é idempotente          • chave de idempotência (não duplica)
   (2 chamadas = 2 e-mails)   • fora de hora → agenda p/ o expediente
                              • respeita o teto diário
                     │
                     ▼
              ENTREGA (assíncrona)
   na fila → enviando → entregue | falhou → (re-tenta, se a clínica ligou) → falha definitiva
```

Ideias que sustentam tudo:

- **Só template aprovado — nunca texto livre.** Você preenche as **variáveis** de um template pronto;
  não redige texto novo por cima. Em canais verificados (WhatsApp/HSM), texto livre sob remetente
  verificado é vetor de **phishing** e é barrado. Trate campos vindos de um agendamento/documento como
  **preenchimento**, não redação.
- **"Enviar agora" ≠ "intenção governada".** Para um e-mail **pontual**, você **envia agora** (sai na
  hora e **não é idempotente** — duas chamadas mandam dois e-mails; confirme antes). Para mensagem
  **automática** (as que uma rotina dispara: lembrete do dia, aniversário), você declara a **intenção**
  e a plataforma resolve o **quando**: não reenvia o que já mandou (idempotência), não incomoda fora de
  hora (agenda para o expediente) e respeita o **teto diário**.
- **Disparar ≠ entregar.** A mensagem entra numa fila e um processo a envia; por isso existe o passo de
  **checar a entrega**. Nova tentativa automática só existe se a clínica a ligou.
- **Regra de ouro do remetente.** Quando o envio permite escolher o remetente, ele é o **e-mail do
  próprio usuário logado** — nunca "em nome de" terceiros. Alguns templates exigem remetente próprio.
- **Falar com o paciente é outward-facing.** O paciente recebe de verdade — **confirme com o usuário**
  antes de disparar.

## Glossário
- **Template**: o texto padronizado (assunto + corpo com `{{variaveis}}`), identificado por um **slug**.
  Você o **usa**; quem o cria/edita é o `designer-mensageria`.
- **Variável / placeholder**: os `{{campos}}` preenchidos **no envio** (nome, data…). O template lista
  quais espera.
- **Enviar (agora)**: dispara **um** e-mail real, na hora, para um destinatário, com um template. **Não**
  é idempotente.
- **Intenção (de envio) governada**: forma de emitir mensagem **automática**; a plataforma decide
  **quando** entregar, com idempotência, janela de horário e teto diário.
- **Chave de idempotência**: identificador que garante que a **mesma** intenção não seja entregue duas
  vezes (uma varredura diária pode repetir a chamada). **Nunca** coloque dado pessoal na chave.
- **Quiet-hours / teto diário**: a plataforma não entrega fora do horário da clínica (agenda para o
  expediente) e não ultrapassa o limite diário de mensagens.
- **HSM (WhatsApp)**: template pré-aprovado pelo provedor para sair fora da janela de conversa —
  conteúdo **verificado** (preenche variável, não reescreve).
- **Status de entrega**: *na fila* → *enviando* → **entregue** ao provedor; ou **falhou**. Depois de
  **falhou**, só há nova tentativa automática **se a clínica ligou a retentativa** (vem desligada) — e aí a
  checagem diz **para quando** ela está agendada. Sem retentativa agendada, nada sai sozinho: é
  **reenviar** pela origem. Quando o provedor **recusa o pedido** (template ou parâmetros que ele não
  aceita), é **falha definitiva** na hora — retentar repetiria o erro. Esgotadas as tentativas, também
  **falha definitiva**.

## Ferramentas (tarefa → ferramenta)
> Ensine a **intenção** e o **quando**. A execução depende de **autorização** — a plataforma aplica
> permissão; a skill nunca promete acesso. Falar com o paciente é **outward-facing** → confirme antes.

- **Achar o template e ver as variáveis que ele espera** → a ferramenta que **lista templates** (com
  detalhe por canal). É o **pré-requisito** de qualquer envio.
- **Enviar um e-mail pontual agora** → a ferramenta de **envio de e-mail**: escolha o destinatário (o
  paciente cadastrado, cujo contato a plataforma resolve, **ou** um endereço direto), o template e as
  variáveis. **Ação real, não idempotente** — confirme com o usuário.
- **Programar uma mensagem automática** (lembrete/aniversário/aviso) → a ferramenta de **intenção de
  envio**: informe o template, o destinatário e uma **chave de idempotência**. A plataforma decide o
  momento (agenda fora de hora, respeita o teto).
- **Saber se a mensagem chegou / por que falhou** → a ferramenta de **checagem de entrega**, com o
  identificador que o envio devolveu (estado atual + histórico de tentativas).

**Ordem mental para "mandar uma mensagem":** achar o template (slug + variáveis) → decidir *agora* vs
*intenção governada* → conferir destinatário/remetente → disparar (confirmando) → **checar a entrega**.

## Fluxos comuns

### Enviar um e-mail agora ao paciente
1. **Ache o template** e as variáveis que ele espera.
2. Escolha o destinatário: o **paciente** (a plataforma resolve o contato) **ou** um **endereço direto**.
3. Preencha as variáveis; se o template exige **remetente próprio**, use o e-mail do próprio usuário.
4. **Confirme** (é e-mail real e **não** idempotente — duas chamadas mandam dois) e dispare.
5. **Cheque a entrega** com o identificador retornado.

### Programar mensagem automática (lembrete/aniversário)
1. **Ache o template** apropriado.
2. Emita a **intenção** com uma **chave de idempotência** determinística (ex.: um marcador do evento + a
   data — **sem dado pessoal na chave**), para que uma varredura repetida **não duplique**.
3. Confie na plataforma para o **quando**: fora do horário → **agendada** para o expediente; **teto**
   estourado → **não** envia (a resposta diz qual caso ocorreu).

### Investigar "não chegou"
1. Pegue o **identificador** do envio.
2. **Cheque a entrega**: *na fila/enviando* = em curso; **entregue** = saiu ao provedor; **falhou** com
   nova tentativa agendada = aguarde o horário que a checagem mostra; **falhou** sem tentativa agendada =
   nada sai sozinho, **reenvie** pela origem (confirmando com o usuário); **falha definitiva** = esgotou ou
   o provedor recusou o pedido — leia o histórico para o motivo (recusa do provedor costuma ser template
   ou variável errada: veja com quem desenha o template, skill `designer-mensageria`).
3. Confirme premissas: o template **existe e está ativo**? O destinatário tem contato válido? A política
   de remetente foi respeitada?

## Regras e invariantes
- **Só template aprovado — nunca texto livre.** Preenche-se variável; não se reescreve o conteúdo
  (risco de phishing/bloqueio em canais verificados).
- **Enviar ≠ entregar.** A entrega é assíncrona; sempre há um passo de **checagem**.
- **"Falhou" não promete nova tentativa.** Só re-tenta sozinho se a clínica ligou a retentativa e a
  checagem mostra o horário; senão, reenviar. Pedido recusado pelo provedor é falha definitiva.
- **"Enviar agora" não é idempotente** (duas chamadas = dois e-mails; confirme). **Intenção governada é
  para o automático** e a chave de idempotência é **obrigatória**.
- **Nunca coloque dado pessoal na chave de idempotência.**
- **A plataforma governa o quando** — quiet-hours e teto diário não se contornam por aqui.
- **Regra de ouro do remetente** — quando escolhível, é o **e-mail do próprio usuário logado**.
- **Toda ação que fala com o paciente é confirmada** antes de disparar (outward-facing).
- **Não se autoria aqui.** Criar/editar template, canais e HSM é `designer-mensageria`.

## Limites / o que esta skill NÃO cobre
- **Desenhar o template** (texto, canais, HSM, política de remetente) → `designer-mensageria`.
- **A conversa/thread** com o paciente (ticket, atribuição, resolução, nota interna) → `conversas`.
- **Convite de pesquisa** (reenviar/antecipar) → `pesquisas-satisfacao`.
- **Texto livre autônomo** ao WhatsApp e **envio em massa/broadcast** ficam **fora** — só template
  governado, com humano no loop.
- Não expõe **como** as mensagens são roteadas/enfileiradas por dentro — só **como dispará-las
  (governado) e conferi-las**.
