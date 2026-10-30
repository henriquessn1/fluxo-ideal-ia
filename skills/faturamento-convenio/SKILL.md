---
name: faturamento-convenio
description: O faturamento de convênio (TISS) no Fluxo Ideal — faturar guias/lotes, o material usado no paciente cobrado sozinho no Anexo de Outras Despesas da guia SP/SADT (códigos TUSS ou da operadora, unidade, preço do convênio, OPME consignado faturado pelo fornecedor ou pela clínica, pendências do lote), importar o retorno da operadora, tratar glosas e recorrer. Use para entender o ciclo de cobrança de convênio, acompanhar lotes/glosas e responder "por que o material não entrou na guia?". É o "financeiro de convênio", distinto do financeiro-caixa.
audience: [ia, humano]
depends_on: [faturamento-convenio, tiss, glosa, consumo-material]
version: 0.3.0
updated: 2026-10-30
---

# Faturamento de convênio (TISS)

Conduzir e acompanhar o **faturamento de convênio** — transformar atendimentos em cobrança à
operadora pelo padrão TISS, importar o retorno e tratar o que foi **glosado** (negado). É o
"financeiro de convênio", um domínio especializado, distinto do financeiro-caixa.

## Quando usar
- Faturar guias/lotes de convênio, ver o status de um lote, acompanhar glosas pendentes / valor glosado.
- Entender o ciclo TISS (faturar → retorno → glosa → recurso).
- Entender e destravar o **material na guia**: o que entrou no Anexo de Outras Despesas, por que um material
  não entrou, o que é cada pendência de material do lote e onde se corrige.

## Quando NÃO usar
- Caixa/pagamento/recebimento **particular** → skill `financeiro`.
- Preço/tabela/cobertura de convênio no orçamento → `precificador` (inclusive o **preço do material** na
  tabela do convênio e o código da operadora dele).
- **Lançar** o material usado no paciente, estornar um consumo, lote/série, consignado → `estoque`. Esta
  skill só **cobra** o que o estoque registrou.
- Autorização de convênio no **agendamento** (inclusive a solicitação de OPME) → `secretaria`.

## Modelo mental
O ciclo é **multi-etapa**:

```
configurar convênio → FATURAR um LOTE (guias TISS: consulta / SP-SADT) → enviar à operadora
   → importar o DEMONSTRATIVO (o retorno) → o não pago vira GLOSA → tratar / RECORRER → conciliar
```

Há **duas naturezas de escrita**, e a fronteira entre elas é a lente-mestra:

- **CONFIGURAR** o convênio — o "contrato TISS" (registro ANS, versões de componente, prazos,
  homologação) e o **código TUSS** do procedimento — é **cadastro**: reversível, interno, não move
  dinheiro nem fala com a operadora → **IA com confirmação**. É onde a IA mais ajuda: *descobrir o que
  colocar* (ex.: as versões vigentes da ANS).
- **FATURAR / recorrer / transmitir** é **ato perante a operadora** (uma rejeição baixa a qualidade do
  prestador) → **humano**. Aqui a IA **lê**: status de lote, glosas, prazos, demonstrativo.

### O material na guia (Anexo de Outras Despesas)
O material usado no paciente **entra sozinho** na guia — ninguém digita. As guias são montadas **por
venda** (uma por senha de autorização) e, ao gerá-las, o sistema busca o material ligado àquela venda:

```
consumo do ato (ligado ao item da venda) ──► guia da senha daquele item, vinculado ao procedimento
"Materiais do atendimento" (só a venda)  ──► primeira guia SP/SADT da venda, sem vínculo a procedimento
produto vendido como item da venda       ──► anexo, a partir do próprio item (o consumo dele não cobra 2×)
                                │
                                ▼
          ANEXO DE OUTRAS DESPESAS da guia SP/SADT (código · quantidade · unidade · valor)
                                │
                     subtotal por tipo de despesa + total geral da guia → total do lote
```

