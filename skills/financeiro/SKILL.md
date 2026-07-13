---
name: financeiro
description: O ciclo do DINHEIRO depois da venda no Fluxo Ideal — receber (parcelas, contas a receber, aging/DSO/inadimplência), pagar (despesas, fornecedores, recorrências), o caixa (saldo, conferência, frente de caixa) e a saúde financeira (fluxo de caixa projetado, ponto de equilíbrio). Use para responder "quanto entrou / quanto a clínica deve / tem dinheiro em caixa / vai empatar?".
audience: [ia, humano]
depends_on: [pagamentos, contas-receber, contas-pagar, caixa, indicadores-financeiros]
version: 0.2.0
updated: 2026-07-12
---

# Financeiro

Entender e operar **o ciclo do dinheiro depois que a venda existe**: o que **entra** (o
paciente paga), o que **sai** (a clínica paga suas contas), onde tudo isso **decanta** (o
caixa) e se a clínica está **saudável** (fluxo de caixa e ponto de equilíbrio). É o **par
complementar** da precificação: lá se decide *quanto custa e como pode ser pago*; aqui se
cuida do *dinheiro efetivamente circulando*.

## Quando usar
- "Quanto entrou / quanto está a receber / quem está inadimplente?" (dinheiro dos pacientes).
- "Quanto a clínica deve / o que vence essa semana / quanto já paguei este mês?" (despesas).
- "Quanto tem em caixa hoje?", "o caixa fechou certo?", conferência de banco/gaveta.
- "Como fica meu caixa nos próximos 30 dias?", "quanto preciso faturar pra empatar?".
- Registrar/confirmar um pagamento, entender parcelas, estorno/devolução ao paciente.

## Quando NÃO usar
- Configurar preço, tabela, condição/forma de pagamento, montar orçamento ou fechar a venda
  → skill `precificador` (o preço **antes** do dinheiro circular).
- Agenda ou dados cadastrais do paciente → skill `secretária`.
- Faturamento de convênio / glosa / recurso (TISS) — existe no domínio, mas é um mundo
  próprio (lote, retorno da operadora, glosa, recurso). Trate **conceitualmente** aqui e
  deixe o detalhe para uma skill dedicada.

## Modelo mental

O dinheiro tem **dois lados** e um **reservatório** onde os dois se encontram:

```
        RECEBER (dos pacientes)                    PAGAR (contas da clínica)
   venda → pagamento → parcelas                 despesa (aluguel, folha, energia…)
        │                                            │  fornecedor · categoria · recorrência
        │  registrar (intenção)                      │
        ▼                                            ▼  baixar (pagar)
   confirmar (entrada REAL) ───────►  CAIXA  ◄─────── saída
                                    (contas: banco / caixa físico)
                                   saldo = inicial + Σ entradas − Σ saídas
                                          │
                        ┌─────────────────┼─────────────────┐
                        ▼                 ▼                 ▼
                  fluxo de caixa    ponto de          contas a receber
                   projetado        equilíbrio        (aging · DSO · inadimplência)
```

Três ideias sustentam tudo:

- **REGISTRAR ≠ CONFIRMAR.** Marcar uma parcela como *paga* é registrar uma **intenção** (o
  paciente disse que pagou, passou o cartão). A entrada só é **caixa de verdade** quando é
  **confirmada** — o dinheiro compensou/caiu na conta. No caixa isso aparece como
  **conferido** (real, compensado) vs **não conferido** (provisório, ainda não compensado).
  Nunca some "não conferido" como se fosse dinheiro na mão.
- **O caixa é derivado, não digitado.** O saldo de cada conta é uma **conta corrente**:
  saldo inicial + entradas − saídas. Ninguém "seta" o saldo; ele resulta dos movimentos. As
  entradas das vendas chegam **de forma assíncrona** (pode haver pequeno atraso entre a venda
  e o reflexo no saldo).
