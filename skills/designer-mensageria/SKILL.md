---
name: designer-mensageria
description: A comunicação da clínica com o paciente no Fluxo Ideal — templates de mensagem (assunto + corpo com variáveis), canais (e-mail, WhatsApp), e as duas formas de falar com o paciente: enviar AGORA por um template ou emitir uma INTENÇÃO governada (a plataforma decide quando entregar). Use para escrever/ajustar textos que vão ao paciente, disparar um e-mail, mandar um aviso automático e checar se a mensagem foi entregue.
audience: [ia, humano]
depends_on: [mensagens, templates, canais, entrega]
version: 0.1.0
updated: 2026-07-10
---

# Designer de Mensageria

Desenhar e operar a **comunicação da clínica com o paciente**: os **textos padronizados** (templates)
que a clínica usa, por quais **canais** eles saem, e como se **dispara** uma mensagem e se **confere**
que ela chegou. É o papel de quem cuida da "voz" da clínica para fora — lembrete de consulta,
aniversário, aviso, e-mail de rotina.

## Quando usar
- Escrever ou **ajustar o texto** de uma mensagem que vai ao paciente (assunto/corpo de um lembrete, de
  um e-mail de confirmação).
- **Enviar** um e-mail ao paciente usando um template pronto.
- Programar uma **mensagem automática** (lembrete, aniversário, aviso) sem duplicar em varreduras.
- Descobrir **quais templates** a clínica tem e **quais variáveis** cada um espera.
- **Checar a entrega** — "o lembrete da Maria saiu?", "por que aquele e-mail falhou?".

## Quando NÃO usar
- Redigir o **conteúdo de um documento clínico/comercial** (receita, atestado, orçamento em PDF) →
  isso é `designer-documentos`. Aqui a mensagem é o *veículo* (o e-mail que carrega o link), não o
  documento.
- Conduzir a **conversa** com o paciente (thread, ticket, atribuir/transferir/resolver atendimento,
  nota interna) → é o domínio de **conversas/tickets** (reporte à skill correspondente; não é esta).
- Pesquisa de satisfação / NPS (convite, reenvio, resultados) → skill de **pesquisas**.
- Notificações **internas** in-app à equipe (aviso na tela) — isto aqui é comunicação **ao paciente**,
  não avisos internos.

## Modelo mental

A mensageria separa **o que se diz** (template) de **como e quando se entrega** (canal + disparo). Três
peças e duas formas de falar:

```
TEMPLATE (o texto padronizado)
  slug (apelido) · descrição · política de remetente
  └─ por CANAL: assunto + corpo com {{variaveis}}
         (o corpo tem "buracos" que o envio preenche na hora)

CANAIS: e-mail (ativo) · WhatsApp · outros
  cada template diz por quais canais pode sair

           DUAS FORMAS DE FALAR COM O PACIENTE
     ┌──────────────────────────┬───────────────────────────┐
     ▼                          ▼
  ENVIAR AGORA               INTENÇÃO GOVERNADA
  (e-mail imediato)          (a plataforma decide QUANDO)
  você escolhe destinatário  para mensagens AUTOMÁTICAS
  + template + variáveis     (lembrete, aniversário, aviso):
  → sai já                   • chave de idempotência (não duplica)
                             • fora do horário → agenda p/ expediente
                             • respeita o teto diário da clínica
                                       │
                                       ▼
                              ENTREGA (assíncrona)
                    na fila → enviando → entregue | falhou → re-tenta | falha definitiva
```

Ideias que sustentam tudo:

- **Template é molde, não a mensagem final.** O texto tem **variáveis** (`{{nome}}`, `{{data}}`…) que
  só ganham valor **no envio**. Editar o template muda **todos os próximos** envios dele — nunca os já
  disparados.
- **O mesmo template tem versões por canal.** O que sai por e-mail pode diferir do que sairia por
  WhatsApp; cada canal tem seu assunto/corpo. Um template só sai pelos canais que ele **permite**.
- **"Enviar por intenção" ≠ "enviar agora".** Para mensagem **automática** (as que uma rotina dispara
  em massa: lembrete do dia, aniversário), você declara a **intenção** e a plataforma resolve o resto —
  não reenvia o que já mandou (idempotência), não incomoda fora de hora (agenda para o expediente) e
  respeita o **teto diário**. Para um e-mail pontual, você **envia agora**.
- **A entrega é assíncrona.** Disparar ≠ entregar. A mensagem entra numa fila e um processo a envia;
  por isso existe o passo de **checar entrega**, com re-tentativas automáticas antes de desistir.
