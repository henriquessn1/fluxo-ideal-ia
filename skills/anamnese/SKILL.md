---
name: anamnese
description: A ANAMNESE pré-consulta do Fluxo Ideal — configurar os MODELOS de questionário (por procedimento/pacote, com vários tipos de pergunta), CRIAR fichas para o paciente responder antes da consulta, e VERIFICAR o preenchimento/status (quem respondeu, por qual canal, quanto já preencheu) — SEM ler o conteúdo de saúde. Use para "cria o questionário pré-cirúrgico", "adiciona uma pergunta ao modelo X", "gera a anamnese do paciente Y", "a anamnese do agendamento Z já foi preenchida?", "quantas fichas estão pendentes?".
audience: [ia, humano]
depends_on: [anamnese, questionario-pre-consulta, ficha]
version: 0.1.0
updated: 2026-08-09
---

# Anamnese pré-consulta

Operar o **questionário que o paciente responde ANTES da consulta**: montar os **modelos**
(as perguntas, por procedimento ou pacote), **criar as fichas** para os pacientes responderem
e **acompanhar o preenchimento**. O foco é **configurar e acompanhar** — o **conteúdo clínico**
das respostas não passa por aqui (fica no prontuário/tablet).

## Quando usar
- **Criar / editar / ativar / desativar** um modelo de anamnese: as perguntas (texto livre,
  escolha única, múltipla escolha, sim/não, nota) e a que **procedimento ou pacote** ele se aplica.
- **Criar uma ficha** para um paciente responder (deixá-la pronta pro tablet da recepção ou pra
  ser preenchida no atendimento).
- "A anamnese do paciente/agendamento já foi preenchida?", "quantas fichas estão pendentes hoje?",
  "quem preencheu essa ficha e por qual canal?".

## Quando NÃO usar
- **Ler as RESPOSTAS** do paciente (o conteúdo clínico) — é dado de saúde e **não** é exposto aqui;
  fica no prontuário/atendimento. Aqui se lê **status e progresso**, nunca "o que ele respondeu".
- **Preencher / concluir** a anamnese no lugar do paciente, ou a conferência de CPF do tablet — o
  **preenchimento é do paciente** (no tablet do quiósque ou na Central, dentro do atendimento).
- **Pesquisa de satisfação / NPS** → `pesquisas-satisfacao`. Anamnese é questionário **clínico**
  pré-consulta; pesquisa é **experiência** pós-atendimento — instrumentos diferentes.
- Montar a agenda ou o catálogo de procedimentos → `secretaria` / `precificador`. Aqui só se **liga**
  um modelo a um procedimento/pacote que já existe.

## Modelo mental

Três peças, em fila — **o molde**, **a ficha do paciente** e **o quanto já foi preenchido**:

```
   MODELO (o molde do questionário)        FICHA (por paciente)                 STATUS (acompanhamento)
   perguntas + vínculo proc/pacote  →  pendente → em preenchimento → concluída  →  quem/quando/canal + progresso
                                                     └────────────→ cancelada
```

- **O modelo é por procedimento (ou pacote).** As perguntas mudam conforme o que vai ser feito —
  um pré-cirúrgico pergunta uma coisa, uma avaliação inicial outra. Um modelo pode ser **genérico**
  (sem vínculo) e servir a qualquer atendimento. Editar as perguntas **sobe a versão** do modelo, e
  cada ficha guarda a versão que respondeu (uma edição futura não altera fichas antigas).
- **A ficha é a anamnese de UM paciente.** Nasce **pendente**, ancorada no paciente (e, quando há,
  no agendamento/atendimento). Ela é **independente**: pode ser criada ao agendar, na recepção ou
  dentro do atendimento, e respondida em qualquer superfície (tablet do quiósque ou Central).
- **O ciclo de vida da ficha**: **pendente** → **em preenchimento** → **concluída**; ou **cancelada**
  (o atendimento/agendamento encerrou sem resposta, ou a ficha expirou). Uma ficha **concluída**
  nunca é cancelada.
- **O acompanhamento é status, não conteúdo.** Dá pra saber se está pendente/concluída, **quem**
  preencheu, **por qual canal** (tablet / recepção / médico) e **quanto** já foi respondido — mas
  **nunca as respostas em si**. O conteúdo clínico vive no prontuário.

## Glossário
- **Modelo (de anamnese)**: o molde do questionário — um conjunto de **perguntas** ligado a um ou mais
  **procedimentos** OU a um **pacote** (ou genérico, sem vínculo). Tem **versão** e um estado ativo/inativo.
