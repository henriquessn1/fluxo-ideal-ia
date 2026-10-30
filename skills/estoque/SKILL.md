---
name: estoque
description: O estoque rastreável da clínica no Fluxo Ideal — saldo por unidade e local, lote/validade e nº de série, FEFO, consumo de material no paciente e vínculo de implante (etiqueta da RDC 556/2021, UDI da classe IV), material consignado com prazo, reserva para procedimento agendado e alertas de validade/mínimo. Use para "quanto tem da lente X na unidade Y?", "o que vence este mês?", "lança o material da cirurgia", "reserva a prótese para amanhã", "quais implantes esse paciente recebeu?".
audience: [ia, humano]
depends_on: [estoque-rastreavel, consumo-material, implantes, consignado, reservas-material, alertas-estoque]
version: 0.1.0
updated: 2026-10-30
---

# Estoque

Consultar e operar o **estoque rastreável** da clínica — qualquer especialidade: o que existe, **onde**
(unidade e local), **de que lote e validade** ou **qual nº de série**, o que **saiu para qual paciente**,
o que é **do fornecedor** (consignado), o que está **reservado** para um procedimento e o que **vai vencer
ou faltar**. O estoque é a fonte da verdade do saldo; o catálogo (preço, cadastro do produto) é da
`precificador`.

## Quando usar
- "Quanto tem de X?", "onde está?", "o que vence até o fim do mês?", "o que está abaixo do mínimo?".
- Dar entrada de material, transferir entre locais, emprestar, contar (ajuste), registrar perda/vencimento.
- Lançar o material usado no paciente (no procedimento ou no atendimento) e corrigir um lançamento.
- Ver os **implantes** de um paciente (rastreabilidade), completar o **UDI** de um implante classe IV.
- Reservar material para um agendamento, ver e liberar reservas (inclusive as órfãs).
- Operar o **consignado**: remessa, devolução ao fornecedor, consumo para o fornecedor faturar, listagem de OPME.

## Quando NÃO usar
- Cadastrar o produto, mudar o preço, o modo de controle ou as marcações (implantável, consignável, classe de
  risco…) → skill `precificador` (é o **catálogo**). O estoque só **lê** o cadastro.
- Ler prontuário, evolução ou conduta → nunca pela IA (ver `medico`). O vínculo de implante é rastreabilidade do
  material, não conteúdo clínico.
- Pagar o fornecedor, conta a pagar → `financeiro`. Faturar material no convênio (TISS) → `faturamento-convenio`.
- Mudar o comportamento do time de avisos do estoque → `designer-agentes`.

## Modelo mental

```
 catálogo (produto: modo de controle · implantável · consignável · classe de risco · registro ANVISA)
        │  o estoque lê
        ▼
 UNIDADE ── LOCAL (padrão da unidade · outros · consignado = exclusivo do fornecedor)
        │
        ▼
 SALDO por produto × local × lote (e por dono: próprio ou a remessa do fornecedor)
        │                     ▲
        │ movimentos (kardex) │ entrada · transferência · empréstimo/devolução · ajuste · perda ·
        │ imutáveis           │ consumo · remessa/devolução ao fornecedor · estorno
        ▼
 físico − reservado = DISPONÍVEL ──► consumo no paciente (FEFO) ──► vínculo de implante (prontuário)
        │
        └─► alertas: validade vencida/próxima · abaixo do mínimo · prazo do consignado
```

Quatro ideias sustentam tudo:
- **O saldo é derivado dos movimentos.** Ninguém digita o saldo: ele resulta do **kardex** (o extrato de
  movimentos), e movimento **nunca se apaga** — corrige-se com **estorno** (o movimento inverso).
- **O produto diz como ele é controlado.** Por **quantidade**, por **lote** (com validade) ou por **nº de
  série** (uma unidade = uma série). Isso decide o que a entrada e a saída exigem.
- **Disponível ≠ físico.** O físico é o que está no local; a **reserva** para um agendamento não é movimento,
  só separa: **disponível = físico − reservado**. O consumo e as outras reservas só usam o disponível.
