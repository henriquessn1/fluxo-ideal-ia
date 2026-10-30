---
name: estoque
description: O estoque rastreável da clínica no Fluxo Ideal — saldo por unidade e local, lote/validade e nº de série, FEFO, consumo de material no paciente e vínculo de implante (etiqueta da RDC 556/2021, UDI da classe IV), material consignado com prazo, reserva para procedimento agendado, alertas de validade/mínimo, o custo do material (custo na entrada, custo médio, extrato valorizado), o inventário (contagem cega, fechamento por diferença e o relatório de inventário de 31/12 ao custo para o contador) e os kits de material por procedimento e por profissional (consumo sugerido, reservar o kit, custo do kit). Use para "quanto tem da lente X na unidade Y?", "o que vence este mês?", "lança o material da cirurgia", "reserva a prótese para amanhã", "quais implantes esse paciente recebeu?", "quanto vale o estoque?", "vamos fazer o inventário", "preciso do inventário de 31/12 para o contador", "monta o kit da cirurgia de catarata", "reserva o kit da cirurgia de amanhã", "quanto custa o material desse procedimento?".
audience: [ia, humano]
depends_on: [estoque-rastreavel, consumo-material, implantes, consignado, reservas-material, alertas-estoque, custo-material, inventario-estoque, kits-material]
version: 0.4.0
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
- "Quanto custa esse material?", "quanto vale o estoque?", o extrato **valorizado** de um produto.
- Fazer o **inventário** (contagem cega por local, recontagem, fechamento por diferença) e tirar o **relatório
  de inventário** numa data (o de 31/12 para o contador).
- Montar e manter o **kit** de material de um procedimento (o padrão e o de cada profissional), usar o kit para
  **sugerir** o material do paciente, **reservar o kit** de um agendamento e saber o **custo do kit**.

## Quando NÃO usar
- Cadastrar o produto, mudar o preço, o modo de controle ou as marcações (implantável, consignável, classe de
  risco…) → skill `precificador` (é o **catálogo**). O estoque só **lê** o cadastro.
- Ler prontuário, evolução ou conduta → nunca pela IA (ver `medico`). O vínculo de implante é rastreabilidade do
  material, não conteúdo clínico.
- Pagar o fornecedor, conta a pagar → `financeiro`. Faturar material no convênio (TISS) → `faturamento-convenio`.
- A **margem** do procedimento com o material e o ponto de equilíbrio → `financeiro` (o estoque só dá o custo).
  A **simulação de margem** de um preço (que usa o custo do kit como custo previsto) → `precificador`.
- Mudar o comportamento do time de avisos do estoque → `designer-agentes`.
- **Escriturar** o Livro Registro de Inventário (termos, visto, escrituração fiscal digital) → é do **contador**;
  o sistema entrega o relatório.

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

Seis ideias sustentam tudo:
- **O saldo é derivado dos movimentos.** Ninguém digita o saldo: ele resulta do **kardex** (o extrato de
  movimentos), e movimento **nunca se apaga** — corrige-se com **estorno** (o movimento inverso).
- **O produto diz como ele é controlado.** Por **quantidade**, por **lote** (com validade) ou por **nº de
  série** (uma unidade = uma série). Isso decide o que a entrada e a saída exigem.
- **Disponível ≠ físico.** O físico é o que está no local; a **reserva** para um agendamento não é movimento,
  só separa: **disponível = físico − reservado**. O consumo e as outras reservas só usam o disponível.
- **O total do produto que aparece no catálogo é projeção do estoque.** O "estoque" e o "estoque baixo" que o
  catálogo mostra vêm daqui (com um pequeno atraso); o detalhe por local, lote e mínimo está aqui. O **custo do
  produto** no catálogo também vem daqui (é o custo médio, só leitura).
- **O custo entra com o material e sai pela média.** Cada entrada própria traz o seu **custo unitário**; o
  estoque mantém um **custo médio** por produto, e tudo o que sai (consumo, perda) sai por esse médio.
- **O kit é uma receita, não um movimento.** Ele diz **o que** um procedimento costuma usar (produto e
  quantidade); **qual lote ou série** sai só se decide no consumo ou na reserva. O kit **sugere** — quem baixa
  é sempre uma pessoa confirmando.

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

**Custo do material**
- **Custo unitário da entrada**: o custo de aquisição de cada unidade — preço de compra **menos** descontos,
  **mais** frete e seguro até a clínica e os tributos da compra que a clínica **não recupera** (juros da compra
  a prazo ficam fora). É **obrigatório** na entrada própria; pode ser 0. O valor vem da nota ou de quem
  comprou — **nunca se estima**.