- **Texto verificado vs texto livre (WhatsApp/HSM).** Em canais como o WhatsApp, o provedor só entrega
  mensagens fora da janela de conversa se o **template foi previamente aprovado** (o HSM). O texto é
  "verificado": você preenche variáveis, mas **não** escreve texto livre por cima do que foi aprovado —
  texto livre sob um remetente verificado é vetor de phishing e pode ser barrado. Trate campos
  derivados de um agendamento/documento como **preenchimento**, não como redação nova.
- **Regra de ouro do remetente.** Quando um envio permite escolher o remetente, ele tem de ser o
  **e-mail do próprio usuário logado** — não se envia "em nome de" terceiros. Alguns templates exigem
  remetente próprio por política.

## Glossário
- **Template**: texto padronizado e reutilizável, identificado por um **slug** (apelido curto e
  estável, ex.: `lembrete-consulta`). Tem uma **descrição** e uma **política de remetente**.
- **Slug**: o apelido do template — é por ele que você o encontra e o referencia num envio.
- **Versão por canal**: o **assunto + corpo** do template **para um canal específico** (e-mail,
  WhatsApp…). É o que você edita quando "ajusta o texto".
- **Variável / placeholder**: os `{{campos}}` do corpo preenchidos **no envio** (ex.: nome do paciente,
  data da consulta). O template lista quais espera; faltar valor no molde não impede editar — o envio
  real é que preenche.
- **Canal**: por onde a mensagem sai (e-mail é o ativo; WhatsApp e outros existem no modelo). Um
  template só sai pelos canais **permitidos** para ele.
- **HSM / template aprovado (WhatsApp)**: mensagem-modelo pré-aprovada pelo provedor para poder ser
  enviada fora da janela de conversa. Conteúdo **verificado**: preenche-se variável, não se reescreve.
- **Enviar (agora)**: dispara **um** e-mail real, na hora, para um destinatário, usando um template.
- **Intenção (de envio) governada**: forma de emitir mensagem **automática**; a plataforma decide
  **quando** entregar, com idempotência, janela de horário e teto diário.
- **Idempotência / chave de idempotência**: um identificador que garante que a **mesma** intenção não
  seja entregue duas vezes (uma varredura diária pode repetir a chamada; a chave impede duplicar).
  Nunca coloque dado pessoal na chave.
- **Política de remetente**: `livre` (qualquer remetente configurado) ou **exige próprio** (o envio
  precisa sair do e-mail do próprio usuário logado).
- **Entrega assíncrona**: a mensagem é enfileirada e enviada por um processo em segundo plano — o
  resultado se confere depois.
- **Status de entrega**: *na fila* → *enviando* → **entregue** ao provedor; ou **falhou** (vai
  re-tentar, com espera crescente entre tentativas) e, esgotadas as tentativas, **falha definitiva**.
- **Prévia (dry-run)**: renderizar o template com valores de exemplo **sem gravar nem enviar** — valida
  a sintaxe e mostra como vai ficar.

## Ferramentas (tarefa → ferramenta)
> Ensine a **intenção** e o **quando**. A execução depende de **autorização** — a plataforma aplica
> permissão; a skill nunca promete acesso.

- **Descobrir quais templates existem / achar o slug / ver as variáveis esperadas** → a ferramenta que
  **lista templates** (com a opção de detalhe, que mostra o conteúdo por canal e os placeholders). É o
  **pré-requisito** de qualquer envio e de qualquer edição.
- **Ajustar o texto (assunto/corpo) de um template existente** → a ferramenta que **edita o conteúdo do
  template** — sempre em **prévia primeiro** (valida e mostra o render sem gravar); grava só na
  confirmação. Muda os **próximos** envios daquele template.
- **Enviar um e-mail pontual ao paciente agora** → a ferramenta de **envio de e-mail**: escolha o
  destinatário (o paciente cadastrado, cujo contato a plataforma resolve, **ou** um endereço direto), o
  template e as variáveis. É **ação real** — confirme com o usuário antes.
- **Programar uma mensagem automática (lembrete/aniversário/aviso)** → a ferramenta de **intenção de
  envio**: informe o template, o destinatário e uma **chave de idempotência** (para não duplicar). A
  plataforma decide o momento (agenda fora de hora, respeita o teto diário).
- **Saber se a mensagem chegou / por que falhou** → a ferramenta de **checagem de entrega**, com o
  identificador que o envio devolveu. Ela mostra o estado atual e o histórico de tentativas.

