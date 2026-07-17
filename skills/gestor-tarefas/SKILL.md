---
name: gestor-tarefas
description: As TAREFAS INTERNAS da equipe da clínica no Fluxo Ideal — o quadro de afazeres da operação (ligar pro fornecedor, revisar o convênio, imprimir formulários) e, cada vez mais, o TECIDO que conecta a operação: a tarefa virou cidadã de primeira classe e aparece no contexto (na agenda do dia, no check-in, na ficha do paciente/atendimento/agendamento), além do quadro próprio. Criar/editar uma tarefa, atribuir, movê-la pelo quadro, gerir vínculos e impedimentos (resolver o impedimento destrava a conclusão), comentar/ver a atividade, privatizar/arquivar, o board agregado e "minhas pendências". Use para "cria uma tarefa pra…", "o que eu tenho pra fazer?", "passa pro Fulano", "resolve o impedimento e conclui", "que tarefas tem esse paciente/agendamento?", "como está o quadro?".
audience: [ia, humano]
depends_on: [tarefas-internas]
version: 0.3.0
updated: 2026-07-17
---

# Gestor de tarefas internas

Operar o **quadro de afazeres da equipe** de uma clínica: o trabalho interno a fazer que
**não** é atender um paciente nem conversar com ele — comprar material, cobrar um retorno de
convênio, organizar a agenda da semana, revisar um cadastro. Este papel **cria** a tarefa, dá a
ela um **dono**, move-a pelas colunas do quadro e mostra a lista de pendências de quem trabalha.
É a lista de "to-do" da operação, não o prontuário e não a conversa.

E, cada vez mais, a tarefa é o **tecido que conecta a operação**: ela deixou de viver só num quadro à
parte e virou **cidadã de primeira classe** — aparece **no contexto onde importa** (na agenda do dia,
no check-in, na ficha do paciente/atendimento/agendamento) e é o material de que **outros fluxos** são
feitos (os **marcos de uma jornada SÃO tarefas** — ver `jornada`). Continua sendo to-do **interno**;
o que mudou é que ela **vem até você** no lugar certo, além de ter o board próprio.

## Quando usar
- "Cria uma tarefa pra ligar pro laboratório amanhã", "anota pra comprar luvas".
- "O que eu tenho pra fazer hoje?" / "minhas pendências" — a lista de trabalho da pessoa.
- "Passa essa tarefa pro Fulano" / "assume isso pra mim" — dar ou trocar o responsável.
- "Move pra em andamento", "marca como concluída" — andar com a tarefa pelo quadro.
- "Quais tarefas estão atrasadas / urgentes / sem dono?" — buscar e filtrar o quadro.
- Vincular a tarefa a **algo do sistema** (um paciente, um atendimento, um orçamento) só como
  **referência de contexto** ("resolver a pendência do orçamento do cliente X").

## Quando NÃO usar
- **Pendência clínica do atendimento** (prontuário aberto, adendo, checklist do profissional,
  "o que falta fechar na consulta") → skill `auxiliar-medico`. Aquilo é trabalho **dentro** de um
  atendimento; aqui é afazer **da operação**.
- **Ticket / fila da conversa com o paciente** (atender, transferir, resolver um atendimento por
  WhatsApp) → skill `conversas`. Um ticket é um episódio de conversa; uma tarefa é um to-do interno.
- **Pendência comercial/financeira como número do negócio** (orçamentos a vencer, retornos a
  cobrar, contas a pagar) → skills `precificador` / `financeiro`. Você pode **criar uma tarefa**
  que aponte pra um desses itens, mas o item em si vive no domínio dele.
- **Desenhar/acompanhar o caso longo do paciente** (cirurgia com etapas pré/pós, fases) → skill
  `jornada`. Lá os **marcos** de uma jornada **são tarefas** — você as **opera** por aqui (mover,
  concluir, destravar), mas o **desenho** do caso (fases, etapas, quando o marco fecha) é da `jornada`.
- **Agenda, cadastro de paciente, mensagem ao paciente** → `secretaria` / `conversas` /
  `designer-mensageria`.

## A tarefa é transversal — aparece onde o trabalho está

A tarefa é **cidadã de primeira classe** da operação: além do quadro próprio, ela **aparece no
contexto onde importa**, sem obrigar ninguém a abrir o board.

- **Na agenda do dia e no check-in** — cada compromisso sinaliza se tem tarefa pendente (um contador);
  dá pra abrir o painel, **criar já vinculada** (ao agendamento **e** ao paciente) e **concluir** ali mesmo.