- **Custo médio (média móvel)**: um só por **produto na clínica** (todas as unidades e locais, saldo próprio,
  inclusive o emprestado). É **recalculado a cada entrada**, ponderado pelas quantidades; **saídas,
  transferências, empréstimos e ajustes saem ao médio vigente e não o mudam**. A perda sai ao médio e é
  despesa do período.
- **Estorno e custo**: estornar uma **saída** devolve o custo que ela levou; estornar uma **entrada** tira o
  custo dela do médio — e é **recusado** se aquele material já saiu (o saldo próprio ou o valor ficariam
  negativos). Um custo digitado errado se corrige assim: estorno da entrada e entrada nova.
- **Consignado não tem custo médio**: é bem do fornecedor. O **consumo de consignado** nasce **aguardando
  faturamento** (sem custo); quando o fornecedor fatura, vira **faturado à clínica** (o custo da nota vai
  direto naquele consumo, sem passar pela média) ou **faturado à fonte pagadora** (custo zero para a clínica).
- **Extrato valorizado**: cada movimento mostra o custo unitário, o valor e o custo médio depois dele. O
  **saldo em valor** é do **produto** (todas as unidades); filtrando por local, é a quantidade do local × o
  médio.
- **Pendência de custo**: material que entrou sem custo (estoque anterior ao custo, produto sem custo no
  catálogo) ficou com custo 0 e aparece na lista de **pendências de custo** (na tela e pelo assistente), para a
  gestão corrigir.
  Produto que nunca teve custo **não tem médio**: as saídas dele ficam sem custo (não se inventa).
- **Ver custo é um acesso à parte** (gestão e financeiro). Sem ele, saldo, extrato e resumo saem **sem os
  valores**. Quem só movimenta **digita** o custo na entrada, mas não o vê nas listas. O custo do produto no
  catálogo segue a mesma regra.
- **Consumo ligado à venda**: o material do ato fica ligado ao **item** da venda e o dos "Materiais do
  atendimento" à **venda** — é assim que o custo chega à margem.

**Inventário**
- **Inventário**: a contagem física de um ou mais **locais** (opcionalmente só alguns produtos), aberta pela
  gestão. Só pode haver **um inventário aberto por local**. Termina **fechado** (com os ajustes) ou **cancelado**
  (sem nenhum movimento). **Fechado não reabre** — uma nova contagem é um inventário novo.
- **Contagem cega**: quem conta vê **o que contar** (produto, unidade, lotes esperados, a remessa no local
  consignado) e o que já lançou — **nunca a quantidade do sistema**. É isso que dá valor à contagem.
- **Folha de contagem**: a lista do que contar num inventário, com o que já foi contado.
- **Lançamento de contagem**: por produto (e lote, no modo lote; e remessa, no local consignado) a **quantidade
  contada** — zero vale — ou, no modo série, **as séries encontradas**. Cada lançamento guarda o momento e o
  saldo do sistema **daquele instante**: a movimentação **não para** durante o inventário.
- **Recontagem**: lançar de novo a mesma linha substitui a contagem anterior (e o momento dela).
- **Foto das séries**: no primeiro lançamento de série de um produto num local, o sistema registra as séries
  que deveriam estar ali **naquele instante**. As encontradas marcam a foto; lançar **nenhuma** encontrada
  também vale (só grava a foto).
- **Revisão**: para quem fecha — contado × esperado, a **diferença** de cada linha (sobra ou falta) e, com o
  acesso de ver custo, o **valor** da diferença.
- **Fechamento por diferença**: cada diferença vira um **ajuste** sobre o saldo **de agora** (não sobre o da
  contagem), ao custo médio, com o inventário como motivo; no local consignado o ajuste é da remessa e **sem
  custo**. Produto não contado não é ajustado.
- **Linha a recontar**: se, desde a contagem, saiu material e o ajuste deixaria o saldo negativo, a linha volta
  para **recontagem** e **nada** é ajustado até recontar.
- **Série não encontrada**: série da foto que continua registrada no local vira **perda**. Se estiver
  **reservada** para um agendamento, o fechamento é bloqueado até liberar a reserva. Série que chegou ou saiu
  do local depois da contagem não é perda.
- **Revisão manual**: série encontrada que **não estava na foto** (de outro local ou sem registro) não entra
  sozinha — a gestão confere a origem.
