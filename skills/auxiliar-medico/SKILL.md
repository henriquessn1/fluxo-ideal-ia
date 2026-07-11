---
name: auxiliar-medico
description: Apoio ao fluxo de ATENDIMENTO clínico no Fluxo Ideal — check-in do paciente, o estado/etapa em que cada atendimento está, anotações da equipe, pendências operacionais do profissional e métricas do atendimento. Use para acompanhar "onde está o paciente hoje", registrar chegada, mover o atendimento de etapa e ver a fila de trabalho. NÃO cobre o conteúdo do prontuário nem conduta clínica.
audience: [ia, humano]
depends_on: [atendimento, checkin, evolucao-operacional, pendencias]
version: 0.1.0
updated: 2026-07-10
---

# Auxiliar do atendimento clínico

Ajuda a IA a **operar o fluxo do atendimento** de uma clínica: registrar a chegada do paciente,
saber e mudar em que **etapa** cada atendimento está, deixar **anotações da equipe**, ver as
**pendências** do profissional e ler **métricas** do dia/período. É o copiloto operacional da
recepção e da equipe clínica — **não** o prontuário e **não** decide conduta médica.

## Quando usar
- "O paciente chegou" — registrar o **check-in** e criar o atendimento.
- "Onde está o Fulano agora?", "quem está em espera?", "quem está em atendimento?" — situação do dia.
- Mover um atendimento de etapa: chamar para atendimento, **finalizar**, **cancelar** (com o motivo).
- Deixar um **comentário/observação** da equipe num atendimento (recado operacional, não clínico).
- "O que ainda falta eu fazer?" — pendências do profissional (prontuários/adendos/checklist abertos).
- "Como foi o movimento?" — métricas de atendimento (totais, finalizados, cancelados, ocupação, retorno).

## Quando NÃO usar
- **Conteúdo clínico**: o que foi escrito no prontuário, evolução clínica, diagnóstico, prescrição,
  conduta — isso fica **fora** deste domínio (e fora do que a IA acessa). Nunca invente conduta.
- **Agenda e cadastro** (marcar/remarcar horário, criar/editar paciente) → skill `secretária`.
- **Preço/orçamento/venda** do que foi atendido → skill `precificador`.
- **Documentos** (receita, atestado, laudo, template) → skill `designer-documentos`.
- **Financeiro** do atendimento (cobrar, pagar, estornar) → domínio de vendas/financeiro.

## Modelo mental

Um **atendimento** é a jornada de UM paciente numa visita, do momento em que ele chega até o
encerramento. Ele nasce (ou é "aberto") no **check-in** e caminha por **etapas de estado**:

```
         check-in (chegada)
                │
                ▼
   Agendado → Em espera → Em atendimento → Finalizado
                                  │
                                  └────────────► Cancelado
                          (a qualquer momento, com motivo/tipo)
```

Ideias que sustentam o domínio:

- **O atendimento tem UM estado atual** e um **histórico de transições** (quem mudou, de quê para quê,
  quando). O estado é a "posição do paciente na fila operacional", não o conteúdo clínico.
- **Todo atendimento nasce com um serviço por trás.** Ele quase sempre vem de um agendamento; quando o
  paciente aparece **sem horário marcado** (encaixe/walk-in), a chegada precisa apontar o **serviço**
  (o item que será atendido) ou uma venda já existente — não existe atendimento clínico solto, sem o
  que está sendo atendido.
- **Finalizar e cancelar não são só "mudar um campo".** Encerrar reflete no financeiro (o que foi
  atendido vira base para cobrança) e o cancelamento carrega um **motivo/tipo** (o paciente faltou? a
  clínica cancelou? remarcou?). Por isso são ações **próprias**, distintas de simplesmente avançar de
  etapa.
- **Anotação da equipe ≠ prontuário.** Comentário é recado operacional visível à equipe
  ("paciente pediu para ser chamado pelo apelido", "atrasou 20 min"). Conteúdo clínico sensível **não**
  entra aqui — vai no prontuário, pela ferramenta clínica própria.
