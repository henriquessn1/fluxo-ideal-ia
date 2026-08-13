---
name: designer-mensageria
description: A AUTORIA da comunicação da clínica com o paciente no Fluxo Ideal — desenhar os templates de mensagem (assunto + corpo com variáveis), gerir os canais (e-mail, WhatsApp) e a aprovação de HSM no provedor. Use para escrever/ajustar os textos que vão ao paciente, criar/ativar um template, gerir canais e submeter/acompanhar o HSM. Disparar de fato (enviar/programar/checar entrega) é do operador → skill `comunicacao-paciente`.
audience: [ia, humano]
depends_on: [mensagens, templates, canais, entrega]
version: 0.5.0
updated: 2026-08-13
---

# Designer de Mensageria

**Desenhar** a comunicação da clínica com o paciente: os **textos padronizados** (templates) que a
clínica usa, por quais **canais** eles saem, e a **aprovação de HSM** no provedor. É o papel de quem
cuida da "voz" da clínica — lembrete de consulta, aniversário, aviso, e-mail de rotina. **Disparar**
essa voz (enviar/programar/checar entrega) é do operador → skill `comunicacao-paciente`.

## Quando usar
- Escrever ou **ajustar o texto** de uma mensagem que vai ao paciente (assunto/corpo de um lembrete, de
  um e-mail de confirmação).
- **Criar/ativar** um template, gerir seus **canais** e a **política de remetente**.
- **Submeter um HSM** para o provedor aprovar e **acompanhar o status** dessa aprovação.
- **Deixar um template pronto para WhatsApp** quando o HSM já foi aprovado mas ele ainda não aparece
  para enviar (vincular o template ao HSM aprovado + liberar o canal).
- Descobrir **quais templates** a clínica tem e **quais variáveis** cada um espera.
- (Para **enviar / programar / checar a entrega** de fato → skill `comunicacao-paciente`.)

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

> **Você desenha o template; disparar (as duas formas acima) é do operador → `comunicacao-paciente`.**
> Conhecer as duas formas importa para desenhar bem — mas o envio em si não é deste papel.

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
- **Criar um template novo, ajustar seus metadados** (ex.: política de remetente) e **ativar/desativar**
  → a ferramenta de **autoria de template**. Prévia primeiro; grava na confirmação.
- **Gerir por quais canais** um template pode sair (permitir/bloquear um canal, ligar/desligar a versão
  de um canal) → a ferramenta de **canais do template**.
- **Ver o status de aprovação do HSM (WhatsApp)** na Meta — *aprovado, pendente ou rejeitado* → a
  ferramenta de **status HSM** (só leitura).
- **Submeter um template novo para a Meta aprovar** (em vez do Business Manager) → a ferramenta de
  **submissão de HSM**. Ela **valida as regras da Meta antes** (barra template mal-formado, protegendo a
  nota do número), roda em **prévia por padrão** e só submete com **confirmação humana**. A ferramenta de
  **listar HSM** acompanha os enviados à Meta (junto com o **status HSM**: aprovado/pendente/rejeitado).
  *Deletar* um HSM na Meta é a caminho (follow-up).
- **Deixar um template PRONTO para sair por WhatsApp** — quando o HSM já foi **aprovado** na Meta mas o
  template ainda não aparece para enviar (o status dele volta *"não vinculado"*): a ferramenta de
  **preparar WhatsApp** faz o vínculo numa tacada — casa o template com o HSM aprovado (pelo mesmo nome,
  ou um que você indique), preenche a ordem das variáveis e libera o canal WhatsApp. Roda em **prévia
  por padrão**; **só vincula a um HSM APROVADO** (se estiver pendente/rejeitado/inexistente, ela recusa
  e explica — não há como burlar a aprovação). Se o HSM estiver como **MARKETING** mas for um aviso
  transacional, ela avisa para recriá-lo como UTILITY (MARKETING fica sujeito a opt-out/limite). Use
  quando o **status HSM** diz *aprovado na Meta* mas o template não está aparecendo no "Iniciar conversa".