- **Relatório de inventário**: o estoque **numa data** (padrão: **31/12 do ano anterior**), reconstruído pelo
  kardex, ao **custo médio daquela data**, por unidade ou consolidado, em **três grupos separados**: **próprio**
  (nos locais), **próprio em poder de terceiros** (os empréstimos em aberto, a quem) e **de terceiros em poder
  da clínica** (o consignado, por fornecedor e remessa, **sem valor**). Total por grupo e geral (o geral soma só
  os dois grupos próprios); lote e validade nas observações. Não aceita data **antes do início do kardex** (a
  migração do saldo) nem no futuro.
- **Quem é obrigado ao Livro Registro de Inventário**: empresa no **lucro presumido** (Lei 8.981/1995, art. 45)
  e no **lucro real** (RIR/2018, art. 276 — inclui os bens de almoxarifado); no **Simples Nacional**, só quem é
  **contribuinte do ICMS** (Resolução CGSN 140/2018, art. 63). A avaliação é ao **custo de aquisição** (custo
  médio), sem ajuste a valor de mercado. A escrituração deve ser feita em até **60 dias** do balanço (ou do
  último dia do ano, para quem não tem escrita contábil) — Convênio SINIEF s/nº de 1970, art. 76, o Modelo 7. A
  escrituração é do **contador**.

**Kits de material**
- **Kit do procedimento (padrão)**: a lista de materiais que um procedimento costuma usar — cada item é um
  **produto** e uma **quantidade** (pode ser fracionada; inteira se o produto é controlado por série). **Lote e
  série nunca entram no kit.** Um procedimento tem no máximo um kit padrão.
- **Kit do profissional**: o kit daquele procedimento **para um profissional** (ex.: o cirurgião A usa outro
  viscoelástico). Quando existe e está ativo, **substitui o kit padrão inteiro** para ele — não soma item a item.
  Um por procedimento × profissional. Procedimento e profissional não mudam depois de criado: para outro par,
  crie outro kit.
- **Kit ativo / inativo**: kit inativo não vale. Desativar o kit do profissional faz voltar ao **padrão**.
- **Kit resolvido**: o kit que vale para um procedimento e um profissional (o dele, senão o padrão), já com a
  **sugestão FEFO** de cada item — o lote de validade mais próxima e o disponível, ou as séries disponíveis.
- **Item indisponível**: produto do kit que ficou **inativo** ou saiu do catálogo. Aparece marcado, sem sugestão,
  e não entra no consumo nem na reserva; o kit continua valendo para os outros itens. Quem tem a gestão troca o
  item.
- **Consumo sugerido**: ao lançar o material de um ato, o kit resolvido **pré-preenche** a lista; a pessoa
  confirma, edita ou remove. **Nunca baixa sozinho.** Se o agendamento tem **reserva ativa** de um produto, a
  **reserva vale antes do kit para aquele produto** (é a série ou a quantidade já separada); os demais itens do
  kit continuam.
- **Reservar o kit**: reserva para o agendamento os itens do kit do procedimento dele (o do profissional do
  agendamento, senão o padrão) e **reserva o que der**: o que já estava reservado conta como feito (pedir de
  novo não reserva em dobro); o resto sai do disponível do local; o que não deu volta como **falta**, com o
  motivo — sem disponível, disponível insuficiente (reservou o que havia), produto inativo ou fora do catálogo,
  ou **escolha a série** (item por série nunca é reservado sozinho: a equipe escolhe a unidade). Diferente da
  reserva comum, que é **tudo ou nada**.
- **Custo do kit**: a soma de quantidade × **custo médio** de cada item — exige o acesso de **ver custo**.
  Produto sem custo médio fica **fora da soma** (o custo fica **parcial**); nenhum item com médio = custo
  **desconhecido**, nunca zero.
- **Margem prevista**: a simulação de margem do procedimento usa o **custo do kit padrão** como custo do
  material quando o procedimento tem kit; sem kit, usa o custo estimado do cadastro do procedimento.

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
- Com o acesso de **ver custo**, o saldo, o resumo e o extrato trazem o **custo médio**, o custo de cada
  movimento e o **valor** — use-os para "quanto vale o estoque?" e "quanto custou esse material?". Sem ele os
  valores não vêm: diga que falta o acesso, **não** responda zero.

