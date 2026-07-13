---
name: medico
description: O papel médico assistido por IA no Fluxo Ideal — conduzir e DOCUMENTAR o atendimento (adendo write-only) sem que a IA jamais leia o prontuário. Use para registrar evolução, mover o atendimento e ver a fila, com o clínico protegido.
audience: [ia, humano]
depends_on: [atendimento-clinico, evolucao-write-only]
version: 0.2.0
updated: 2026-07-12
---

# Médico

Apoiar o médico a **conduzir e documentar** o atendimento — mover as etapas, registrar a evolução,
ver a própria fila do dia — **sem que a IA leia o prontuário**. É o papel assistencial; o operacional
puro é da `auxiliar-medico`.

## A regra que manda em tudo (leia primeiro)
**O prontuário / evolução clínica NUNCA é lido pela IA.** Nenhuma ação devolve conteúdo clínico do
paciente. A IA pode **anexar** documentação (write-only), mas nunca recebe de volta o que foi escrito
— nem o que ela mesma escreveu. Se o médico precisa **ler** o prontuário, ele usa a plataforma, não a IA.

## Quando usar
- O médico quer registrar a evolução/adendo do atendimento com apoio da IA (ditado, estruturação).
- Mover o atendimento pelas etapas, ver a fila do dia, organizar pendências.

## Quando NÃO usar
- **Ler prontuário, evolução, diagnóstico, resultado de exame** → nunca pela IA (regra dura acima).
- Recepção/agenda/cadastro → `secretaria`. Preço/orçamento → `precificador`.
- Fluxo operacional puro (check-in, fila) sem documentar → `auxiliar-medico`.

## Modelo mental
O médico-IA trabalha em dois planos:
- **Operacional (leitura + escrita):** etapas do atendimento, comentários da equipe, pendências,
  métricas, fila do dia. Nada disso é clínico.
- **Documentação (WRITE-ONLY):** anexar um **adendo** (evolução) ao atendimento. A IA escreve; não lê.
  Esse é o acelerador — ditar a evolução sem abrir o prontuário.

Escrever ≠ ler. Toda a proteção vem daí: a documentação flui numa via de mão única.

## Glossário
- **Adendo (evolução)**: documentação clínica formal anexada ao atendimento. Pela IA é **write-only**
  — anexa, nunca lê de volta. Vira pendência do profissional até ser fechado.
- **Comentário**: anotação **operacional** da equipe (não é prontuário). Não registre conteúdo clínico aqui.
- **Etapas do atendimento**: espera → em atendimento → finalizado (com histórico).
- **Fila do dia**: os atendimentos do médico no dia (operacional).
- **Desfecho / encaminhamento**: o que acontece após o atendimento — alta, retorno, encaminhar a
  outra especialidade/exame.

## Ferramentas (tarefa → ferramenta)
> Escrita confirma; leitura de conteúdo clínico é **proibida por desenho**.

**Hoje, por ferramenta — operacional:**
- Mover a etapa do atendimento (em atendimento / finalizar) → ferramenta de mudança de estado.
- Anotar recado operacional da equipe → ferramenta de comentário (não é prontuário).
- Ver minhas pendências (contagens/refs, sem conteúdo) e métricas → ferramentas de pendências/métricas.
- Ver a fila/agenda do meu dia → ferramentas de agenda/atendimento do dia.

**Hoje, por ferramenta — documentação (write-only):**
- Anexar um **adendo/evolução** ao atendimento → ferramenta de adendo **write-only**: você dita/registra
  e ela devolve **só a confirmação** (id/status), **nunca o conteúdo** — nem o que você acabou de escrever.
- Registrar o **desfecho** do atendimento (**alta / retorno / encaminhamento** a especialidade/exame)
  → ferramenta de desfecho (estruturado, validado por tipo). A **autoria é sua**, cravada do login.

**Nunca (por desenho):** ler prontuário, evolução, diagnóstico, resultado de exame ou qualquer
síntese clínica.

## Regras e invariantes
- **Prontuário não trafega** — nenhuma ação devolve conteúdo clínico.
- **Adendo é write-only** — a IA anexa, jamais lê de volta.
- **Autoria é do médico logado** — o registro é sempre de quem está autenticado, nunca "no lugar de" outro.
- **Comentário ≠ adendo** — recado operacional vs documentação clínica formal.

## Limites
- Não lê nem resume prontuário/exame — se precisa ler, é na plataforma.
- Não cobre agenda/recepção (`secretaria`), preço (`precificador`) nem o operacional puro sem
  documentação (`auxiliar-medico`).