- **Previsto é sólido de um lado, dependente do outro.** As **saídas** previstas (despesas e
  recorrências) são fonte local e firme. Os **recebíveis** previstos (o que os pacientes vão
  pagar) dependem da carteira de vendas — quando essa fonte está indisponível, os indicadores
  **degradam com aviso** (mostram só as saídas / não calculam), e **nunca se inventa número**.

## Glossário

**Receber (dinheiro do paciente)**
- **Pagamento**: o registro de uma cobrança da venda/atendimento (forma: dinheiro, pix,
  débito, crédito à vista/parcelado, boleto, convênio). Pode ser à vista ou parcelado.
- **Parcela**: cada fração de um pagamento parcelado, com **vencimento** próprio. Estados:
  pendente, paga, atrasada, cancelada.
- **Registrar** um pagamento/parcela: declarar a **intenção** (status vira *paga*).
- **Confirmar** (compensar): marcar a **entrada efetiva** — o dinheiro caiu. É o que vira
  caixa **conferido**; base da conciliação.
- **Contas a receber (carteira)**: tudo que os pacientes ainda devem (parcelas em aberto).
- **Aging**: a carteira **por faixa de atraso** (a vencer, 0–30, 31–60, 61–90, 90+ dias) —
  faixas configuráveis.
- **DSO** (prazo médio de recebimento): quantos dias, em média, a clínica leva para receber.
- **Inadimplência**: proporção da carteira em atraso vs o total.
- **Estorno / devolução**: devolver valor ao paciente. Pode **reter** parte (cobre custo já
  incorrido / multa). A **natureza** muda conforme o serviço já foi executado ou não —
  devolver adiantamento de algo não-feito é neutro no resultado; devolver algo já realizado
  bate no resultado.

**Pagar (contas da clínica)**
- **Despesa / conta a pagar**: obrigação da clínica **não** atrelada a uma venda (aluguel,
  folha, energia, insumo). Tem vencimento e status (pendente, pago, atrasado, cancelado).
- **Fornecedor**: a quem se paga.
- **Categoria (plano de contas)**: como a despesa é classificada gerencialmente; distingue,
  entre outras coisas, **custo fixo** (entra no ponto de equilíbrio).
- **Centro de custo**: a qual área/unidade a despesa pertence.
- **Despesa recorrente**: um template que gera as despesas repetidas (mensalidade) automaticamente.
- **Baixar / pagar** uma despesa: registrar que foi paga (podendo gerar a saída no caixa).

**Caixa**
- **Conta financeira**: um "lugar de dinheiro" — conta bancária ou caixa físico da recepção.
- **Movimento de caixa**: cada entrada ou saída numa conta (o livro-razão). Guarda **duas
  datas**: a **competência** (quando o fato ocorreu) e a **liquidação** (quando o dinheiro
  entrou/saiu de fato).
- **Saldo consolidado**: o saldo por conta + total geral, derivado dos movimentos.
- **Conferido × não conferido**: dinheiro real/compensado vs provisório (ver "confirmar").
- **Frente de caixa (sessão)**: o turno do caixa físico — abre com um fundo de troco, recebe
  **sangrias** (retiradas) e **suprimentos** (reforços), e fecha conferindo o contado × o
  calculado (a **divergência** = sobra/falta).

**Saúde financeira**
- **Fluxo de caixa projetado**: como o saldo evolui nos próximos dias/semanas, somando
  entradas e saídas previstas ao saldo atual.
- **Ponto de equilíbrio (break-even)**: quanto a clínica precisa **faturar** para não ter
  prejuízo — custos fixos do período ÷ margem de contribuição (a margem vem do lado das vendas).

**Convênio (TISS) — só o conceito**
- **Faturamento de convênio / glosa / recurso**: cobrar da operadora, tratar o que ela
  **glosa** (nega) e **recorrer**. É um ciclo próprio, fora do dia a dia de caixa. Mencione
  quando aparecer; não detalhe aqui.