**Gerir (acesso de gestão do estoque)**
- Configurar o estoque (unidade principal, consignado ligado/prazo, antecedência dos alertas), criar/editar
  locais e **definir o mínimo** de um produto num local → ferramenta de **gestão da configuração**.
- **Movimentar** → ferramenta de **movimentação**: entrada, transferência entre locais, empréstimo (a quem) e a
  devolução dele, **ajuste** (informe a quantidade **contada**; o sistema lança a diferença), **perda** (perda,
  vencimento ou avaria) e **estorno** de um movimento. Entrada, transferência, empréstimo e entregas pedem o
  acesso de **movimentar**; ajuste, perda e estorno pedem o de **ajustar** (mais restrito). A **entrada própria
  exige o custo unitário** — pergunte se não veio; **0 só** para doação ou bonificação. As ações que saem ao
  custo médio (transferência, empréstimo, ajuste, perda, estorno) **não recebem custo**; a remessa consignada
  também não.
- **Pendências de custo** (entradas que ficaram com custo 0 por falta de custo) → ferramenta que **lista as
  pendências de custo** (pede o acesso de ver custo). **Corrigir o custo** de uma entrada pendente →
  ferramenta de **correção de custo**: pede o acesso de **ajustar** e o de **ver custo**, mostra a simulação
  primeiro e só grava confirmado; o custo médio se refaz sozinho. Só vale para entrada **pendente** — custo
  errado em outra entrada se corrige por estorno e entrada nova.
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

**Inventário (contar pede o acesso de movimentar; abrir, revisar, fechar e cancelar, o de ajustar)**
- Os inventários (abertos, fechados, cancelados), a **folha de contagem**, a **revisão** e o **relatório de
  inventário** numa data → ferramenta de **consulta do inventário**. A folha nunca traz o saldo do sistema; o
  relatório vem **resumido** (por grupo, totais, por local e as primeiras linhas) — o arquivo completo (CSV) e
  o PDF saem da tela de relatórios do estoque.
- **Abrir** o inventário (locais e, se quiser, só alguns produtos), **lançar a contagem**, **fechar** e
  **cancelar** → ferramenta de **operação do inventário**. A prévia do fechamento mostra a revisão resumida (o
  que vai virar ajuste, perda ou revisão manual) — mostre, confirme e só então feche. A resposta de uma contagem
  só diz **quantas linhas entraram**.
- O **regime tributário** da clínica (para dizer se ela é obrigada ao livro) está na configuração fiscal → skill
  `financeiro`, se quem pergunta tiver acesso; sem ele, dê a regra geral.

**Kits (consultar é leitura; manter é da gestão — acesso de ajustar; a sugestão é do consumo; reservar o kit é
do acesso de reserva)**
- Os kits como estão cadastrados (por procedimento, por profissional, só os padrões ou só os de profissional,
  inclusive os inativos), um kit, e o **kit que vale** para vários procedimentos e profissionais de uma vez (ex.:
  os procedimentos da semana — sem sugestão de lote) → ferramenta de **consulta de kits**.
- **Criar** o kit (padrão ou do profissional), **trocar a lista de itens** (a lista inteira), **ativar,
  desativar ou renomear** e **apagar** → ferramenta de **gestão de kits**. A prévia mostra o kit atual; confirme
  e só então grave.
- O **kit resolvido com a sugestão FEFO** para lançar o material de um ato (com o agendamento, ela marca o item
  que já tem reserva) → ferramenta de **consumo** (leitura). Depois, o lançamento é o de sempre.
- **Reservar o kit** de um agendamento (reserva o que der e lista as faltas) → ferramenta de **gestão de
  reservas**. A reserva comum (itens escolhidos, tudo ou nada) segue na mesma ferramenta.
- O custo do kit e de cada item só vêm com o acesso de **ver custo** — sem ele, diga que falta o acesso, não
  responda zero.

**Fora da IA:** marcar um alerta como "já avisado" é do time de avisos; anexar a **foto da etiqueta** do
implante é pela tela.

## Fluxos comuns

### "Quanto tem da lente +22 na unidade Centro?"
1. Ache o produto pelo nome (pergunte se vier mais de um).
2. Peça o saldo com o resumo: responda pelo **disponível** daquele local/unidade e diga o reservado à parte.
3. Se for por lote, diga as validades; se for por série, quantas séries estão livres.