- **O total do produto que aparece no catálogo é projeção do estoque.** O "estoque" e o "estoque baixo" que o
  catálogo mostra vêm daqui (com um pequeno atraso); o detalhe por local, lote e mínimo está aqui.

## Glossário

**Onde e quanto**
- **Unidade**: o estabelecimento da clínica (matriz, filial). Uma é a **unidade principal** — usada quando a
  unidade do atendimento ou da venda não é conhecida.
- **Local**: onde o material fica dentro da unidade (estoque principal, sala, armário). Toda unidade tem um
  **local padrão**. Um **local consignado** só guarda material do fornecedor.
- **Saldo / físico**: quanto há num local (por lote e por dono). Nunca fica negativo.
- **Reservado**: o que está separado para agendamentos. **Disponível** = físico − reservado.
- **Kardex (extrato)**: a lista de movimentos de um produto, do mais novo ao mais antigo, com quem lançou.

**Como o produto é controlado**
- **Modo de controle**: *quantidade* (sem lote nem série), *lote* (cada entrada tem número e **validade**;
  a saída sai de um lote) ou *série* (cada unidade tem um **nº de série** único). Não muda com saldo no estoque.
- **FEFO** ("primeiro que vence, primeiro que sai"): sem lote escolhido, a saída pega o lote de validade mais
  próxima, dividindo entre lotes se precisar. **Lote vencido é bloqueado** para consumo, reserva e baixa da
  venda — ele sai do estoque por **perda (vencimento)**.
- **Implantável**: produto que fica no paciente (lente intraocular, prótese, stent…). O consumo dele cria um
  **vínculo de implante**.
- **Classe de risco** (I a IV): vem do registro ANVISA do produto; **nunca se infere**.

**Paciente**
- **Consumo**: o material usado num atendimento — ligado ao **ato** (o procedimento executado) ou ao
  atendimento como um todo ("Materiais do atendimento"). Cada linha vira um movimento de saída.
- **Vínculo de implante**: o registro do que foi implantado em quem — nome/modelo, fabricante, código, lote ou
  série, registro ANVISA, data e, quando houver, o **UDI**. Guardado pelo prazo do prontuário (20 anos).
- **Etiqueta de rastreabilidade (RDC 556/2021)**: implantáveis de **classe III e IV** trazem etiquetas para o
  prontuário, o paciente e a cobrança; o vínculo guarda esses dados e pode receber a **foto da etiqueta**.
- **UDI** (identificação única do dispositivo, em duas partes: a do modelo e a da produção): **obrigatório só
  na classe IV** (RDC 591/2021) — um item por unidade. Na classe III é opcional (ex.: a lente intraocular é
  classe III).
- **Entrega pendente**: produto **vendido** que não pôde baixar sozinho (controlado por série, implantável,
  sem saldo ou lote vencido) — a equipe escolhe a série/lote (e o UDI) e entrega.

**Fornecedor (consignado)**
- **Consignado**: material do fornecedor guardado na clínica, que só vira compra quando é usado. É opcional
  — a clínica liga na configuração do estoque.
- **Remessa**: a chegada de material consignado, com a NF de remessa do fornecedor. Não tem custo nem gera
  conta a pagar.
- **Prazo do consignado**: cada remessa tem **até quando usar** — data da remessa + prazo da clínica (padrão
  **180 dias**, Ajuste SINIEF 2/2024). Mudar o prazo na configuração não mexe nas remessas já recebidas.
- **Consumo para o fornecedor**: o relatório do que foi usado, para o fornecedor faturar e repor; cada linha
  fica *aguardando* ou *reposta*.
- **Listagem de OPME**: o saldo consignado atual por fornecedor, que o Fisco pode pedir.

**Agenda e avisos**
- **Reserva**: material separado para um **agendamento** — por quantidade (o lote é escolhido no consumo) ou
  por série (aquela unidade). A data e a unidade vêm do agendamento.
- **Reserva órfã**: reserva ativa cuja data do agendamento já passou — liberar.
- **Mínimo**: por **produto × local** (0 = sem mínimo). "Abaixo do mínimo" = físico do local ≤ mínimo.
- **Alerta**: lote vencido, lote perto de vencer, abaixo do mínimo, consignado com prazo vencido ou perto do
  prazo. Calculado na hora; a antecedência (padrão 30 dias) é configuração do estoque.