- **Enviar / programar / checar a entrega** de fato ao paciente **não é deste papel** — é do operador de
  envio → skill `comunicacao-paciente`. Aqui você entrega o template pronto; lá se dispara.

**Ordem mental para "ajustar/criar um template":** achar o template (slug + variáveis) → editar o
conteúdo por canal em **prévia** → conferir os `{{placeholders}}` e a política de remetente → gravar
(vale para os **próximos** envios). O **disparo** é `comunicacao-paciente`.

## Fluxos comuns

### Ajustar o texto de um e-mail ("muda o assunto do lembrete")
1. **Ache o template** e veja o conteúdo atual do canal (o detalhe mostra o corpo e as variáveis).
2. Reescreva o assunto/corpo **preservando os `{{placeholders}}`** que o envio precisa preencher.
3. Rode em **prévia** (dry-run): confira o render e a sintaxe. Variável sem valor de exemplo é só
   informativo; **erro de sintaxe** impede gravar.
4. Só então **grave**. Lembre: passa a valer para os **próximos** envios; os já enfileirados não mudam.
5. Se for um template **crítico/transacional** (verificação, código de acesso, link de assinatura,
   convite de pesquisa), redobre o cuidado — editar errado quebra automações; confirme explicitamente.

> **Enviar agora, programar mensagem automática e investigar "não chegou"** são fluxos do operador de
> envio → skill `comunicacao-paciente`.

## Regras e invariantes
- **Template é molde** — o texto final só existe **no envio**, com as variáveis preenchidas.
- **Editar template afeta o futuro, nunca o passado** — envios já disparados não mudam.
- **Cada canal tem sua versão** e o template só sai pelos **canais permitidos**.
- **Texto verificado (HSM) não vira texto livre** — em canais verificados, preencha variáveis; não
  reescreva o conteúdo aprovado (risco de phishing/bloqueio).
- **O vínculo do HSM com a Meta é sagrado** — ao ativar/desativar ou editar a versão de um canal
  verificado, a plataforma **preserva** o vínculo aprovado. Apagá-lo derruba a aprovação na Meta e o
  template **para de sair**. (Submeter/listar HSM na Meta é **por ferramenta**, com **confirmação
  humana**; deletar na Meta é a caminho.)
- **Regra de ouro do remetente** — quando escolhível, o remetente é o **e-mail do próprio usuário
  logado**; alguns templates exigem isso por política.
- **Templates críticos/transacionais** (verificação, código, link mágico, convite de pesquisa) exigem
  confirmação reforçada antes de editar — quebrá-los derruba automações.
- **Toda ação que fala com o paciente é confirmada com o usuário** antes de disparar.

## Limites / o que esta skill NÃO cobre
- Não cobre o **conteúdo dos documentos** que a mensagem carrega (receita, atestado, orçamento) →
  `designer-documentos`.
- **Enviar / programar / checar a entrega** de fato ao paciente → skill `comunicacao-paciente` (o
  operador de envio). Aqui só se **desenha** o template.
- Não cobre a **conversa/ticket** com o paciente (thread, atribuição, resolução, nota interna) →
  skill `conversas`.
- Não cobre **pesquisa de satisfação/NPS** → skill `pesquisas-satisfacao`.
- **Criar template, editar metadados (política de remetente), ativar/desativar e gerir canais** agora
  são **por ferramenta** (autoria). Continuam **fora**: **excluir** template, **envio em
  massa** (broadcast) e **anexos**. **Submeter/listar HSM na Meta** agora é **por ferramenta** (com confirmação humana); **deletar** HSM na Meta é a caminho.
- Não expõe **como** as mensagens são roteadas, enfileiradas ou entregues por dentro — só **como
  desenhá-las, dispará-las e conferi-las**.