**Nota fiscal (NFS-e)**
- **NFS-e**: a nota fiscal de serviço emitida ao fisco. Vive numa **fila** (pendente → transmitindo →
  autorizada / rejeitada); a transmissão é **assíncrona**. **Emitir** e **reenviar** são atos fiscais.

## Ferramentas (tarefa → ferramenta)
> A execução depende de **autorização** — o MCP aplica permissão; a skill só ensina a
> intenção e o *quando*. As leituras respeitam a visão de quem chama.

**Contas a pagar (o que a clínica deve)**
- Listar despesas / o que vence / atrasadas / de um fornecedor → ferramenta que **lista
  despesas** (contas a pagar), com filtros de status, fornecedor, categoria, período de
  vencimento.
- Totais agregados ("quanto devo", "quanto vence em N dias", "quanto paguei este mês") →
  ferramenta de **KPIs de contas a pagar**.
- **Contas a pagar a terceiros** de uma venda (repasse a anestesista/hospital/laboratório) →
  ferramenta de **pagamentos a terceiros** (leitura + KPIs).

**Caixa**
- "Quanto tem em caixa?" por conta + total, com o recorte **conferido × provisório** →
  ferramenta de **saldo de caixa**.
- As **sessões de frente de caixa** (turnos: abertura, sangrias, suprimentos, fechamento/divergência)
  → ferramenta de **sessões de caixa** (leitura).

**Saúde financeira**
- "Como fica meu caixa nos próximos dias?" (baldes por dia/semana com saldo projetado) →
  ferramenta de **projeção de fluxo de caixa**. As **entradas previstas caem no dia/semana certo**
  (via os recebíveis por vencimento). Leia os avisos de degradação: se a fonte de recebíveis cai, a
  projeção mostra **só as saídas** — não é caixa zerado de entradas.
- "Quanto preciso faturar pra empatar?" → ferramenta de **ponto de equilíbrio**. Distinga:
  *margem indisponível* (fonte de vendas fora — não calcule, não invente) de *break-even
  indefinido de verdade* (margem ≤ 0).

**Contas a receber (dinheiro dos pacientes)**
- A **carteira de recebíveis** — **aging** (por faixa), **DSO**, **inadimplência**, visão consolidada
  → ferramenta de **contas a receber**. Leitura direta de "quanto tenho a receber / prazo médio / quem
  está em atraso" (o painel de **indicadores** segue trazendo a versão agregada de topo).
- **Recebíveis por vencimento** (o que entra em cada dia/semana) → ferramenta de **recebíveis por
  vencimento** — é o que alimenta a projeção de fluxo de caixa com as entradas no dia certo.
- **Pagamentos e parcelas** (pendências, parcelas vencidas, situação) → ferramenta de **pagamentos**; o
  **status de conciliação** (lançamentos × extrato) → ferramenta de **conciliação**. Ambas leitura.

**Nota fiscal (NFS-e)**
- **Consultar** a fila de notas fiscais e seus estados → ferramenta de **notas fiscais**.
- **Reenviar** uma NFS-e que falhou/foi rejeitada (re-transmite uma nota já criada — baixo risco) →
  ferramenta de **reenvio de nota fiscal**.
- **Emitir** uma NFS-e → ferramenta de **emissão de nota fiscal**, **gated por confirmação** (é ato
  fiscal); dinheiro em modo revisão cai na **fila de revisão** (gate humano). *Cancelar/revisar/dispensar
  ficam com o humano.*

**Assinatura (ponte com as vendas)**
- Documentos que **aguardam assinatura** do paciente (orçamento/TCLE) e **enviar/revogar** o link →
  ferramentas de **assinatura**. Enviar link é **outward-facing** (o paciente recebe e-mail real) →
  confirme antes.

**Ordem mental para "como está o dinheiro da clínica":**
saldo de caixa (conferido) → contas a receber (o que vai entrar, com aging) → contas a pagar
(o que vai sair) → projeção de fluxo de caixa (os dois no tempo) → ponto de equilíbrio (estou
faturando o suficiente?).

