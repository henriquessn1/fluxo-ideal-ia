---
name: reportar-e-sugerir
description: Como a IA reporta um BUG ou sugere uma MELHORIA do próprio sistema Fluxo Ideal (de suavizar um atrito a apontar uma capacidade que falta, como estoque ou folha de pagamento) — e acompanha o desfecho. É a ponte de qualidade: cada report vira um registro estruturado no backlog do time. Reportar é SEGURO e não conserta nada (cai numa fila de revisão). Use quando encontrar um erro/resultado incorreto ao operar uma ferramenta, tiver uma ideia de melhoria, ou quiser saber o que aconteceu com o que você reportou.
audience: [ia, humano]
depends_on: [feedback, qualidade, melhoria-continua]
version: 0.1.3
updated: 2026-07-14
---

# Reportar problema (bug / sugestão)

A ponte de **qualidade** entre a IA que opera o sistema e o time que o constrói. Quando você
(a IA) encontra um **erro** ao usar uma ferramenta/tela, ou percebe um **atrito** que poderia
melhorar, você **registra** isso — e cada registro vira um item estruturado no backlog do time
Fluxo Ideal. É o multiplicador silencioso: muitas IAs em muitas clínicas exercitando o sistema o
tempo todo, cada tropeço virando conhecimento acionável.

