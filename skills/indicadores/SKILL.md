---
name: indicadores
description: A visão de GESTÃO/BI da clínica no Fluxo Ideal — o dashboard executivo que cruza agenda, comercial, atendimento, financeiro e satisfação num lugar só: ler os KPIs, abrir as quebras (drill-down por profissional/convênio/procedimento), comparar com o período anterior e ver a evolução no tempo. Ensina o que cada indicador significa em NEGÓCIO (ocupação, no-show, conversão, ticket médio, produção, DSO, inadimplência, TMA, NPS). Exportar a base crua é papel à parte (backup/DPO). Use para "como está a clínica?", "quero um panorama", "abre por profissional", "compara com o mês passado".
audience: [ia, humano]
depends_on: [indicadores, gestao, exportacao]
version: 0.2.1
updated: 2026-07-13
---

# Indicadores

A **camada de gestão** da clínica: a leitura executiva que junta números de vários domínios
(agenda, comercial, atendimento, financeiro, satisfação) num painel só para responder "como
a clínica está indo?". Aqui você **lê e interpreta** o placar; a operação por trás de cada
número mora nas skills de domínio.

## Quando usar
- "Como está a clínica?", "me dá um panorama / raio-x", "resumo executivo do mês".
- Ler um indicador de topo e o que ele significa: ocupação, no-show, conversão, ticket médio,
  produção, DSO, inadimplência, TMA, taxa de retorno, NPS.
- **Abrir a quebra** de um número (produção por profissional/convênio, margem por procedimento, aging
  por faixa, TMA de retorno × 1ª consulta…).
- **Comparar com o período anterior** (a variação de cada KPI, com o sentido) e ver a **evolução no tempo**.
- Comparar seções (a agenda está cheia mas a conversão caiu? o caixa aperta e a inadimplência subiu?).
- **Exportar a base crua** ("baixar tudo", "backup", "pro contador/Excel") — mas isso é um **papel à
  parte** (backup/DPO), não a leitura de BI; ver a seção de export.

## Quando NÃO usar
- **Operar** ou detalhar um número específico — a fonte de cada indicador vive na skill de domínio:
  - preço, tabela, orçamento, montar/fechar venda → `precificador`.
  - dinheiro depois da venda (parcelas, contas a receber com aging, contas a pagar, caixa,
    fluxo de caixa, ponto de equilíbrio, inadimplência caso-a-caso) → `financeiro`.
  - agenda, marcar/remarcar, dados do paciente → `secretaria`.
  - fila de atendimento, prontuário, tempos por atendimento → `auxiliar-medico`.
- Configurar o dashboard, criar indicador novo, mexer na pesquisa de satisfação → é administração
  (fora do escopo desta skill).

## Modelo mental

Indicadores é uma **leitura agregada de topo**, não uma nova fonte de dados. O painel **espelha**
o dashboard executivo da clínica: uma chamada devolve os KPIs já agrupados por **seção**, cada um
alimentado pelo domínio que é dono daquele número.

```
                        PAINEL DE INDICADORES (leitura de topo)
   ┌───────────┬──────────┬───────────┬─────────────┬────────────┬─────────────┐
   │ EXECUTIVA │  AGENDA  │ COMERCIAL │ ATENDIMENTO │ FINANCEIRO │ SATISFAÇÃO  │
   │ (o topo   │ ocupação │ produção  │ TMA         │ break-even │ NPS / CSAT  │
   │  dos KPIs │ no-show  │ ticket    │ taxa de     │ fluxo de   │ % promotores│
   │  de cada  │ compare- │ conversão │ retorno     │ caixa      │ nº respostas│
   │  seção)   │ cimento… │ margem…   │ …           │ projetado  │             │
   └─────┬─────┴────┬─────┴─────┬─────┴──────┬──────┴─────┬──────┴──────┬──────┘
         ▼          ▼           ▼            ▼            ▼             ▼
     (topo de    agenda      comercial   atendimento  financeiro   satisfação
      todas)                 (vendas)                              (pesquisas)
```

Quatro ideias que sustentam tudo:

