---
name: precificador
description: O sistema de precificação do Fluxo Ideal — como se configura preço (catálogo, tabelas, condições e formas de pagamento, favoritos) e como isso converge em orçamento e venda. Use para entender "quanto custa", como montar um orçamento e por que os valores são o que são.
audience: [ia, humano]
depends_on: [precos, catalogo, convenios, condicoes-pagamento, orcamentos]
version: 0.3.0
updated: 2026-07-10
---

# Precificador

Entender e operar **todo o caminho do preço** numa clínica — da configuração (o que custa e como pode
ser pago) até ele virar **orçamento** e **venda**. Precificar aqui **não é** só pôr um valor num item;
é montar a cadeia que faz o valor certo aparecer no documento certo.

## Quando usar
- "Quanto custa?" de procedimento, produto ou pacote — e por quê.
- Configurar/entender tabelas de preço, descontos, condições e formas de pagamento.
- Montar ou explicar um **orçamento** (a junção de tudo isso num documento) e sua virada em **venda**.

## Quando NÃO usar
- O que acontece com o dinheiro **depois** — registrar/confirmar pagamento, parcelas em aberto,
  contas a receber, caixa, faturamento/glosa (TISS) → skill `financeiro`.
- Agenda ou dados do paciente → skill `secretária`.

## Modelo mental

Preço no Fluxo Ideal é uma **cadeia de configuração que converge num documento**, não um número solto:

```
catálogo ─┬─ tabela de preço (valor · desconto · cortesia · comissão, por item, por tabela)
          ├─ condição de pagamento (parcelas/juros)  ← vinculada à tabela
          └─ forma de pagamento (pix, cartão, convênio…)
                        │
        favoritos ──────┤  (atalho: itens que o profissional usa direto)
                        ▼
                  montar os itens
                   ┌────┴─────────────────────┐
                   ▼                           ▼
              ORÇAMENTO                     VENDA direta
    (junta item+tabela+cobertura+      (montada na hora, sem
     condição+validade+aceite)          orçamento prévio)
                   │  (aprovado → converte)
                   └──────────► VENDA
```

Três ideias que sustentam tudo:
- **O valor sempre depende da tabela aplicável** (particular / convênio / promoção) e da **cobertura**
  (particular, coberto, coparticipação). Não existe "preço único".
- **A venda NÃO depende de orçamento.** O orçamento é um caminho **opcional** (proposta antes de fechar);
  a venda pode ser criada **direto**, montando os itens na hora. Quando existe orçamento aprovado, ele
  **converte** em venda; quando não existe, a venda nasce sozinha.
- **Orçamento e venda são snapshot**: o preço é fotografado no momento. Mudar o catálogo depois **não**
  altera um documento já emitido.

## Glossário
**Configuração**
- **Catálogo**: o que existe — **procedimentos**, **produtos** (com estoque), **pacotes** (combos, às vezes já com retornos).
- **Tabela de preço**: quanto vale, por contexto (particular / um convênio / promoção). O **mesmo item tem preços diferentes em tabelas diferentes**; cada preço pode ter valor fixo, desconto, cortesia e comissão próprios naquela tabela, e a tabela define o **limite de desconto** permitido.
- **Condição de pagamento**: como se parcela (nº de parcelas, juros simples/composto ou descritivo). É **vinculada às tabelas** — uma tabela oferece um conjunto de condições.
- **Forma de pagamento**: por onde se paga (pix, dinheiro, cartão, boleto, convênio), com sua regra de parcelamento.
- **Favoritos do profissional**: itens que o profissional usa com frequência (um pode ser o padrão) — atalho para **montar** orçamento/venda rápido, sem varrer o catálogo.

**Cobertura**
- **Cobertura de convênio**: convênio paga; o paciente pode ficar em **R$ 0**. Não é desconto nem gratuidade — há receita do convênio por trás.
- **Coparticipação**: convênio paga uma parte, paciente outra. O item vale o **cheio**; muda o **rateio entre pagadores**, não o preço.
- **Autorização de convênio**: alguns procedimentos exigem aval prévio da operadora. É **pré-requisito operacional**, não preço.

**Documentos e ajustes**
- **Orçamento**: o documento que **junta** itens (snapshot), tabela, cobertura, condição de pagamento, validade e aceite do cliente. É a peça central da precificação.
- **Venda**: orçamento aprovado/confirmado, pronto para o ciclo de pagamento.
- **Desconto / cortesia**: redução dentro do limite da tabela / item incluído sem custo (isenção comercial).
- **No-show**: falta pode gerar **multa configurável** (confirmável, perdoável ou ajustável por quem tem alçada).
- **Retorno**: direito de retorno já incluído (ex.: num pacote) — **não se recobra**.

## Do catálogo à venda (o caminho)
1. **Configurar catálogo** — cadastrar procedimentos/produtos/pacotes.
2. **Precificar por tabela** — definir o valor de cada item em cada tabela (particular, convênio, promoção), com desconto/cortesia/comissão e o limite de desconto da tabela.
3. **Ligar pagamento à tabela** — associar as condições de pagamento e habilitar as formas.
4. **Montar** — escolher os itens (usando **favoritos** para agilizar).
5. **Fechar** — dois caminhos, e o orçamento é **opcional**:
   - **Com orçamento** (proposta antes de fechar): gerar o **orçamento** — fotografa item + tabela + cobertura + condição + validade; o cliente registra **aceite**; aprovado, **converte em venda**.
   - **Venda direta** (sem orçamento): montar e registrar a **venda** na hora.

## Ferramentas (tarefa → ferramenta)
> A execução depende de **autorização** — o MCP aplica permissão; a skill só ensina a intenção e o _quando_.

- Ver/gerir procedimentos, produtos e pacotes → ferramentas de catálogo (pacote também **simula** preço).
- Ver quais tabelas de preço existem e gerí-las → ferramentas de tabelas de preço.
- Ver/definir o preço de um item numa tabela → ferramentas de preço de item.
- Consultar as condições e formas de pagamento de uma tabela → ferramentas de pagamento (config).
- Saber quais convênios a clínica atende → ferramenta de convênios.
- Consultar/ montar orçamentos (e o preço fotografado) → ferramentas de orçamento.

**Ordem mental para "quanto custa":** tabela aplicável → preço do item nela → cobertura (particular / coberto / coparticipação) → desconto → condição de pagamento → total no orçamento.

## Regras e invariantes
- **Não existe preço único** — resolva sempre pela **tabela** aplicável primeiro.
- **A venda não exige orçamento** — pode ser criada direto; o orçamento é uma etapa opcional que, quando existe e é aprovada, converte em venda.
- **Orçamento/venda são snapshot** — catálogo alterado depois não muda documento já emitido.
- **Condição de pagamento pertence à tabela** — as opções de parcelamento saem da tabela aplicada, não são livres.
- **Coparticipação preserva o valor cheio** — muda o rateio, não o preço do item.
- **Cobertura ≠ desconto** — R$ 0 ao paciente ainda gera receita (do convênio).
- **Autorização é pré-condição, não preço.**

## Limites
- Não cobre o **ciclo do dinheiro** (registrar/confirmar pagamento, parcelas, contas a receber, caixa) nem **faturamento/glosa TISS** → `financeiro`.
- Não cobre agenda/paciente → `secretária`.
- Não expõe como preços são calculados/armazenados por dentro — só como **configurá-los, usá-los e pensá-los**.