- O anexo **não é uma guia separada**: faz parte da própria guia SP/SADT e não tem número próprio
  (Padrão TISS 4.03.00, ANS). **A guia de consulta não tem anexo** — material numa venda cuja guia sai
  como consulta vira pendência.
- Cada material vira um **item da guia**, como um procedimento: entra no valor da guia e do lote, no
  "Faturado" do convênio e na **glosa**/**recurso** item a item, do mesmo jeito que um procedimento.
- O anexo é um **retrato** tirado ao gerar as guias. Com o lote **aberto**, gerar de novo refaz o retrato;
  depois de **gerado/enviado**, ele não muda (ver "Estorno depois do envio").

## Glossário
- **TISS / TUSS**: o padrão da ANS de troca com a operadora / a tabela de códigos de procedimento.
- **Guia**: o documento de cobrança de um atendimento (consulta ou SP-SADT).
- **Lote**: o conjunto de guias enviado à operadora de uma vez.
- **Demonstrativo**: o retorno da operadora — o que pagou, o que glosou e por quê.
- **Glosa**: valor negado (total/parcial) pela operadora. Tem uma **máquina de estados**.
- **Recurso**: a contestação de uma glosa.
- **Autorização prévia**: aval da operadora antes de executar (pré-requisito, não cobrança).

**Material na guia** (Padrão TISS 4.03.00, ANS)
- **Anexo de Outras Despesas**: a parte da guia SP/SADT onde vão materiais, medicamentos, gases, taxas,
  diárias e OPME. Cada linha leva data, tipo de despesa, tabela + código, quantidade, unidade de medida,
  valor unitário, valor total e descrição.
- **Tipo de despesa**: classificação TISS da linha — **01** gases medicinais · **02** medicamentos ·
  **03** materiais · **08** OPME (o padrão TISS tem ainda 05 diárias e 07 taxas e aluguéis, que não vêm do
  estoque). Vem do **cadastro do produto**; sem escolha, implantável vale 08 e o resto 03.
- **Tabela + código**: com código **TUSS**, a linha sai na **tabela 19** (materiais e OPME) — **20** para
  medicamentos, **18** para taxas, diárias e gases. **Sem TUSS**, sai na **tabela 00** com o **código da
  operadora** (até 10 caracteres), cadastrado no **preço do produto na tabela do convênio**. Não se inventa
  código próprio para algo que já tem TUSS.
- **Unidade de medida**: obrigatória em toda linha — a unidade TISS (terminologia de unidades da TUSS)
  do cadastro do produto.
- **Item vinculado**: o procedimento da guia ao qual o material se refere (o material do ato). O dos
  "Materiais do atendimento" vai sem vínculo.
- **OPME**: órtese, prótese e material especial (ex.: lente intraocular, anel, prótese).
- **Registro ANVISA e referência do fabricante na guia**: exigidos **só para OPME sem TUSS** (o registro
  vai com até 15 caracteres).
- **AFE** (autorização de funcionamento da empresa de quem a clínica comprou o OPME): vai **só no OPME
  comprado pela clínica**. Vem da entrada do material no estoque (em lote/série, a da entrada daquele
  lote ou série; em controle por quantidade, a da entrada mais recente). No consignado que a clínica
  cobra, vem da remessa.
- **OPME consignado — quem fatura**: configuração **por convênio**. **"O fornecedor fatura direto"** à
  operadora (padrão) — o OPME **fica fora da guia** e aparece listado como "faturado pelo fornecedor";
  **"a clínica cobra"** — entra no anexo como os demais. A ANS não fixa regra: é contratualização entre
  operadora e prestadores (Parecer Técnico ANS nº 24/2021), e a nota do OPME vai para a fonte pagadora
  (Ajuste SINIEF 2/2024).

## Ferramentas (tarefa → ferramenta)
> A execução depende de **autorização** — o MCP aplica a permissão; a skill ensina a intenção e o *quando*.
> As leituras trazem uma **projeção enxuta**: dados do beneficiário (nome/carteirinha) **nunca trafegam**
> e os textos livres (motivo de glosa, justificativa) são **higienizados**.

**Ler o convênio (agora por ferramenta):**
- **Glosas** — os **prazos/SLA** de contestação vencendo, os **indicadores** (quanto glosado e por quê) e
  a **busca** de glosas por filtro.
- **Lotes** — buscar e ver o **status** de um lote, com o **anexo de outras despesas** de cada guia
  (itens, subtotais por tipo de despesa) e as **pendências** do lote (inclusive as de material).
- **Recursos** — acompanhar os **recursos** (as contestações de glosa).
- **Board de autorização prévia** — a fila de autorizações do convênio (leitura).
- **Demonstrativos** — a **listagem do retorno** da operadora (o que ela pagou / glosou).
- **Dinheiro do convênio (visão gerencial)** — os **recebíveis de convênio** e a **reconciliação de
  convênio** (apresentado × pago × glosado) → pela quebra (**drill-down**) do painel de gestão (skill
  `indicadores`), disponível também a este papel.

**Configurar o convênio (por ferramenta, com prévia + confirmação — é cadastro, não movimento):**
- **Contrato TISS** — criar/editar a configuração TISS do convênio: **registro ANS**, as **versões de
  componente** da ANS, **prazos**, o **status de homologação** e **quem fatura o OPME consignado** ("o
  fornecedor fatura direto" ou "a clínica cobra"). A IA ajuda a *descobrir o que colocar*.
  *Ligar a transmissão automática (webservice) ou marcar "produção" arma envio real → confirmação
  reforçada; o segredo do webservice (credencial/certificado) fica com o humano.*
- **Código TUSS do procedimento** — mapear o código que vai na guia, pela ferramenta de **catálogo de
  procedimentos** (compartilhada com o `precificador`); **procurar** o código válido pela ferramenta de
  **lookup TUSS**; e **importar** o catálogo TUSS da ANS (gated).
- **Dados TISS do material** — código TUSS, **tipo de despesa**, **unidade de medida**, registro ANVISA e
  referência do fabricante ficam no **cadastro do produto** (ferramentas de catálogo, `precificador`); o
  **valor do convênio** e o **código da operadora** ficam no **preço do produto na tabela do convênio**
  (ferramenta de preço de item, `precificador`). A AFE fica na entrada do material (`estoque`).

**Faturar / tratar (sob humano — ato perante a operadora):**
- Faturar um lote, gerar as guias/o XML (e **gerar de novo** um lote aberto), **importar/parsear** um
  demonstrativo, **tratar/recorrer** uma glosa, transmitir à operadora. É o "enviar" — fica **humano**.

## Fluxos comuns

### "Que material entrou nesta guia?"
1. Abra o lote e a guia: o anexo lista cada material (código, quantidade, unidade, valor) e os subtotais por
   tipo de despesa; o total da guia já soma o anexo.
2. OPME consignado de convênio em que **o fornecedor fatura direto** não aparece no anexo — aparece na
   lista "faturado pelo fornecedor". Isso é o esperado, não falha.
3. Faltou um material que foi usado? Veja se o consumo foi lançado e ligado à venda (skill `estoque`) e se
   há pendência de material no lote (abaixo).

### "O lote não gera o XML — pendência de material"
As pendências abaixo **bloqueiam** o XML; resolva no cadastro e peça a quem fatura para **gerar as guias de
novo** (lote aberto):

| Pendência | Onde se resolve |
|---|---|
| Material **sem preço** ou com preço **bloqueado** na tabela do convênio da venda | Preço do produto na tabela do convênio (`precificador`) |
| Material **sem unidade de medida** TISS | Cadastro do produto (`precificador`) |
| Material **sem TUSS e sem código da operadora** | Procure o TUSS (lookup TUSS) e grave no produto; não existindo, peça à operadora o código dela e grave no preço do produto na tabela do convênio |
| **OPME sem TUSS** sem registro ANVISA (ou com registro maior que 15 caracteres) ou sem referência do fabricante | Cadastro do produto — copie do registro/etiqueta, **nunca** invente |
| Material numa venda cuja guia sai como **consulta** | Material só sai em **SP/SADT**; quem fatura decide se o atendimento vai em SP/SADT ou se o material não é cobrado |

**Aviso (não bloqueia):** OPME **comprado pela clínica sem AFE** (ex.: saldo migrado de antes) — a guia sai,
mas a operadora pode exigir; complete a AFE na entrada do material (`estoque`) quando souber.

Configurar o cadastro (produto, preço, contrato TISS) é **IA com confirmação**; gerar de novo e enviar é
**humano**.

### "O material foi estornado depois de enviar o lote"
1. Com o lote **aberto**, basta **gerar de novo** — o anexo refaz o retrato com o que vale agora.
2. Com o lote **gerado/enviado**, o XML enviado **não muda**. A tela do lote mostra a **divergência**
   ("material estornado depois do envio"), consultando o estoque na hora.
3. O que fazer perante a operadora com essa diferença é decisão **humana** (quem fatura).

### "Por que esse material não foi faturado?"
- Material lançado **antes** de o consumo passar a ser ligado à venda **não entra sozinho** na guia — a
  tela do lote declara a data de corte. Cobrá-lo é decisão humana.
- Consumo sem ligação à venda, OPME consignado faturado pelo fornecedor, ou pendência em aberto: veja os
  fluxos acima.

## Regras e invariantes
- **Configurar ≠ faturar.** Cadastrar/editar o contrato TISS e o mapeamento TUSS é **config** (IA com
  confirmação); **faturar/recorrer/transmitir** é ato perante a operadora (**humano**).
- **Faturar/recorrer é ato perante a operadora** — humano no loop.
- **Glosa tem máquina de estados** — não se "pula" para um estado; segue o fluxo.
- **Autorização ≠ cobrança** — é pré-requisito operacional.
- **Contrato TISS ≠ tabela de preço.** A configuração TISS (registro ANS, versões, prazos) é deste perfil;
  os **preços** negociados do convênio são do `precificador`.
- **Material entra sozinho, a partir do estoque.** Ninguém digita material na guia; se ele não está lá, a
  causa está no consumo, no cadastro ou numa pendência.
- **Material só em SP/SADT** — a guia de consulta não tem anexo.
- **O preço do material é o valor do convênio** do produto na **tabela de preço da venda** — a mesma regra
  do procedimento. Sem preço (ou bloqueado) não fatura.
- **TUSS primeiro**: com TUSS, tabela 19/20/18; sem TUSS, tabela 00 + código **da operadora**. Nunca código
  próprio para algo que tem TUSS.
- **Cobra uma vez só**: o produto vendido como item da venda vai no anexo pelo item; o consumo dele não
  repete a cobrança.
- **OPME consignado fica fora da guia** quando o convênio diz que o fornecedor fatura direto (o padrão).
- **Registro ANVISA e referência só para OPME sem TUSS; AFE só para OPME comprado pela clínica.**
- **O XML enviado não se reescreve** — estorno posterior aparece como divergência no lote.
- **O "Esperado" do convênio inclui o material** das guias geradas, para bater com o "Faturado" (soma das
  guias); a margem realizada recebe a **receita** do material faturado junto com o custo. A **venda não
  ganha item** pelo material cobrado — ele fica na guia e no lote.

## Limites
- Não cobre caixa/pagamento particular (`financeiro`), preço/tabela do convênio (`precificador`) nem
  autorização no agendamento (`secretaria`).
- Não lança, não estorna e não move material — isso é do `estoque`.
- Fora daqui: anexo de outras despesas em guia de consulta, resumo de internação ou honorários; tabelas
  de mercado (Simpro/Brasíndice); o **anexo de solicitação de OPME** (é da autorização, não da cobrança).
- O faturamento no backend é **ativado por convênio** (liga quando o convênio precisa); as ferramentas
  existem, mas dependem dessa ativação **e** da autorização do papel.