### "Lança o material da cirurgia"
1. Confirme o atendimento, o paciente e, se houver, o ato e o agendamento.
2. Se o procedimento tem **kit**, comece pelo **kit resolvido** (do profissional do ato, senão o padrão) com a
   sugestão FEFO de cada item; sem kit, peça a sugestão FEFO produto a produto. Com o agendamento, o que estava
   **reservado** vale antes do item do kit do mesmo produto.
   Mostre a lista como **sugestão**: a pessoa confirma, muda quantidades, tira ou acrescenta itens.
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

### "Monta o kit da cirurgia de catarata"
1. Ache o procedimento (no catálogo) e, se o kit for de um profissional, o profissional.
2. Veja se já existe kit para o par: existindo, **troque os itens** (a lista inteira) em vez de criar outro.
3. Monte os itens: produto (pelo nome ou código — pergunte se vier mais de um) e quantidade. **Sem lote e sem
   série** — eles se escolhem no consumo. Produto inativo é recusado.
4. Kit do profissional: lembre que ele **substitui o padrão inteiro** — inclua tudo o que ele usa, não só a
   diferença.
5. Mostre a prévia, confirme e grave. Com o acesso de ver custo, diga o **custo do kit** (e se ficou parcial).

### "Reserva o kit da cirurgia de amanhã"
1. Ache o agendamento: o procedimento e o profissional vêm **dele** (com vários procedimentos, vale o
   principal). Agendamento sem procedimento, ou procedimento sem kit, é recusado.
2. Mostre a prévia e confirme; o local é o padrão da unidade do agendamento, salvo se a pessoa escolher outro.
3. Leia o resultado: o que foi **reservado** e as **faltas** com o motivo. Item por **série**: mostre as séries
   disponíveis e reserve a escolhida (reserva comum). Sem disponível: sugira **transferir** de outro local ou
   comprar.
4. Pedir de novo não reserva em dobro — só tenta o que faltou.

### "Quanto custa o material desse procedimento?"
1. Precisa do acesso de **ver custo**; sem ele, diga que o valor não está disponível para quem pergunta.
2. Consulte o kit que vale (do profissional, se a pergunta for sobre ele; senão o padrão) e responda o **custo
   do kit** = Σ quantidade × custo médio. Custo **parcial** ou **desconhecido**: diga quais itens estão sem
   custo médio — não complete com estimativa.
3. A margem do procedimento usa esse custo (o do kit padrão) quando há kit → `precificador` para simular o
   preço, `financeiro` para a margem realizada.

### "Chegou material consignado"
1. Confira que o consignado está ligado e que existe um **local consignado** na unidade.
2. Registre a **remessa**: fornecedor, local consignado, NF de remessa e itens no modo de controle do produto.
   O prazo de uso sai sozinho (data + prazo da clínica).
3. No uso, o consumo é o normal, escolhendo o **local consignado**.
4. Para o fornecedor faturar: o relatório de consumo; quando ele repõe, marque como **reposto** (com a NF).
   O que não foi usado volta por **devolução ao fornecedor**, antes do prazo.

### "Chegou material" (entrada com custo)
1. Ache o produto e o local; confira o modo de controle (lote e validade? séries?).
2. Pergunte o **custo unitário** de aquisição, se não veio: preço − descontos + frete/seguro + tributos que a
   clínica não recupera, dividido pela quantidade. Na dúvida sobre o que entra no custo, peça ao contador —
   não estime.
3. Mostre a prévia (quantidade, lote/séries, custo) e grave confirmado. O custo médio do produto se recalcula
   sozinho.
4. Custo errado já gravado: estorne a entrada (se o material ainda não saiu) e lance de novo.

### "Quanto vale o estoque?" / "Quanto custa esse material?"
1. Precisa do acesso de **ver custo**; sem ele, diga que os valores não estão disponíveis para quem pergunta.
2. Valor do produto = saldo próprio × custo médio (todas as unidades). Por local = quantidade do local × médio.
3. O **consignado não entra** no valor da clínica (é do fornecedor).
4. Produto com pendência de custo está com custo 0 até a gestão corrigir — avise que o valor está incompleto
   e, se quem pergunta tem o acesso, ofereça corrigir (simulação, confirmação, gravação).

### "Vamos fazer o inventário" (contagem cega)
1. Com o acesso de ajustar, **abra** o inventário nos locais escolhidos (e, se for parcial, os produtos). Já
   havendo um aberto no local, feche ou cancele aquele antes.
2. Para quem vai contar, mostre só a **folha de contagem**. **Não consulte nem mostre o saldo, o extrato ou a
   revisão** a quem conta — isso desfaz a contagem cega.