- **Cada KPI carrega um estado, não só um número.** Um indicador vem com **valor** e um **status**:
  `ok`, `degradado` ou `indisponivel`. Se a fonte daquele número estiver fora do ar ou você não
  tiver acesso, o KPI vem `indisponivel` **com motivo** — **nunca com um número inventado**. Ler
  o status é parte de ler o indicador.
- **Nunca invente número.** Se a seção não veio, diga "indisponível" e o porquê. Um KPI degradado
  (ex.: entradas futuras subestimadas porque a fonte de recebíveis oscilou) **não é zero** — é um
  número parcial com aviso. Reporte o aviso junto.
- **Frescor varia por seção.** Alguns números são **ao vivo** (TMA/atendimento), outros têm um
  **cache curto** (agenda, alguns minutos). Para "agora mesmo", prefira o que é ao vivo e mencione
  a defasagem do que é cacheado.
- **Acesso é por seção.** A visão de cada pessoa depende do papel dela: recepção vê agenda, não vê
  financeiro. Uma seção pedida sem permissão vem sinalizada como **sem acesso** — de forma
  transparente, não como se estivesse vazia.

O **período** (data início/fim) e os filtros (**profissional**, **convênio**) recortam o painel.
Atenção: o filtro de convênio faz sentido para **agenda/atendimento**; o **comercial** e o
**financeiro** são da clínica inteira. Alguns indicadores (ex.: prazo médio de recebimento)
**exigem** um período definido — sem ele, vêm indisponíveis com um motivo acionável ("informe as
datas").

## Glossário — o que cada indicador significa em NEGÓCIO
> Aqui é o **significado de gestão** e **quando olhar**. O cálculo interno mora na skill de domínio.

**Executiva** — o topo: os poucos números que resumem a saúde geral (ocupação, no-show, produção,
conversão, TMA, taxa de retorno). É por onde começar um panorama.

**Agenda** (fonte: agenda)
- **Ocupação (%)**: quão cheia está a agenda — capacidade usada. Baixa = cadeira vazia (receita perdida);
  alta demais sem folga = risco de atraso. É o termômetro de demanda × capacidade.
- **No-show (%)**: faltas. Dinheiro e horário perdidos; alto pede confirmação ativa / política de multa.
- **Comparecimento (%)**: o espelho do no-show — quem realmente veio.
- **Confirmação (%)**: quantos confirmaram antes. Confirmação baixa tende a preceder no-show alto.
- **Encaixe (%)**: proporção de encaixes — mede pressão de demanda sobre a agenda.
- **Retorno (%)** (agenda): fatia de retornos — indício de continuidade de cuidado / fidelização.

**Comercial** (fonte: vendas)
- **Produção (R$)**: quanto a clínica **vendeu** no período (volume de negócio fechado).
- **Ticket médio (R$)**: valor médio por venda — sobe com upsell/pacotes, cai com muita venda pequena.
- **Conversão de orçamentos (%)**: dos orçamentos feitos, quantos viraram venda. Mede a eficácia
  comercial (proposta → fechamento). Conversão baixa com muitos orçamentos = oportunidade escapando.
- **Margem de contribuição (R$ e %)**: o que sobra de cada venda depois dos custos diretos, para
  cobrir os custos fixos. É a base do ponto de equilíbrio (ver `financeiro`).
- **Carteira a receber (R$)**: total que os pacientes ainda devem (parcelas em aberto). O detalhe
  por faixa de atraso (aging) e caso-a-caso é do `financeiro`.
- **DSO (dias)**: prazo médio de recebimento — em quantos dias, em média, a clínica recebe. Alto =
  dinheiro preso; sobe quando parcelamento estica ou inadimplência cresce. **Exige período.**
- **Inadimplência (%)**: fatia da carteira em atraso vs o total. Sobe = risco de caixa.

**Atendimento** (fonte: atendimento) — números **ao vivo**
- **TMA (min)**: tempo médio de atendimento. Muito alto = gargalo/sala travada; muito baixo pode
  indicar atendimento apressado. Lê a eficiência operacional da porta pra dentro.
- **Taxa de retorno (%)** (atendimento): fatia de atendimentos que são retorno — continuidade do cuidado.
- **Total de atendimentos**: volume realizado no período.

**Financeiro** (fonte: financeiro) — o corte executivo; o operacional é a skill `financeiro`
- **Ponto de equilíbrio / break-even (R$)**: quanto a clínica precisa **faturar** para não ter
  prejuízo no período. Depende da margem (do comercial) — se a margem não veio, o número **degrada**
  (não é zero); margem ≤ 0 deixa o break-even **indefinido**.
- **Fluxo de caixa projetado (saldo final, R$)**: para onde o caixa caminha no horizonte. Se a fonte
  de recebíveis oscilar, a projeção mostra **só as saídas** e vem **degradada** (entradas subestimadas)
  — leia o aviso, não trate como caixa zerado de entradas.

**Satisfação** (fonte: pesquisa de satisfação ativa da clínica) — **só agregados numéricos**
- **NPS (score, -100 a 100)**: lealdade — promotores menos detratores. Termômetro de recomendação.
- **% Promotores / % Detratores**: a composição por trás do NPS.
- **Nota média (CSAT, 0–10)**: satisfação média declarada.
- **Total de respostas**: base amostral — NPS com pouquíssimas respostas é frágil; olhe o total antes de concluir.
- **Nunca** há texto livre / comentário do paciente aqui — a seção lê **só números** (privacidade).

## Ferramentas (tarefa → ferramenta)
> A execução depende de **autorização** — o MCP aplica permissão; a skill só ensina a intenção e o
> _quando_. Você só recebe as seções que seu papel permite; as demais vêm sinalizadas como sem acesso.

**Ler o painel**
- Panorama executivo / "como está a clínica" / qualquer KPI de gestão → a ferramenta do **dashboard
  de indicadores**. Numa chamada devolve as seções (executiva, agenda, comercial, atendimento,
  financeiro, satisfação); dá pra pedir **uma seção** específica ou **todas**, e recortar por
  **período**, **profissional** e **convênio**.
  - Sempre **leia o `status` de cada KPI** antes de reportar. `indisponivel`/`degradado` vêm com
    motivo — repasse o motivo, não invente número.
  - Para "agora": prefira os KPIs ao vivo (atendimento); avise que agenda tem cache curto.
  - Para DSO e afins que dependem de período: informe **data início e fim**.

**Aprofundar o painel (drill-down)**
- Abrir as **quebras** de um KPI de topo — sair do "quanto" para o "de onde vem": produção **por
  profissional** e **por convênio**; conversão de pacientes **novos × já existentes**; **margem** por
  procedimento / profissional / convênio; a carteira **por faixa de atraso** (aging) e o DSO **a prazo ×
  total**; os **recebíveis de convênio** e a **reconciliação de convênio**; o TMA de **retorno × 1ª
  consulta** → a ferramenta de **drill-down** do painel.

**Comparar períodos**
- "Este período × o anterior" — a **variação** de cada KPI (em % e absoluta), já com o **sentido** (se
  subir é bom ou ruim), e o período anterior **derivado sozinho** (você só informa o período atual) → a
  ferramenta de **comparação de períodos**.

**Evolução no tempo (série)**
- A **curva ao longo do tempo** (por mês / semana / dia) — o que o "total do período" não mostra → a
  ferramenta de **série temporal**, escolhendo a **fonte**: **produção** (vendas) · **agenda** (no-show /
  ocupação / comparecimento) · **atendimento** (TMA / taxa de retorno) · **financeiro** (despesas pagas /
  caixa realizado — o **histórico**, não a projeção futura). *Os filtros variam por fonte:* **convênio** só
  vale em produção; **profissional** vale em produção / agenda / atendimento; o financeiro filtra por
  **plano de contas / centro de custo / conta**.

**Exportar a base crua (papel à parte — NÃO é do BI)**
- "Exporta tudo em Excel / backup / pro contador" gera a **base crua** da clínica (dados pessoais **sem
  máscara**) — o maior ponto de saída de dado. Por isso **não faz parte do papel de BI**: disparar o
  export é uma permissão **separada** (papel de **backup / DPO**). Se você não a tem, o export **não está
  no seu alcance** — leia/interprete o painel e encaminhe o pedido a quem cuida de backup.
- Quando **é** o seu papel: a **senha** do ZIP é **fornecida pelo humano** (a IA **nunca** a inventa nem
  a guarda) e o **link de download não é repassado pela IA** — ele chega por **notificação ao próprio
  disparador** do job. A IA pode acompanhar o **estado** (aguardando / processando / pronto / erro), mas
  **não entrega o link**. Sem a senha, o ZIP não abre.

**Ordem mental para um panorama:** executiva (o topo) → aprofunde a seção que chamou atenção com o
**drill-down** → **compare** com o período anterior / olhe a **série** → cheque o status de cada KPI.

## Fluxos comuns

### "Como está a clínica este mês?"
1. Peça o painel de **todas as seções** com o **período** do mês.
2. Comece pela **executiva** (topo), depois destrinche onde há sinal (ex.: agenda cheia mas conversão baixa).
3. Para cada KPI, **leia o status**: reporte `indisponivel`/`degradado` com o motivo — nunca preencha buraco com número inventado.
4. Cruze histórias: no-show alto + confirmação baixa; carteira grande + DSO/inadimplência subindo;
   produção alta + margem baixa (vendendo muito, ganhando pouco).

### "A recepção pediu um panorama e não veio o financeiro"
- Normal: acesso é **por seção**. As seções sem permissão vêm **sinalizadas como sem acesso** — diga
  isso com transparência ("seu perfil não vê a seção financeira"), não trate como "está zerado".

### "Quero um raio-x só do comercial, por profissional"
- Peça **a seção comercial** filtrando por **profissional**. Lembre: o filtro de **convênio** não se
  aplica ao comercial (é da clínica inteira); use-o para agenda/atendimento.

### "Exporta tudo pra eu mandar pro contador"
1. Confirme o **papel**: exportar a base crua é de **backup/DPO**, não do BI. Se o usuário não tem essa
   permissão, o export não aparece — leia/interprete o painel e encaminhe a quem faz backup.
2. Sendo o papel certo: a **senha** é **do humano** (ele define e anota; a IA não inventa nem guarda).
3. Acompanhe o **estado** do job (aguardando / processando / pronto / erro). O **link de download não é
   entregue pela IA** — chega por **notificação ao disparador**. Exports grandes podem ir pra **madrugada**.

## Regras e invariantes
- **Nunca invente número.** KPI sem fonte = `indisponivel` com motivo; KPI parcial = `degradado`
  com aviso. Ambos são reportados como tais — jamais como zero nem como valor cheio.
- **Status faz parte do indicador.** Ler o valor sem ler o status é ler errado.
- **Frescor importa.** Distinga números ao vivo (atendimento) de cacheados (agenda) ao falar de "agora".
- **Acesso é por seção** — seção sem permissão é sinalizada, não silenciada.
- **Filtros têm alçada:** convênio vale para agenda/atendimento; comercial e financeiro são da clínica
  inteira; DSO e similares exigem período.
- **Satisfação é só agregado** — nunca comentário/texto livre do paciente.
- **Export é papel à parte e protege o dado:** disparar a base crua é permissão **separada** (backup/DPO),
  fora do BI. A senha é **do humano** (a IA não inventa nem guarda) e o **link não é repassado pela IA**
  (vai por notificação ao disparador). Perder a senha = perder o acesso ao arquivo.
- **Indicadores é leitura.** Nada aqui altera agenda, venda, caixa ou paciente (o export é um backup
  de saída, não uma mutação). Ação/operação é nas skills de domínio.

## Limites / o que esta skill NÃO cobre
- O **cálculo interno** de cada número e a **operação** por trás dele — vive na skill de domínio
  (`financeiro`, `precificador`, `secretaria`, `auxiliar-medico`). Aqui é só o **significado de
  gestão** e **quando olhar**.
- **Agir** sobre um indicador (cobrar um inadimplente, remarcar um no-show, fechar uma venda) → skill de domínio.
- **Configurar** o dashboard, criar indicadores, administrar a pesquisa de satisfação → administração, fora do escopo.
- **Alertas / metas automáticos por KPI** (avisar quando um número cruza um limite) **não existem** ainda —
  o acompanhamento é manual (leia e compare você mesmo).
- Não expõe como os indicadores são compostos/consultados por dentro — só como **lê-los, interpretá-los, aprofundá-los e compará-los**.
