---
name: precificador
description: O sistema de precificação do Fluxo Ideal — como se configura preço (catálogo, tabelas, condições e formas de pagamento, favoritos) e como isso converge em orçamento e venda. Use para entender "quanto custa", como montar um orçamento e por que os valores são o que são.
audience: [ia, humano]
depends_on: [precos, catalogo, convenios, condicoes-pagamento, orcamentos, termos-orcamento]
version: 0.4.4
updated: 2026-08-04
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
  contas a receber, caixa → skill `financeiro`; faturamento/glosa (TISS) → skill `faturamento-convenio`.
- Agenda ou dados do paciente → skill `secretaria`.

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
- **Autorização de convênio**: alguns procedimentos exigem aval prévio da operadora. É **pré-requisito operacional**, não preço. Configura-se **por tabela de convênio**, em modalidades: *não requer*, *automática* (online/imediata), *prévia* (auditoria — solicitar e aguardar) ou *OPME* (com anexo de materiais).

**Documentos e ajustes**
- **Orçamento**: o documento que **junta** itens (snapshot), tabela, cobertura, condição de pagamento, validade, **termos** e aceite do cliente. É a peça central da precificação.
- **Termo do orçamento**: o **texto legal** que acompanha o orçamento — declaração de aceite, intercorrências, itens não inclusos, **TCLE** (consentimento) ou outros. O orçamento **seleciona** um template de termo por tipo (há um **padrão** por tipo). Você **escolhe** qual termo entra; **redigir/versionar o texto** dos termos é da skill `designer-documentos` (tela **Templates de Termos**, nas configurações).
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
> A execução depende de **autorização** — o MCP aplica permissão; a skill ensina a intenção e o _quando_.

**Hoje, por ferramenta:**
- Ver/gerir procedimentos, produtos e pacotes → ferramentas de catálogo.
- Ver e gerir as tabelas de preço → ferramentas de tabelas de preço.
- Ver/definir o preço de um item numa tabela → ferramenta de preço de item. Além do valor/desconto,
  ela configura a **cobertura de convênio** do item: *coberto totalmente* (paciente paga R$ 0) ou
  *coberto parcialmente/coparticipação* (informe a **parte do paciente** = copay e a **parte do
  convênio**) — e isso vale para **procedimento e produto** (ex.: lente, medicação). Só para
  **procedimento**, define também a **modalidade de autorização** exigida pela tabela do convênio
  (não requer / automática online / prévia com auditoria / OPME com anexo).
- Copiar os preços de uma tabela para outra (montar um convênio novo a partir de outro) → ferramenta de cópia de preços.
- Saber quais convênios a clínica atende → ferramenta de convênios.
- Consultar, montar, editar e aprovar orçamento (detalhe, pendências, gestão) → ferramentas de orçamento. O **detalhe** mostra o **desfecho do funil**: aprovado/recusado (por **quem** e **quando**), o **motivo da recusa** e o **aceite do cliente** — se aceitou, **em que data/hora** e **como** (vazio = ainda não aceitou). O **conteúdo** sensível do aceite (texto da declaração, IP, documento) **não** é exposto.
- Acompanhar a **assinatura eletrônica** do orçamento: quais estão **pendentes** da assinatura do paciente e se o **link foi aberto** (quantas vezes / quando — o caso "mandei o link e o paciente diz que não recebeu") → ferramentas de assinatura. **Enviar/reenviar** ou **revogar** o link do paciente é ação de envio (papel financeiro).
- Ver os **termos** disponíveis para anexar ao orçamento (por tipo, e qual é o **padrão**) → ferramenta que **lista os templates de termos**. Você **seleciona** o termo; **redigir/versionar o texto** é `designer-documentos`.
- Simular uma venda (memória de cálculo), simular o preço de um pacote, criar a venda a partir da simulação, converter um orçamento aprovado em venda e tocar o ciclo da venda → ferramentas de venda.
- Definir condições e formas de pagamento e simular o parcelamento → ferramentas de pagamento.
- Fazer o split de coparticipação e ancorar a autorização de convênio no item → ferramentas de pagador/autorização.
- Listar retornos pendentes → ferramenta de retornos.

**Feito na plataforma (ainda não por ferramenta):** **registrar** o aceite do cliente e a **edição do orçamento via simulação**, os **favoritos** do profissional e a **revisão de no-show**. A IA raciocina sobre isso, mas a **ação** hoje passa pela plataforma. (⚠️ apenas **registrar** o aceite é da plataforma — **consultar** se/quando o cliente aceitou já vem no detalhe do orçamento, acima.)

> Análise estratégica (reajuste em massa, histórico de preço, comparador de tabelas, simulador de margem, política de desconto) já existe no backend e está **a caminho** como ferramenta.

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
- Não cobre o **ciclo do dinheiro** (registrar/confirmar pagamento, parcelas, contas a receber, caixa) → `financeiro`; **faturamento/glosa TISS** → `faturamento-convenio`.
- Não cobre agenda/paciente → `secretaria`.
- Não expõe como preços são calculados/armazenados por dentro — só como **configurá-los, usá-los e pensá-los**.