## Ferramentas (tarefa → ferramenta)
> A execução depende de **autorização** — o MCP aplica permissão; a skill ensina a intenção e o _quando_.
> Toda escrita mostra uma **prévia** primeiro: mostre-a, **confirme com o usuário** e só então grave.

**Achar o produto primeiro.** As ferramentas do estoque aceitam o produto pelo **nome ou código** e o
resolvem no catálogo. Se mais de um produto casar, **pergunte qual** (mostre as opções) — não escolha.
Para achar o local, use a ferramenta de configuração. Buscar pelo nome exige também a leitura do catálogo.

**Ver (acesso de leitura do estoque)**
- "Quanto tem? onde? o que vence até tal data?" → ferramenta de **saldo**: linhas por produto × local × lote
  (próprio ou consignado, validade, prazo da remessa). Com um produto, traz o **resumo**: total, reservado,
  **disponível por local**, mínimo/abaixo do mínimo e séries disponíveis.
- "O que aconteceu com esse produto?" → ferramenta de **extrato** (kardex). Sem dado de paciente.
- "O que está vencendo / faltando?" → ferramenta de **alertas** (por tipo, com severidade e dias restantes);
  na mesma ferramenta, a visão dos **mínimos** por local com o físico atual.
- Configuração do estoque e os **locais** de cada unidade → ferramenta de **configuração**.

**Gerir (acesso de gestão do estoque)**
- Configurar o estoque (unidade principal, consignado ligado/prazo, antecedência dos alertas), criar/editar
  locais e **definir o mínimo** de um produto num local → ferramenta de **gestão da configuração**.
- **Movimentar** → ferramenta de **movimentação**: entrada, transferência entre locais, empréstimo (a quem) e a
  devolução dele, **ajuste** (informe a quantidade **contada**; o sistema lança a diferença), **perda** (perda,
  vencimento ou avaria) e **estorno** de um movimento. Entrada, transferência, empréstimo e entregas pedem o
  acesso de **movimentar**; ajuste, perda e estorno pedem o de **ajustar** (mais restrito).
- **Entregas pendentes** da venda → ferramenta de entregas pendentes (listar) e a movimentação (entregar com
  série/lote e UDI, ou cancelar).

**Paciente (acesso de consumo no paciente)**
- Antes de lançar, peça a **sugestão FEFO** (lotes ou séries disponíveis no local da unidade) e, se houver
  agendamento, o que foi **reservado** para ele → ferramenta de **consumo** (leitura). A mesma ferramenta lista
  os consumos de um atendimento, ato, venda ou paciente (exige um filtro).
- **Lançar** o material (tudo ou nada) ou **estornar** um consumo inteiro ou só algumas linhas → ferramenta de
  **lançamento de consumo**. Uma nova tentativa automática não duplica a baixa.
- **Implantes** de um paciente (pelo identificador do paciente) → ferramenta de **implantes**.

**Agenda (acesso de reserva)**
- Ver as reservas de um agendamento ou de um produto, inclusive as **órfãs** → ferramenta de **reservas**.
- Reservar (tudo ou nada) ou liberar com motivo → ferramenta de **gestão de reservas**.

**Fornecedor (acesso ao consignado)**
- Remessas (abertas, perto do prazo), uma remessa, o **consumo para o fornecedor** e a **listagem de OPME** →
  ferramenta do **consignado**. O relatório pela IA vem **sem identificar o paciente** (só o atendimento).
- Registrar a remessa, devolver ao fornecedor e marcar consumo como **reposto** → ferramenta de **operação do
  consignado**. Com o consignado desligado, a ferramenta avisa — ligar é da gestão.

**Fora da IA:** marcar um alerta como "já avisado" é do time de avisos; anexar a **foto da etiqueta** do
implante é pela tela.

## Fluxos comuns

### "Quanto tem da lente +22 na unidade Centro?"
1. Ache o produto pelo nome (pergunte se vier mais de um).
2. Peça o saldo com o resumo: responda pelo **disponível** daquele local/unidade e diga o reservado à parte.
3. Se for por lote, diga as validades; se for por série, quantas séries estão livres.