3. Lance o que está na prateleira, por local: a **quantidade** (zero, se não achou nada), o **lote** lido na
   embalagem (modo lote), a **remessa** (local consignado) ou, no modo série, **as séries encontradas** — lido
   no leitor ou digitado, **nunca inventado**. Não achou nenhuma série? Lance a lista **vazia**.
4. Errou ou ficou em dúvida? **Reconte**: lançar de novo a mesma linha substitui a anterior.
5. Quem fecha olha a **revisão**: sobras, faltas e, com o acesso de ver custo, o valor. Diferença grande? Peça
   recontagem antes de fechar.
6. **Feche** com prévia e confirmação. Se vier "reconte antes de fechar", alguém tirou material depois da
   contagem: reconte as linhas indicadas. Série reservada não encontrada: libere a reserva do agendamento (ou
   ache a série) antes. Séries em **revisão manual** não entram sozinhas — confira a origem.
7. Fechado não reabre. Desistiu antes de fechar? **Cancele** (nada é movimentado).

### "Preciso do inventário de 31/12 para o contador"
1. Peça o **relatório de inventário** da data (sem data = 31/12 do ano anterior), por **unidade** ou consolidado
   — empresa **sem escrita contábil** levanta o inventário **em cada estabelecimento** no último dia do ano; na
   dúvida, pergunte ao contador.
2. Os valores exigem o acesso de **ver custo**; sem ele, o relatório vem só com as quantidades — diga isso, não
   responda zero.
3. Leia os **avisos** antes de entregar: **pendência de custo** deixa o valor incompleto (corrija primeiro) e o
   **consignado** sai sem valor (é bem do fornecedor).
4. Explique os **três grupos** e que o total geral é só do que é **próprio**.
5. Diga **quem é obrigado** (lucro presumido e real; Simples só se contribuinte do ICMS) e o prazo de **60 dias**
   do balanço; se tiver acesso à configuração fiscal, confira o regime da clínica.
6. O arquivo (CSV) e o PDF saem da tela de relatórios do estoque; **escriturar o livro é do contador**.

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
- **Custo nunca se inventa nem se estima**: vem da nota ou de quem comprou. Sem o acesso de ver custo, os
  valores **faltam** — não são zero.
- **Um só custo médio por produto na clínica**; a saída mantém o médio; o consignado fica fora dele.
- **Contagem é cega**: a quem conta, só a folha — nunca o saldo nem a revisão.
- **Inventário fecha por diferença sobre o saldo de agora**, tudo ou nada; **fechado não reabre**. Produto não
  contado não é ajustado.
- **Série que sumiu vira perda; série achada sem registro vai para revisão manual** — nunca entra sozinha.
- **O kit nunca baixa sozinho**: ele só sugere; o consumo é sempre confirmado por uma pessoa.
- **Lote e série nunca entram no kit.** O kit diz o produto e a quantidade; o lote/série é escolhido no consumo
  ou na reserva.
- **O kit do profissional substitui o padrão inteiro**; inativo não vale (volta ao padrão).
- **A reserva do agendamento vale antes do kit** para o mesmo produto; os outros itens do kit continuam.
- **Reservar o kit reserva o que der e diz o que faltou**; a reserva comum é tudo ou nada.
- **Custo do kit sem custo médio é desconhecido, não zero.**

## Limites / o que esta skill NÃO cobre
- **Cadastro do produto** (preço, modo de controle, marcações, classe de risco) → `precificador`.
- **Nota fiscal de entrada (NF-e) e faturamento de material no convênio** — chegam em ciclos próprios e serão
  acrescentados aqui quando existirem.
- **Kits**: não há baixa automática do kit, kit para **item de pacote**, kit por convênio ou por lateralidade
  (olho), kit dentro de kit, nem bandeja de instrumental (CME).
- **Escrituração do Livro Registro de Inventário** (termos, visto do fisco, escrituração fiscal digital) → contador.
  Laudo de perda por vencimento e inventário rotativo automático (por curva ABC) não existem hoje.
- **Margem e ponto de equilíbrio** com o material → `financeiro`. Rateio de custo fixo não é custo do material.
- **Temperatura e medicamentos controlados**: o produto só **marca** isso hoje; não há registro nem livro.
- **Pagar o fornecedor** → `financeiro`. **Comportamento do time de avisos** → `designer-agentes`.
- Não expõe como o estoque é calculado ou guardado por dentro — só como **consultá-lo, operá-lo e pensá-lo**.