- **Na ficha do paciente, do atendimento e do agendamento** — um painel lateral lista as tarefas
  **daquele contexto**, com ações rápidas (iniciar/concluir) e o **prazo** em destaque quando atrasa.
- **Dois recortes naturais** ao surgir num contexto: as **daquela entidade** (deste agendamento/
  atendimento) e as **do paciente** (todas as abertas dele) — **sem duplicar**: uma tarefa ligada ao
  agendamento **e** ao paciente conta **uma só**.
- **É o tecido que conecta** — a mesma tarefa pode ser o **marco de uma jornada** (`jornada`), o
  afazer atrelado a um orçamento, ou o lembrete de um retorno. O **vínculo** (abaixo) é o que faz a
  tarefa aparecer no lugar certo. O quadro geral continua existindo; o que mudou é que a tarefa também
  **vem até você** no contexto.

## Modelo mental

Uma **tarefa** é um afazer interno que anda por um **quadro de três colunas**:

```
        A FAZER  ──────►  EM ANDAMENTO  ──────►  CONCLUÍDA
        (to-do)          (alguém tocando)       (feito — terminal)
           ▲                                         │
           └─────────────── reabrir ◄───────────────┘
                    (voltar de concluída limpa a conclusão)

   quem faz:   DONO (um responsável — pessoa OU bot)  ·  SEM DONO (ninguém pegou ainda)
   trava:      IMPEDIMENTO aberto (bloqueada / aguardando algo)  → não deixa concluir
   contexto:   VÍNCULO a um paciente/atendimento/agendamento/orçamento/venda (só referência)
   alcance:    PÚBLICA (a equipe vê)   ·   PRIVADA (só o destinatário — configurada na tela)
```

Ideias que sustentam o domínio:

- **Tarefa é to-do interno, não trabalho de paciente.** Ela existe pra organizar a **operação**
  da clínica. Se o "afazer" é conteúdo de um atendimento ou uma conversa com o paciente, ele
  pertence a outro domínio — aqui entra no máximo como uma tarefa que **aponta** pra ele.
- **Três estados, e "concluída" é terminal (mas reabrível).** A tarefa nasce em **a fazer**, vai
  pra **em andamento** quando alguém pega, e termina em **concluída**. Voltar de concluída
  **reabre** (limpa o registro de conclusão). Mover pro mesmo estado não faz nada (é idempotente).
- **Dono é opcional e pode ser um bot.** Uma tarefa pode ficar **sem dono** (ninguém assumiu) ou
  ter **um** responsável — que pode ser uma **pessoa** ou um **agente/bot** da clínica. Atribuir
  dá dono; desatribuir devolve ao "sem dono". Trocar o dono de uma tarefa de outra pessoa é um ato
  deliberado — **confirme** antes.
- **Impedimento trava a conclusão — e resolvê-lo destrava.** Uma tarefa pode carregar um
  **impedimento** aberto (**bloqueada por** algo ou **aguardando** alguém); enquanto ele estiver
  aberto, **não dá pra concluir**. **Resolver o impedimento** (agora por ferramenta) libera a
  conclusão — isso é **tratar o bloqueio**, não "forçar" a conclusão por cima dele. Continua não
  havendo atalho de pular um impedimento sem resolvê-lo.
- **Comentário e atividade dão a história da tarefa.** Além dos campos, a tarefa tem uma **trilha**:
  comentários livres da equipe e um **log automático** do que aconteceu (mudou de dono, de estado…).
  É rastro interno — nunca vai ao paciente e respeita a mesma privacidade (tarefa privada de outro não se vê).