### "Lança o material da cirurgia"
1. Confirme o atendimento, o paciente e, se houver, o ato e o agendamento.
2. Peça a sugestão FEFO (com o agendamento, ela já traz o que estava reservado).
3. Monte os itens: no modo **lote**, use o lote sugerido ou o lido na embalagem; no modo **série**, as séries
   que saíram. **Nunca invente** lote, série, validade ou UDI — pergunte.
4. Implantável **classe IV**: exija o **UDI** e mande **uma linha por unidade**. Classe III: UDI se tiver.
5. Mostre a prévia, confirme e lance. Com o agendamento, as reservas dele viram consumo.
6. Errou? Estorne o consumo (ou só a linha) com motivo — o estorno genérico de movimento não serve para consumo.
   Ato cancelado ou excluído estorna o material dele sozinho.

### "Reserva a prótese para o agendamento de amanhã"
1. Ache o agendamento e o produto; o local padrão é o da unidade do agendamento.
2. Por quantidade (o lote é escolhido no consumo) ou por série (aquela unidade). Faltando disponível, o pedido
   inteiro é recusado com o que há.
3. Agendamento cancelado, com falta ou excluído libera a reserva sozinho. **Reagendado para outra unidade**: a
   reserva por quantidade muda de local; a de série fica e pede **transferência** antes do procedimento.
4. Reserva órfã (data passada) → liberar com motivo.

### "Chegou material consignado"
1. Confira que o consignado está ligado e que existe um **local consignado** na unidade.
2. Registre a **remessa**: fornecedor, local consignado, NF de remessa e itens no modo de controle do produto.
   O prazo de uso sai sozinho (data + prazo da clínica).
3. No uso, o consumo é o normal, escolhendo o **local consignado**.
4. Para o fornecedor faturar: o relatório de consumo; quando ele repõe, marque como **reposto** (com a NF).
   O que não foi usado volta por **devolução ao fornecedor**, antes do prazo.

### "O que vence este mês?" / "O que está faltando?"
1. Peça os alertas (ou o saldo com "vence até").
2. Responda por severidade: vencido primeiro (sai por perda/vencimento), depois perto de vencer e abaixo do
   mínimo. Sugira **transferir** de outro local antes de dizer que falta.
3. O time **estoque-avisos** (se instalado) já avisa a equipe 1×/dia útil, sem repetir o mesmo alerta.

## Regras e invariantes
- **Movimento nunca se apaga nem se edita.** Corrige-se com estorno, que é outro movimento; o kardex é a prova.
- **Saldo nunca fica negativo**; o pedido sem saldo suficiente é recusado com o disponível.
- **Nada de inventar** lote, série, validade, UDI, classe de risco ou registro ANVISA. Faltou, pergunte.
- **Lote vencido não sai para paciente**, reserva nem venda. Sai por perda (vencimento).
- **Dado de implante nunca vai em lista, aviso ou mensagem, e nunca junto do nome do paciente.** Consulte por
  paciente, só quando precisar (rastreabilidade, etiqueta, recall), e responda só a quem pediu.
- **Consignado é do fornecedor**: só em local consignado, não se empresta, e transferência só entre locais
  consignados. O prazo de uso é por remessa.
- **Reserva não é movimento** — não aparece no kardex; o estorno de um consumo não reabre a reserva.
- **Toda escrita com prévia e confirmação** — movimento de estoque é registro de rastreabilidade.

## Limites / o que esta skill NÃO cobre
- **Cadastro do produto** (preço, modo de controle, marcações, classe de risco) → `precificador`.
- **Nota fiscal de entrada (NF-e), custo do material, kits por procedimento, inventário e faturamento de
  material no convênio** — chegam em ciclos próprios e serão acrescentados aqui quando existirem.
- **Temperatura e medicamentos controlados**: o produto só **marca** isso hoje; não há registro nem livro.
- **Pagar o fornecedor** → `financeiro`. **Comportamento do time de avisos** → `designer-agentes`.
- Não expõe como o estoque é calculado ou guardado por dentro — só como **consultá-lo, operá-lo e pensá-lo**.