- **Pergunta**: pode ser **texto livre**, **escolha única** (uma opção), **múltipla escolha** (várias
  opções), **sim/não** ou **nota** (escala numérica). Escolha única e múltipla exigem **opções**.
- **Vínculo**: a que **procedimento(s)** ou **pacote** o modelo se aplica — é como o sistema sabe qual
  questionário oferecer. Sem vínculo = **modelo genérico**.
- **Ficha (instância)**: a anamnese de **um** paciente, criada a partir de um modelo. Tem um **estado**.
- **Estado**: **pendente** (criada, aguardando) · **em preenchimento** · **concluída** (respondida e
  congelada) · **cancelada** (encerrada sem resposta / expirada).
- **Canal de preenchimento**: **tablet** (o próprio paciente no quiósque da recepção), **recepção** ou
  **médico** — a rastreabilidade de **quem** digitou.
- **Progresso**: quantas perguntas já foram respondidas de quantas o modelo tem — **sem** o conteúdo.

## Ferramentas (tarefa → ferramenta)
> A execução depende de **autorização** — a plataforma aplica a permissão; a skill só ensina a intenção
> e o _quando_. As **escritas pré-visualizam** (dry-run) e aplicam só após confirmar.

**Ler os modelos**
- **Ver quais modelos existem / quais perguntas tem / a que procedimento se aplica** → ferramenta que
  lista os modelos (filtra ativos/inativos) e, sob pedido, detalha um com as perguntas e os vínculos.

**Configurar o modelo (o molde — com confirmação)**
- **Criar / editar / ativar / desativar** um modelo: montar as perguntas (texto livre, escolha única,
  múltipla escolha, sim/não, nota) e ligar a **procedimento(s) ou pacote** (ou deixar genérico) →
  ferramenta de autoria do modelo. Pré-visualiza antes de gravar; trocar as perguntas **sobe a versão**.
  **Excluir** um modelo fica de fora (é feito na Central).

**Criar a ficha do paciente (com confirmação)**
- **Gerar uma anamnese pendente para um paciente responder** → ferramenta de criar ficha. O modelo é
  resolvido pelo **procedimento/pacote** do atendimento, ou você indica um modelo específico (útil pro
  genérico). A ficha nasce **pendente** e fica disponível pro tablet/Central — **não** dispara nada ao
  paciente por aqui.

**Acompanhar o preenchimento (status, sem os dados)**
- **Saber se uma anamnese já foi preenchida, quantas estão pendentes, quem preencheu e por qual canal**
  → ferramenta de verificação de fichas (filtra por paciente/agendamento/atendimento/estado). Devolve
  **estado + quem/quando/canal + progresso** — **nunca** as respostas.

**Ordem mental para "montar uma anamnese nova":** confira se já existe um modelo parecido → crie/edite
o modelo com as perguntas e o vínculo ao procedimento/pacote (pré-visualiza) → ative → daí em diante,
ao agendar/atender aquele procedimento, gere a ficha pro paciente e acompanhe o preenchimento.

## Fluxos comuns

### "Cria o questionário pré-cirúrgico"
1. Veja se já há um **modelo** parecido (evita duplicar).
2. **Crie o modelo** com as perguntas (escolha os tipos certos: sim/não pra "usa anticoagulante?",
   texto livre pra "alergias", nota pra "nível de dor") e **ligue ao procedimento** (ou pacote).
3. Pré-visualize, confirme e **ative**. Pronto — o questionário passa a valer pra aquele procedimento.

### "A anamnese do paciente X já foi preenchida?"
1. **Verifique as fichas** do paciente (ou do agendamento/atendimento).
2. Reporte o **estado** (pendente/em preenchimento/concluída/cancelada), **quem** preencheu, **por qual
   canal** e o **progresso** — sem abrir o conteúdo das respostas.

### "Gera a anamnese pro paciente responder no tablet"
1. Confirme o **procedimento/pacote** do atendimento (ou escolha um **modelo** direto).
2. **Crie a ficha** (pré-visualiza; confirme). Ela nasce **pendente** e aparece na lista do tablet da
   recepção pra o paciente preencher.

## Fronteira de privacidade (LGPD)
A anamnese é **dado de saúde** (LGPD art. 11). Por aqui você **configura** o instrumento e **acompanha**
o preenchimento — **as respostas do paciente e do médico nunca são lidas** por esta capacidade. Quem lê o
conteúdo clínico é o profissional, no prontuário/atendimento. Preencher/concluir é do **paciente** (tablet/
Central), não do assistente.
