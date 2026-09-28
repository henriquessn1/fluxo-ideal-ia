---
name: jornada
description: A Jornada de Cuidado (Episódio de Cuidado) do Fluxo Ideal — o caso longo do paciente (cirurgia/procedimento com etapas pré e pós) que dura semanas e não cabe no atendimento do dia. Cobre configurar o modelo de uma jornada (fases, etapas, marcos, marcas), acompanhar onde cada paciente está (fase atual, quem travou), preencher/filtrar marcas (ex.: data da cirurgia, confirmado) e operar a jornada de um paciente. Use para "montar a jornada da catarata", "onde estão meus pacientes de cirurgia?", "quem travou?", "abrir a jornada da Maria", "marcar a data da cirurgia da Maria", "quais cirurgias são desta semana?".
audience: [ia, humano]
depends_on: [jornada-cuidado, tarefas, atendimento-clinico]
version: 0.2.0
updated: 2026-09-28
---

# Jornada de Cuidado

Acompanhar e configurar o **episódio de cuidado** de um paciente — o caso longo (uma cirurgia de
catarata, um tratamento com pré-operatório, exames, autorização de convênio, cirurgia e
pós-operatório) que se estende por **semanas** e passa por **vários atendimentos**. A Jornada é a
**casca que organiza** esse caso: ela **coordena, dá visão e sinaliza pendências** — ela **não
executa** (quem executa segue sendo o atendimento, a tarefa, a venda, a agenda).

## A ideia central (leia primeiro)
Uma Jornada tem **duas camadas** — e confundir as duas é o erro clássico:

1. **O modelo ("Tipo de Jornada")** — o **molde reusável** de um tipo de caso (ex.: "Catarata").
   Define, de uma vez, as **fases** do caso, as **etapas** do quadro operacional e os **marcos** que
   toda jornada daquele tipo herda. Configura-se **uma vez**; vale para todos os pacientes daquele tipo.
2. **A jornada do paciente (a instância)** — o caso concreto de uma pessoa, que **nasce a partir do
   modelo**.

E a regra que manda em tudo: **a fase de uma jornada é sempre DERIVADA do estado dos marcos — nunca
escrita à mão.** Você não "arrasta o paciente para a fase Cirurgia"; você conclui os marcos daquela
etapa e a fase avança sozinha. Além disso, **os marcos de uma jornada SÃO tarefas** — o quadro
operacional da jornada é, por baixo, o quadro de Tarefas filtrado por aquele caso.

## Quando usar
- **Configurar/ajustar o modelo** de um tipo de jornada (montar a Catarata: fases, etapas, marcos).
- **Acompanhar** os pacientes em jornada: em que fase estão, o que falta pra avançar, **quem travou**.
- **Operar** a jornada de um paciente: abrir, encerrar, ligar um atendimento, atualizar dados.

## Quando NÃO usar
- **Marcar/remarcar uma consulta avulsa** → recepção/agenda (`secretaria`).
- **Conduzir/documentar o atendimento do dia** (evolução, adendo) → `medico`/`auxiliar-medico`.
- **Tarefa interna solta da equipe** (sem ser marco de uma jornada) → `gestor-tarefas`.
- **"Forçar" uma fase** — não existe; a fase é derivada dos marcos (ver regras).

## Modelo mental
Pense em três verbos:

- **Configurar (o modelo):** desenhar o molde — as **fases** (a régua macro: ex. Investigação →
  Pré-op → Cirurgia → Pós-op → Alta), as **etapas** operacionais (as colunas do quadro, cada uma
  ligada a uma fase) e os **marcos** de cada etapa. Antes de salvar, o modelo é **validado** para
  garantir que tudo se encaixa (uma etapa apontando para uma fase que não existe, ou um marco para
  uma etapa inexistente, deixaria o quadro quebrado). Salvar é sempre **prévia → confirmação**.
- **Acompanhar (as instâncias):** olhar o retrato — quem está em cada fase, o que falta pra avançar,
  e principalmente a **fila de pendências**: casos **parados** há dias ou com **requisito vencido**.
- **Operar (uma instância):** abrir a jornada de um paciente (que já nasce com os marcos do molde),
  ligá-la a um atendimento, encerrá-la, e mover os **marcos** (que são tarefas) — cada mudança faz a
  **fase recalcular**.

## Glossário
- **Jornada (Episódio de Cuidado):** o caso longo de um paciente; agrega vários atendimentos; tem um
  quadro próprio de fases. Coordena — não executa.
- **Tipo de Jornada (molde):** o modelo reusável de um tipo de caso (Catarata, Refrativa…). Dono das
  fases, etapas e marcos que as jornadas daquele tipo herdam.