- **Pendência é o que ainda falta fechar**, classificada por **urgência**. É a lista de trabalho do
  profissional — sempre em **referências** (qual atendimento, qual pendência, quão urgente), nunca o
  texto clínico em si.

## Glossário
- **Atendimento**: a visita de um paciente, com estado atual + histórico, do check-in ao encerramento.
- **Check-in**: registrar que o paciente **chegou**, criando/abrindo o atendimento. É **idempotente**
  por agendamento — repetir o check-in do mesmo agendamento devolve o atendimento que já existe, não
  cria outro.
- **Walk-in / encaixe**: paciente que chega **sem horário marcado**. A chegada exige informar o
  **serviço** (o que será atendido) ou uma venda existente — a clínica não abre atendimento sem isso.
- **Etapas de estado**: `Agendado`, `Em espera`, `Em atendimento`, `Finalizado`, `Cancelado`. As três
  primeiras são a fila operacional; as duas últimas são **terminais**.
- **Finalizar**: encerrar o atendimento como concluído — reflete no que foi atendido (base do financeiro).
- **Cancelar**: encerrar sem conclusão, com **motivo** e **tipo** (ex.: paciente faltou, cancelado pelo
  cliente, cancelado pela clínica, remarcado, outro).
- **Comentário**: anotação/observação **da equipe** num atendimento (recado operacional; a autoria é de
  quem escreveu). Não é prontuário.
- **Checklist**: itens a conferir/concluir dentro de um atendimento (o que já foi feito, o que falta).
- **Acompanhante**: quem esteve presente junto com o paciente no atendimento.
- **Pendência**: algo em aberto que o profissional precisa fechar (prontuário aberto, adendo aberto,
  item de checklist não concluído), classificado por **urgência** (`urgente`, `alta`, `media`, `baixa`).
- **Retorno**: atendimento marcado como retorno de um anterior (vínculo operacional; a regra de recobrança
  é do domínio de preço).
- **Insights**: resumo textual do atendimento; parte dele é restrita por papel (só quem tem função
  clínica vê a fatia clínica). É leitura, quando a permissão permite — não é conduta a inventar.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. A **execução depende de autorização** — o MCP aplica permissão; a
> skill nunca promete acesso. Ações que mudam estado devem ser **confirmadas com o usuário** antes.

- **Registrar a chegada do paciente** (criar/abrir o atendimento) → ferramenta de **check-in**. Para
  walk-in/encaixe, lembre de informar o **serviço** ou a venda existente.
- **Ver a situação dos atendimentos** (do dia, de um período, de um paciente, ou só os **ativos agora**)
  → ferramenta de **busca** de atendimentos. Traz uma visão enxuta (estado, quem, quando) — sem detalhe
  clínico.
- **Abrir a visão 360 de UM atendimento** (detalhe + **histórico de transições de estado**; opcionalmente
  comentários, checklist, acompanhantes) → ferramenta de **contexto** do atendimento. Se uma seção não
  for permitida, ela vem marcada como sem acesso, sem derrubar o resto.
- **Mudar a etapa** (chamar para atendimento, avançar de estado; ou **finalizar**; ou **cancelar** com
  motivo/tipo) → ferramenta de **mudança de estado**. Confirme com o usuário antes.
- **Deixar uma anotação da equipe** num atendimento → ferramenta de **comentário**. Só recado
  operacional — nada de conteúdo clínico sensível.
- **Ver a minha lista de pendências** como profissional (contagens por urgência + referências) →
  ferramenta de **pendências**. Devolve **referências**, nunca o texto do prontuário.
- **Ler métricas do atendimento** (resumo por período dia-a-dia, ou o dashboard agregado) → ferramenta
  de **métricas**. O dashboard agregado pode ter algum atraso (é cacheado) — avise quando for decisão
  sensível a tempo.