- **Vínculo é referência, não posse — e é o que faz a tarefa aparecer no contexto.** Ligar uma
  tarefa a um paciente, atendimento, agendamento, orçamento ou venda é só **contexto** ("essa tarefa
  é sobre aquilo") — ajuda a achar, a entender e a **surgir na ficha/agenda daquele item**. **Não**
  dá acesso ao item vinculado nem move nada nele. Uma tarefa pode ter **mais de um** vínculo (ex.:
  do agendamento **e** do paciente) — e ainda assim conta como **uma**.
- **Pública por padrão; privada é da tela.** Uma tarefa nasce **pública** (a equipe enxerga).
  Torná-la **privada** (visível só ao destinatário) é uma ação da interface da clínica, não deste
  papel. Tarefa privada de **outra** pessoa é invisível — nem aparece na busca, nem abre no detalhe
  (some por privacidade, indistinguível de inexistente).

## Glossário
- **Tarefa**: um afazer interno da equipe (título + descrição opcional), com um estado no quadro,
  prioridade e, talvez, prazo, dono, vínculos e impedimentos.
- **Estado / coluna**: onde a tarefa está no quadro — **a fazer**, **em andamento**, **concluída**.
  As duas primeiras são "aberto"; **concluída** é terminal (reabrível).
- **Prioridade**: a urgência declarada — **baixa**, **média** (padrão), **alta**, **urgente**.
- **Prazo**: a data-limite (opcional). Vencido e ainda não concluída = **atrasada** — um sinal para
  priorizar, não uma mudança de estado.
- **Responsável / dono**: quem cuida da tarefa (um só). Pode ser uma **pessoa** ou um **bot**.
  Sem responsável = **sem dono**.
- **Impedimento**: o que trava a tarefa — **bloqueada por** (depende de outra coisa/tarefa) ou
  **aguardando** (esperando algo/alguém). Aberto, impede a conclusão até ser resolvido.
- **Vínculo**: uma referência de contexto a uma entidade de outro domínio — **cliente**,
  **atendimento**, **agendamento**, **orçamento** ou **venda**. Só aponta; não dá acesso.
- **Visibilidade**: **pública** (a equipe vê) ou **privada** (só o destinatário). Nasce pública;
  privar é ação da tela.
- **Minhas pendências**: minhas tarefas ainda **abertas** (a fazer + em andamento), o ponto de
  partida pra "o que eu faço agora", com destaque para as **atrasadas**.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. A execução depende de **autorização** — a plataforma aplica
> permissão; a skill nunca promete acesso. Ações que mudam o quadro **confirmam com o usuário** antes.

**Ler / achar**
- **"O que eu tenho pra fazer?"** (minhas tarefas abertas, com as atrasadas em destaque) → use a
  ferramenta de **minhas pendências**. É o ponto de partida do dia.
- **Buscar/filtrar o quadro** (por estado, prioridade, minhas, responsável, prazo, se está
  bloqueada, ou por vínculo a um paciente/atendimento/etc.) → use a ferramenta de **busca de
  tarefas**. Traz uma lista enxuta (sem a descrição completa).
- **Abrir o detalhe de UMA tarefa** (descrição completa + vínculos + impedimentos) → use a
  ferramenta de **detalhe da tarefa**, com o id vindo da busca. Se a tarefa for privada de outra
  pessoa, ela simplesmente "não existe" pra você.
- **A visão do quadro agregada** (quantas em cada coluna — o placar) → ferramenta de **board**
  (contagem por estado, com preview opcional).
- **A trilha de uma tarefa** (comentários + log do que aconteceu) → ferramenta de **atividades da tarefa**.

**Operar o quadro** (mudam o mundo — confirmam antes)
- **Criar uma tarefa** (entra em "a fazer", pública) → ferramenta de **criar tarefa**. Título é
  obrigatório; prioridade, prazo, dono e vínculos são opcionais. Para atribuir a si, use a própria identidade.
- **Editar** os campos de uma tarefa (título, descrição, prioridade, prazo…) → ferramenta de **editar tarefa**.
- **Atribuir / trocar / tirar o dono** → ferramenta de **atribuir tarefa**. Tirar o dono é **explícito**
  (anti-acidente); confirme antes de reatribuir tarefa de terceiro.
- **Mover pelo quadro** (a fazer ↔ em andamento ↔ concluída) → ferramenta de **mudar estado**. Concluir
  **com impedimento aberto falha** — **resolva o impedimento** (abaixo) e conclua. Voltar de concluída reabre.
- **Gerir impedimentos** — abrir (bloqueada/aguardando) ou **resolver** (⭐ resolver **destrava** a
  conclusão) → ferramenta de **impedimentos**.
- **Gerir vínculos** — apontar/retirar a referência a um paciente/atendimento/orçamento/venda → ferramenta
  de **vínculos** (só contexto; não dá acesso ao item).
- **Comentar** na tarefa (nota da equipe na trilha) → ferramenta de **comentar**.
- **Privatizar** (torná-la visível só ao destinatário — **gated**, confirme; some da visão da equipe) →
  ferramenta de **privatizar**; **arquivar** uma tarefa encerrada → ferramenta de **arquivar**.

**Ordem mental para "cuida das tarefas":** ver **minhas pendências** (ou buscar) → abrir o **detalhe**
da tarefa certa → decidir → **criar / atribuir / mover** (confirmando).

## Fluxos comuns

### Criar e encaminhar uma tarefa
1. **Crie** a tarefa com um título claro (e descrição/prazo/prioridade se fizer sentido). Ela nasce
   em **a fazer**, pública. Confirme com o usuário antes de criar.
2. Se já se sabe quem faz, **atribua** o responsável no ato (ou depois). Sem dono, ela fica no quadro
   esperando alguém pegar.
3. Se a tarefa é sobre algo do sistema (um orçamento, um paciente), **vincule** para dar contexto —
   é só referência, não muda nada no item vinculado.

### "O que eu tenho pra fazer hoje?"
1. Puxe **minhas pendências** — as abertas (a fazer + em andamento), com as **atrasadas** destacadas.
2. Comece pelas **atrasadas** e pelas de prioridade **urgente/alta**.
3. Para cada uma, abra o **detalhe** se precisar do texto completo e dos impedimentos.

### Andar com uma tarefa
1. Ao começar, **mova** de "a fazer" para "em andamento" (assuma como dono se ainda não tiver).
2. Ao terminar, **mova** para "concluída". Se falhar por **impedimento aberto**, veja o que trava,
   **resolva o impedimento** (por ferramenta) e conclua — resolver o bloqueio destrava; não há como
   pular um impedimento sem resolvê-lo.
3. Se ficou algo pendente numa tarefa recém-concluída, dá pra **reabrir** (voltar de concluída).

### Passar a tarefa pra outra pessoa
1. Confirme com o usuário para quem vai.
2. **Atribua** o novo responsável (pode ser pessoa ou bot). Isso troca o dono.
3. Se a intenção é deixá-la **sem dono** (devolver ao quadro), use a **desatribuição explícita** —
   não passe um responsável em branco por acidente.

## Regras e invariantes
- **Tarefa é to-do interno.** Não é pendência clínica (`auxiliar-medico`), nem ticket de conversa
  (`conversas`), nem pendência comercial/financeira (`precificador`/`financeiro`) — no máximo
  **aponta** pra eles por vínculo.
- **Três estados; concluída é terminal e reabrível.** Mover pro mesmo estado é idempotente; voltar
  de concluída limpa a conclusão.
- **Impedimento aberto trava a conclusão; resolvê-lo destrava.** Resolver o impedimento (por ferramenta)
  libera a conclusão — é tratar o bloqueio, não forçar por cima. Pular um impedimento sem resolvê-lo não existe.
- **Comentário/atividade é rastro interno.** Comentar deixa nota na trilha da equipe; o log automático
  registra as mudanças. Nunca vai ao paciente e respeita a privacidade da tarefa.
- **Dono é opcional e pode ser bot.** Atribuir dá dono; a desatribuição é **explícita** (anti-acidente).
- **Vínculo é só contexto.** Aponta pra uma entidade de outro domínio; **não** concede acesso a ela
  nem altera nada nela.
- **Privacidade é opaca — na leitura E na escrita.** Tarefa privada de outra pessoa não aparece na
  busca, não abre no detalhe e **também não pode ser editada por ID** — dá "não existe" em qualquer
  caminho (a ação corre com a identidade de quem chama). Privatizar é **gated** (some da visão da equipe).
- **Ações que mexem no quadro confirmam.** Criar, atribuir e mover agem no mundo real — confirme com
  o usuário. A autorização efetiva é da plataforma; a skill só ensina a intenção.

## Limites / o que esta skill NÃO cobre
- **Pendência clínica do atendimento** (prontuário, adendo, checklist, insights) → `auxiliar-medico`.
- **Ticket / fila / estado da conversa com o paciente** → `conversas`.
- **Orçamentos a vencer, retornos a cobrar, contas a pagar** como número do negócio →
  `precificador` / `financeiro` (uma tarefa pode só **referenciar** esses itens).
- **Agenda, cadastro de paciente, mensagem ao paciente** → `secretaria` / `designer-mensageria`.
- **Editar em massa** (mexer em muitas tarefas de uma vez) e **apagar** uma tarefa não são deste papel —
  aqui se opera **uma** por vez. (Privatizar, arquivar, board, impedimentos, vínculos e comentários
  **agora são** por ferramenta.)
- Não expõe **como** as tarefas são armazenadas ou processadas por dentro — só **como criá-las,
  operá-las e pensá-las**.