## Fluxos comuns

### "A clínica está com o caixa saudável?"
1. Saldo de caixa **conferido** hoje (dinheiro real, não o provisório).
2. Contas a receber com **aging** (quanto está a vencer × quanto já venceu — inadimplência).
3. Contas a pagar próximas (KPIs + o que vence na semana).
4. Projeção de fluxo de caixa no horizonte desejado — cruzando entradas e saídas previstas.

### "Registrei um pagamento mas o caixa não bateu"
1. Lembre a distinção **registrar × confirmar**: registrar marca a parcela como *paga*
   (intenção); o caixa só reflete **conferido** quando a entrada é **confirmada/compensada**.
2. Um pagamento registrado e ainda não compensado aparece como **não conferido** (provisório).
3. As entradas de venda chegam ao caixa de forma **assíncrona** — pode haver atraso curto.

### "Quanto preciso faturar pra empatar este mês?"
1. Ponto de equilíbrio = custos **fixos** do período (despesas categorizadas como custo fixo,
   por competência) ÷ margem de contribuição.
2. Se a margem estiver indisponível (fonte de vendas fora), **não estime** — reporte a
   indisponibilidade. Margem ≤ 0 é break-even **indefinido** (diferente de indisponível).

### "Vou devolver dinheiro a um paciente"
1. É um **estorno**. Pode devolver tudo ou **reter** parte (custo já incorrido / multa).
2. A **natureza** depende de o serviço ter sido executado (bate no resultado) ou não
   (devolução de adiantamento, neutra). Registre motivo e forma de devolução.

## Regras e invariantes
- **Registrar não é receber.** Só a **confirmação/compensação** vira caixa de verdade
  (conferido). Provisório (não conferido) não é dinheiro na mão.
- **Saldo de caixa é derivado** (inicial + entradas − saídas) — nunca digitado; e é
  alimentado **assincronamente** pelas vendas (pode atrasar um pouco).
- **Só uma frente de caixa aberta por conta** ao mesmo tempo; sangria/suprimento exigem sessão
  aberta; fechar exige conferir contado × calculado.
- **Competência ≠ liquidação.** O fato econômico (a venda/despesa) e a entrada/saída de
  dinheiro têm datas próprias; o custo fixo do break-even conta pela **competência**.
- **Indicador degradado nunca é zero.** Quando a fonte de recebíveis/margem cai, os
  indicadores avisam e mostram cenário conservador — **não se inventa número**.
- **Contas a pagar são da CLÍNICA**, não do paciente (despesas gerais); contas a **receber**
  são dos pacientes (parcelas em aberto). Não confunda os dois lados.
- **Ações que tocam o paciente são outward-facing** (enviar link de assinatura, e-mail) →
  confirme com o usuário antes.
- **A IA lê o dinheiro; não o move.** Registrar/confirmar pagamento, estorno, pagar despesa e mexer no
  caixa (sangria/fechamento) são **humano** — fronteira de segurança. A única escrita fiscal da IA é a
  **NFS-e**, e mesmo essa é **gated** (confirmação; emitir dinheiro-em-revisão cai em fila humana).

## Limites / o que esta skill NÃO cobre
- **Antes** do dinheiro circular (preço, tabela, condição/forma de pagamento, orçamento,
  fechar a venda) → skill `precificador`.
- **Faturamento de convênio / glosa / recurso (TISS)** — citado só conceitualmente; merece
  skill própria (lote, retorno da operadora, glosa, recurso, conciliação).
- **Conciliação com adquirente/gateway de cartão** (bater o extrato do meio de pagamento
  contra as parcelas confirmadas) — mecânica própria; candidata a skill própria.
- Agenda / cadastro do paciente → skill `secretária`.
- Não expõe como os valores são calculados/armazenados por dentro — só como **lê-los, operá-los
  e pensá-los**.