**Ordem mental para "cadê o paciente / o que faço agora":** buscar (dia ou ativos-agora) → abrir o
contexto do atendimento certo → decidir a próxima etapa → mudar de estado (confirmando) → registrar
comentário se precisar.

## Fluxos comuns

### Paciente chegou (com horário marcado)
1. Localize o atendimento/agendamento do paciente (busca do dia).
2. Registre o **check-in** — o atendimento é aberto e entra na fila (`Em espera`).
3. Se o check-in do mesmo agendamento já tinha sido feito, você recebe o atendimento existente (não
   duplica) — apenas siga com ele.

### Paciente sem horário (walk-in / encaixe)
1. Faça o **check-in** informando o **serviço** que será atendido (ou uma venda existente) — sem isso a
   clínica não abre o atendimento.
2. Siga o fluxo normal de etapas.

### Chamar para atendimento e encerrar
1. Abra o **contexto** do atendimento e confira o **estado atual** (a etapa pode ter mudado desde a sua
   última leitura).
2. Avance o estado para `Em atendimento` quando o profissional receber o paciente.
3. Ao concluir, use **finalizar** (não é o mesmo que "mudar de estado" — finalizar fecha e reflete no
   que foi atendido). Confirme com o usuário.

### Cancelar / faltou
1. Confirme com o usuário o **motivo** e o **tipo** (paciente faltou? cliente cancelou? clínica cancelou?
   remarcou?).
2. Use **cancelar** com esse motivo/tipo — é uma ação própria, não um simples avanço de etapa.

### "O que ainda falta eu fazer hoje?"
1. Leia as **pendências** do profissional: contagens por **urgência** (`urgente` → `baixa`) + referências.
2. Trate primeiro as mais urgentes. Para cada referência, abra o atendimento correspondente pela ferramenta
   de contexto — mas o **conteúdo clínico** em si é resolvido na ferramenta de prontuário, fora deste domínio.

## Regras e invariantes
- **O estado pode ter mudado desde a sua leitura.** Antes de mudar de etapa, releia o **estado atual** e
  parta dele; se o sistema recusar por conflito (o estado atual não é o que você esperava), releia o
  contexto e repita a ação com o estado certo. Nunca force por cima de uma leitura velha.
- **Check-in é idempotente por agendamento** — repetir não cria um segundo atendimento.
- **Não existe atendimento sem serviço.** Walk-in exige o item atendido ou uma venda existente.
- **Finalizar e cancelar são terminais e têm consequência** (financeiro / motivo). Trate como ações
  deliberadas, sempre confirmadas — não como "avançar mais uma etapa".
- **Comentário é operacional, não clínico.** Nada de dado sensível de saúde numa anotação de equipe.
- **Pendências e a visão do profissional são referências**, nunca o conteúdo do prontuário.
- **Nunca invente conduta clínica.** Este domínio trata o **fluxo operacional** (etapas, chegada,
  pendências, métricas) — a decisão clínica é do profissional, no prontuário.
- **Toda ação depende de autorização.** Leituras podem vir parciais (uma seção sem acesso é marcada, não
  é erro); escritas podem ser negadas. A skill ensina a intenção, o MCP decide o acesso.

## Limites / o que esta skill NÃO cobre
- **Prontuário / conteúdo clínico / conduta** — fora deste domínio por design; a IA vê só o fluxo
  operacional e referências.
- **Agenda e cadastro de paciente** → skill `secretária`.
- **Preço, orçamento e venda** do que foi atendido → skill `precificador`.
- **Documentos clínicos** (receita, atestado, laudo, templates) → skill `designer-documentos`.
- **Financeiro** (cobrar/pagar/estornar) do atendimento → domínio de vendas/financeiro.
- Não expõe como o atendimento é armazenado/processado por dentro — só como **acompanhá-lo, operá-lo e
  pensá-lo**.