## Quando usar
- Você **operou uma ferramenta e deu errado**: erro, resultado incorreto, comportamento inesperado
  (ex.: "a ferramenta de gravar devolveu o registro **sem o campo que enviei**", "o total do relatório
  **não bateu** com a soma dos itens", "a ação **retornou erro** mesmo com um filtro válido").
- Você percebeu uma **melhoria**: um atrito a suavizar (um passo automatizável, uma informação que
  faltou, um filtro ausente) — **ou uma parte nova do sistema** que a clínica precisaria e que **não
  existe** (ex.: controle de estoque, folha de pagamento dos colaboradores, comissões).
- Você quer **saber o desfecho** de um bug/sugestão que **você** reportou antes (foi corrigido?
  o time precisa de mais info?).

## Quando NÃO usar
- **Dúvida de uso** ("como eu faço X?") — não é bug; resolva pela skill do papel, não reporte.
- **Problema do PACIENTE ou clínico** (uma reclamação do paciente, um atendimento a tratar) — isso
  é um **ticket/atendimento** → skill `conversas`. Aqui é problema **do sistema**, não da pessoa.
- **Pedir suporte humano na hora** — reportar é assíncrono (entra numa fila de revisão), não é um
  canal de socorro imediato.

## Modelo mental

Reportar é **registrar evidência**, não pedir conserto na hora:

```
   você encontra um bug / tem uma ideia
                 │
                 ▼
        REPORTA (com evidência)  ──►  fila de REVISÃO do time
                 │                         (não vai direto a ninguém)
                 │                          triar → resolver → responder
                 ▼
        CONSULTA O DESFECHO  ◄────────────  o time devolve o status
        (resolvido? corrigido? precisa + info?)
```

Ideias que sustentam tudo:

- **Você reporta do seu ponto de vista: a FERRAMENTA.** Você opera o sistema por **ferramentas**
  (não pelas telas da Central), então seus reports são quase sempre sobre **comportamento de
  ferramenta**: um resultado errado, um **campo que sumiu na resposta**, um **filtro que falta**, ou
  ter que **encadear duas ferramentas** para o que devia ser uma. Descreva assim — não em "cliques de
  tela" que você nem usa.
- **Reportar ≠ consertar.** Seu report **não** corrige o problema nem vira uma tarefa por mágica —
  ele entra numa **fila de revisão** onde o time classifica e decide. Não prometa ao usuário que
  "já foi corrigido"; prometa que "foi registrado".
- **Bug exige evidência: o que ESPERAVA × o que ACONTECEU.** Um bug sem isso não é acionável. Diga
  o resultado que você esperava e o que de fato veio — é o coração de um report útil.
- **Zero PII — sempre.** **Nunca** coloque dado de paciente no report: nome, CPF, telefone, e-mail,
  conteúdo de mensagem, nada clínico. Descreva o **comportamento**, não o dado ("ao salvar um
  paciente com convênio, o campo X sumiu" — não *qual* paciente). A plataforma higieniza na borda,
  mas escreva limpo por princípio.
- **É uma ação SEGURA.** Reportar não muda nada no mundo, não toca o paciente, não move dinheiro —
  é só um registro. Pode reportar sem cerimônia (não precisa de confirmação pesada). É de propósito:
  o valor está em **muitos** reports honestos.
- **Você fecha o próprio loop.** Dá pra consultar o desfecho dos **seus** reportes — e, quando um
  bug seu foi **corrigido**, re-verificar no campo se realmente resolveu.

## Glossário
- **Bug**: um erro/resultado incorreto/comportamento inesperado **do sistema** ao operar uma
  ferramenta ou tela.
- **Sugestão de melhoria**: uma ideia de como o sistema poderia ser melhor — de **suavizar um atrito**
  do que já existe (automação, informação que falta, filtro ausente) a **uma parte nova** que ainda
  não existe (ex.: controle de estoque, folha de pagamento).
- **Evidência**: num bug, o par **esperado × obtido** (o que deveria ter acontecido × o que
  aconteceu). O que torna o report acionável.
- **Severidade**: o quão grave é o bug — de leve a crítico. Ajuda o time a priorizar.
- **Fila de revisão**: onde os reports caem para o time **triar** (classificar → resolver →
  responder). Não é um humano específico; é o backlog central de qualidade.
- **Desfecho / status do report**: a resposta curada que volta do time — *resolvido*, *corrigido*,
  *não será feito*, *preciso de mais informação*, *aviso*, *é assim mesmo (FAQ)* — com um recado e
  se **virou uma tarefa** de backlog.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. Reportar é uma ação **segura e universal** — está disponível a
> qualquer papel. A execução depende de **autorização** como qualquer outra.

- **Reportar um bug** → a ferramenta de **reporte de bug**. Exige a **evidência**: descreva o que
  **aconteceu** e o que você **esperava**. Ajuda muito informar a **área** afetada (ex.: agenda,
  vendas, atendimento), a **ferramenta/rota**, os **passos** para reproduzir e a **severidade**. **Sem
  PII.**
- **Sugerir uma melhoria** → a ferramenta de **sugestão** — de um **atrito a suavizar** a uma
  **capacidade nova** que falta no sistema (ex.: estoque, folha de pagamento). Descreva a ideia e, se
  souber, a **área** a que se aplica. Sem PII.
- **Acompanhar o que você reportou** → a ferramenta de **status dos seus reportes**. Devolve **só os
  seus**, com o desfecho curado (corrigido / não será feito / precisa de info…) e se virou tarefa.

**Ordem mental para "isso deu errado":** confirme que é **bug do sistema** (não dúvida de uso, não
problema do paciente) → junte a **evidência** (esperado × obtido, onde, passos) → **reporte** (sem
PII) → depois, se quiser, **consulte o desfecho**.

## Fluxos comuns

### Reportar um bug bem-feito
1. Confirme que é mesmo um **bug do sistema** (uma ferramenta/tela que se comportou errado) — não
   uma dúvida de como usar, nem um problema do paciente.
2. Monte a **evidência**: o que você **esperava** que acontecesse × o que **aconteceu**; em qual
   **área/ferramenta**; e os **passos** para reproduzir, se der.
3. Escolha a **severidade** com honestidade (um total errado de dinheiro é mais grave que um rótulo
   torto).
4. **Reporte** — sem nenhum dado de paciente no texto. O sistema confirma o registro (não a correção).
5. Diga ao usuário que **foi registrado** (não que "já foi corrigido").

### Sugerir uma melhoria
1. Descreva a **ideia** de forma concreta. Dois tipos valem — os dois são ouro:
   - **Suavizar um atrito** do que já existe, **do jeito que você opera** (por ferramenta, não por
     tela): *"para achar um atendimento eu preciso buscar o paciente primeiro e depois cruzar — seria
     melhor buscar o atendimento direto pelo nome do paciente"*, ou *"a ferramenta de busca não tem
     filtro por período, então trago tudo e filtro na mão"*.
   - **Uma parte NOVA do sistema** que ainda não existe — uma capacidade que a clínica precisaria e
     para a qual **não há ferramenta**: *"não há como controlar o estoque de materiais"*, *"faltaria
     uma folha de pagamento dos colaboradores"*, *"seria útil um controle de comissões"*. Você opera o
     sistema todo dia — quando percebe um **buraco de capacidade**, sinalizar é dos feedbacks mais
     valiosos que existem.
2. Aponte a **área**, se souber (ou diga que é **capacidade nova**). Sem PII.
3. **Sugira**. Vira um registro para o time avaliar.

### Acompanhar / re-verificar
1. Use a ferramenta de **status dos seus reportes** para ver o desfecho do que você mandou.
2. Se o time respondeu **preciso de mais informação**, complemente com um novo report claro.
3. Se um bug seu foi **corrigido**, **re-verifique no campo** (refaça o passo) para confirmar que
   resolveu de verdade — e, se não resolveu, reporte de novo com a nova evidência.

## Regras e invariantes
- **Bug exige evidência.** Sempre o par **esperado × obtido** — sem isso, o report não é acionável.
- **Nunca PII.** Nenhum dado de paciente no texto do report (nome, CPF, contato, conteúdo, clínico).
  Descreva o comportamento, não a pessoa.
- **Reportar ≠ consertar.** Cai numa fila de revisão; não promete correção nem cria tarefa por si só.
- **Não use para dúvida de uso** nem para **problema do paciente** (isso é `conversas`) — é problema
  **do sistema**.
- **É ação segura** — não muda o mundo, não toca o paciente. Reporte sem medo; o valor está no volume
  honesto.
- **Você só vê os SEUS reportes** ao consultar o desfecho (não os de outros).

## Limites / o que esta skill NÃO cobre
- **Suporte humano imediato** — reportar é assíncrono (fila de revisão), não um socorro na hora.
- **Reclamação/atendimento do paciente** → skill `conversas` (é um ticket, não um bug de sistema).
- **Consertar o bug ou abrir a tarefa você mesmo** — o time tria e decide; seu papel é registrar
  bem.
- **Ver reportes de outras IAs/pessoas** ou o backlog interno — você acompanha só o que **você**
  reportou.
- Não expõe **como** o report é roteado/armazenado por dentro — só **como registrá-lo bem e
  acompanhá-lo**.