**Ordem mental para "mandar uma mensagem":** achar o template (slug + variáveis) → decidir *agora* vs
*intenção governada* → conferir destinatário/remetente → disparar → **checar a entrega**.

## Fluxos comuns

### Ajustar o texto de um e-mail ("muda o assunto do lembrete")
1. **Ache o template** e veja o conteúdo atual do canal (o detalhe mostra o corpo e as variáveis).
2. Reescreva o assunto/corpo **preservando os `{{placeholders}}`** que o envio precisa preencher.
3. Rode em **prévia** (dry-run): confira o render e a sintaxe. Variável sem valor de exemplo é só
   informativo; **erro de sintaxe** impede gravar.
4. Só então **grave**. Lembre: passa a valer para os **próximos** envios; os já enfileirados não mudam.
5. Se for um template **crítico/transacional** (verificação, código de acesso, link de assinatura,
   convite de pesquisa), redobre o cuidado — editar errado quebra automações; confirme explicitamente.

### Enviar um e-mail agora ao paciente
1. **Ache o template** e as variáveis que ele espera.
2. Escolha o destinatário: o **paciente** (a plataforma resolve o contato) **ou** um **endereço
   direto** — um dos dois.
3. Preencha as variáveis; se o template exige **remetente próprio**, use o e-mail do próprio usuário.
4. **Confirme com o usuário** (é e-mail real, não idempotente — duas chamadas mandam dois e-mails) e
   dispare.
5. **Cheque a entrega** com o identificador retornado.

### Programar mensagem automática (lembrete/aniversário)
1. **Ache o template** apropriado.
2. Emita a **intenção** com uma **chave de idempotência** determinística (ex.: um marcador do evento +
   a data — **sem dado pessoal na chave**), para que uma varredura repetida **não duplique**.
3. Confie na plataforma para o **quando**: fora do horário da clínica a mensagem é **agendada** para o
   expediente; se o **teto diário** estourou, ela **não** é enviada (a resposta diz qual caso ocorreu).

### Investigar "não chegou"
1. Pegue o **identificador** do envio.
2. **Cheque a entrega**: *na fila/enviando* = ainda em curso; **entregue** = saiu ao provedor;
   **falhou** = há re-tentativas em andamento; **falha definitiva** = esgotou — leia o histórico de
   tentativas para o motivo.
3. Confirme premissas: o template **existe e está ativo**? O destinatário tem contato válido? A
   política de remetente foi respeitada?

## Regras e invariantes
- **Template é molde** — o texto final só existe **no envio**, com as variáveis preenchidas.
- **Editar template afeta o futuro, nunca o passado** — envios já disparados não mudam.
- **Cada canal tem sua versão** e o template só sai pelos **canais permitidos**.
- **Enviar ≠ entregar** — a entrega é assíncrona; sempre há um passo de **checagem** (com
  re-tentativas antes de desistir).
- **Intenção governada é para o automático** — idempotência **obrigatória** (não duplica), respeita
  **horário** e **teto diário**. Envio pontual é o "agora"; não confunda os dois.
- **Nunca coloque dado pessoal na chave de idempotência.**
- **Texto verificado (HSM) não vira texto livre** — em canais verificados, preencha variáveis; não
  reescreva o conteúdo aprovado (risco de phishing/bloqueio).
- **Regra de ouro do remetente** — quando escolhível, o remetente é o **e-mail do próprio usuário
  logado**; alguns templates exigem isso por política.
- **Templates críticos/transacionais** (verificação, código, link mágico, convite de pesquisa) exigem
  confirmação reforçada antes de editar — quebrá-los derruba automações.
- **Toda ação que fala com o paciente é confirmada com o usuário** antes de disparar.

## Limites / o que esta skill NÃO cobre
- Não cobre o **conteúdo dos documentos** que a mensagem carrega (receita, atestado, orçamento) →
  `designer-documentos`.
- Não cobre a **conversa/ticket** com o paciente (thread, atribuição, resolução, nota interna) → skill
  de conversas/tickets.
- Não cobre **pesquisa de satisfação/NPS** → skill de pesquisas.
- Não cobre **criação/exclusão de template**, mudança de metadados (política de remetente,
  ativar/desativar), gestão de quais canais são permitidos, envio em massa (broadcast) nem anexos —
  isso é administração estrutural feita na interface da clínica.
- Não expõe **como** as mensagens são roteadas, enfileiradas ou entregues por dentro — só **como
  desenhá-las, dispará-las e conferi-las**.