- **Fase:** o estágio macro do caso (a régua de progresso). É **sempre derivada** dos marcos.
- **Etapa (coluna operacional):** a raia do quadro da recepção; cada etapa pertence a uma fase.
- **Marco:** o que precisa acontecer numa etapa. **É uma tarefa.** Pode ser **obrigatório** (trava o
  avanço da fase até concluir) e/ou **automático** (fecha sozinho quando o fato correspondente
  acontece na plataforma — ex.: um termo assinado, um convênio autorizado). Tem um **papel** (um
  identificador estável — é por ele que a automação mira o marco).
- **Regra de derivação:** como a fase é calculada a partir dos marcos (qual a fase inicial e a fase
  de conclusão).
- **Pendência de SLA:** um caso **parado** (sem movimento há dias) ou com um **requisito obrigatório
  vencido** — a fila proativa de "quem precisa de atenção".
- **Marca:** um **campo customizável** que a clínica define **por tipo de jornada** — uma **data**
  (ex.: data da cirurgia), um **sim/não** (ex.: confirmado), uma **seleção** (ex.: lado OD/OE), um
  **texto** ou **número**. É configuração do MODELO. Cada marca pode ser usada como **filtro** e/ou
  como **raia (swimlane)** no quadro. É distinta da **fase** (a marca é um dado que você preenche; a
  fase é derivada dos marcos).
- **Valor de marca:** o que você preenche numa jornada específica para uma marca (ex.: "data da
  cirurgia = 15/10"). Vive na jornada do paciente; editável a qualquer momento.

## Ferramentas (tarefa → ferramenta)
> A skill diz **o que existe e por quê**; as ações reais vêm das ferramentas autorizadas do MCP. Toda
> **escrita** passa por prévia + confirmação, e a Jornada é um recurso que a clínica **liga** (opt-in).

**Configurar o modelo:**
- Ver os tipos de jornada já configurados (e o resumo de cada um) → ferramenta de listagem/leitura de tipos.
- Montar/editar um modelo (fases, etapas, marcos, regra de derivação **e marcas**) → ferramenta de
  gravação do tipo. A gravação é **precedida de validação** e só grava com confirmação.
- Definir as **marcas** do tipo (os campos customizáveis: data/sim-não/seleção/texto/número, e se
  cada uma serve de filtro e/ou raia) → faz parte do mesmo modelo (o resumo do tipo já conta quantas
  marcas ele tem).
- Conferir a coerência de um modelo antes de salvar → ferramenta de **validação** (aponta referências
  quebradas — e marcas malformadas, ex.: seleção sem opções — antes que virem um quadro quebrado).

**Acompanhar:**
- Listar/buscar jornadas (por paciente, status, tipo ou fase) → ferramenta de busca de jornadas.
- **Filtrar por marca** (ex.: "cirurgias desta semana", "confirmados = sim") → a busca de jornadas
  aceita filtro por valor de marca (faixa de datas / opção / sim-não).
- Ver o detalhe de uma jornada (fase atual, o que falta, próxima fase **e os valores das marcas**) →
  ferramenta de contexto da jornada.
- Ver a fila de pendências (parados / requisito vencido) → ferramenta de pendências de SLA.

**Operar uma jornada:**
- Abrir a jornada de um paciente (já com os marcos do molde) → ferramenta de criação.
- Atualizar dados (título/tipo/profissional/convênio) **ou preencher/alterar valores de marca**
  (ex.: setar a data da cirurgia, marcar "confirmado") → ferramenta de edição. Preencha só as marcas
  que mudaram; deixe em branco (vazio) para limpar uma marca. Editável a qualquer momento.
- Encerrar (concluir) ou cancelar → ferramenta de mudança de estado.
- Ligar um atendimento à jornada → ferramenta de vínculo.
- Recalcular a fase (após mover marcos) → ferramenta de recálculo.
- Mover/concluir/destravar os **marcos** (que são tarefas) → ferramentas de Tarefas (ver `gestor-tarefas`).

## Regras e invariantes
- **A fase é sempre derivada** dos marcos — nunca setada à mão. Para mudar a fase, muda-se o estado
  dos marcos.
- **Marco = tarefa.** O quadro operacional da jornada é o quadro de Tarefas daquele caso.
- **O modelo é validado antes de salvar** — referência quebrada (etapa→fase, marco→etapa) **bloqueia**
  a gravação; recomendações apenas avisam.
- **Escrita confirma** — nada é gravado sem prévia + confirmação; e a Jornada precisa estar **ligada**
  na clínica.
- **A IA não apaga** modelo nem jornada — exclusão é ação da plataforma, não da IA.
- **Sem dado clínico** — a jornada carrega referências e progresso; o conteúdo clínico vive no
  atendimento/prontuário (fora deste papel).
- **Marca ≠ fase.** A marca é um **dado que você preenche** (data da cirurgia, confirmado); a fase é
  **derivada dos marcos**. Preencher uma marca **não** move a fase. As marcas de um tipo existem só
  se a clínica as configurou naquele modelo (nem todo tipo tem marcas).
