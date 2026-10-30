# estoque-avisos — avisa a equipe, abre a tarefa de reposição e manda o relatório ao fornecedor do consignado

Time de **3 agentes `script`** (sem IA, sem custo de token) que cuida do que o estoque pede de rotina:

| Agente | Quando roda (padrão, fuso de São Paulo) | O que faz |
|---|---|---|
| **`estoque_avisos`** | dia útil às 8h | junta os alertas novos (validade, mínimo, prazo do consignado) num **resumo** para os papéis escolhidos |
| **`estoque_reposicao`** (novo na 1.1) | dia útil às 7h30 | abre **uma tarefa de reposição por produto × local** que caiu abaixo do mínimo |
| **`estoque_relatorio_fornecedor`** (novo na 1.1) | segunda às 9h | manda por **e-mail a cada fornecedor do consignado** o que foi usado e ainda aguarda reposição |

Cada agente tem o **seu papel** (service-account com as permissões só do que ele faz) e pode ser ligado ou
desligado sozinho na Central.

## 1. `estoque_avisos` — o resumo à equipe

Uma vez por dia útil, junta os alertas novos do estoque num **único resumo** e avisa os papéis da equipe que a
clínica escolheu:

```text
Estoque: 3 alertas novos
Urgente: 1 lote vencido.
Atenção: 1 lote perto de vencer, 1 item abaixo do mínimo.
• Vencido: Fio de sutura 3-0 · Sala 1 · lote L123 · validade 20/10/2026 (venceu há 9 dias) · 4 no local
• Vence logo: Anestésico · Sala 2 · lote A9 · validade 05/11/2026 (vence em 7 dias) · 12,5 no local
• Abaixo do mínimo: Gaze · Sala 1 · 3 de mínimo 5
```

O aviso aparece no sino da Central, com o link para o estoque (onde fica o painel de alertas com o detalhe).

| Gatilho | Comportamento |
|---|---|
| `cron` `0 8 * * 1-5` (`America/Sao_Paulo`) | lista os alertas do estoque **ainda não avisados** → guarda os tipos ligados → manda **um** resumo para cada papel escolhido → marca os alertas como avisados |

- **Alertas que entram** (calculados pelo estoque na hora da consulta):
  - **lote vencido**: lote com saldo e validade passada (urgente);
  - **lote perto de vencer**: validade dentro da antecedência da configuração do estoque (padrão 30 dias);
  - **abaixo do mínimo**: saldo do local menor ou igual ao mínimo do local (urgente quando o saldo é zero);
  - **consignado com prazo vencido** e **consignado perto do prazo**: só com o consignado ligado.
- **Um resumo por rodada:** contagem por severidade e tipo (urgente primeiro) e as primeiras linhas (`max_linhas`,
  padrão 10): produto, local, lote e validade, ou remessa (nota e fornecedor) e prazo, e a quantidade ou o mínimo.
  Os alertas não trazem nenhum dado de paciente.
- **Sem aviso repetido:** depois do aviso, o time marca cada alerta como avisado no estoque. O alerta só volta se a
  condição sumir e aparecer de novo (ex.: o saldo foi reposto e caiu outra vez).
- **Falha no aviso não marca:** se o aviso não chegar a todos os papéis, nada é marcado e os alertas voltam na rodada
  seguinte (melhor repetir do que perder). O resumo da execução fica com `acao_bloqueada`.
- **Sem nada novo, sai limpo:** sem alerta, ou só com tipos desligados, não manda aviso.
- **Lista grande:** o estoque devolve até 1000 alertas por consulta. As contagens do aviso valem para todos, e o que
  não coube na lista é avisado na rodada seguinte.

O resumo de cada rodada (Central → Inteligência Artificial → execuções) mostra `alertas`, `na_lista`, `por_tipo`,
`destinos`, `avisados`, `marcados`, `ignorados` e `falhas_aviso` (+ `truncado`, `acao_bloqueada` e `etapa` quando for o
caso). Sem nome de produto e sem dado pessoal.

## 2. `estoque_reposicao` — a tarefa de reposição

| Gatilho | Comportamento |
|---|---|
| `cron` do knob `cron_reposicao` (padrão `30 7 * * 1-5`, `America/Sao_Paulo`) | lista os alertas **abaixo do mínimo ainda sem tarefa** → abre **uma tarefa por produto × local** para o papel de `papel_reposicao` → marca o alerta como "com tarefa" |

- **A tarefa:** título "Repor <produto> em <local>", prioridade **alta** quando o local está sem saldo (senão
  média), a descrição com **físico × mínimo** do local e o **link para o produto** no estoque. O responsável é o
  **papel** (tarefa do grupo — quem do papel pegar, assume).
- **Sem tarefa repetida:** logo depois que a tarefa nasce, o alerta ganha a marca "com tarefa" (uma marca própria,
  separada da do resumo — o resumo das 8h continua avisando normalmente). A marca **cai sozinha quando a condição
  some** (o saldo voltou acima do mínimo); se cair de novo, nasce outra tarefa.
- **Duplicata rara, aceita:** a tarefa não tem chave de idempotência. Se a tarefa nascer e a marca falhar, a rodada
  seguinte pode abrir **outra tarefa para o mesmo item** — é o preço aceito para nunca deixar de abrir. A falha da
  marca fica no log e no resumo (`acao_bloqueada`, `etapa: marcar_com_tarefa`).
- **Falha ao listar** (inclusive 409 do estoque) **ou ao abrir a tarefa:** log + `acao_bloqueada`, sem marcar — o
  alerta volta na rodada seguinte.
- **Teto por rodada:** `max_por_rodada` (50, até 200) tarefas; o resto vai na próxima (`adiados` no resumo).
- **Não lê dado de paciente** (só produto, local e quantidades).

Resumo da rodada: `alertas`, `tarefas`, `marcados`, `falhas_tarefa`, `falhas_marca` (+ `adiados`, `truncado`,
`acao_bloqueada`, `etapa`). Sem nome de produto.

## 3. `estoque_relatorio_fornecedor` — o relatório ao fornecedor do consignado

| Gatilho | Comportamento |
|---|---|
| `cron` do knob `cron_relatorio` (padrão `0 9 * * 1`, `America/Sao_Paulo`) | lista o consumo de consignado que **ainda aguarda reposição** nos últimos `dias_janela` dias → agrupa por fornecedor → manda **um e-mail por fornecedor** → avisa a gestão do que não pôde ir |

- **Período:** tudo o que foi usado nos últimos `dias_janela` dias (padrão 90) e **ainda aguarda reposição**. É um
  **lembrete que repete** toda semana até alguém marcar "reposto" no estoque (ou a nota de faturamento do fornecedor
  casar com o consumo). O agente **nunca marca "reposto"**.
- **Consignado desligado** na clínica → sai limpo, sem erro.
- **Uma vez por semana por fornecedor:** o e-mail leva a chave `estoque-relatorio:<fornecedor>:<semana ISO>` (sem dado
  pessoal). Rodar de novo na mesma semana não manda outro e-mail (`deduplicados` no resumo).
- **Não envia e avisa a gestão** (`papel_gestao`, um aviso por rodada com a lista) quando:
  - o fornecedor **não tem e-mail** no cadastro do financeiro, ou **não foi encontrado**;
  - a identificação do paciente de alguma linha **não pôde ser lida** porque o cadastro de pacientes estava fora do
    ar — o relatório incompleto não sai; vai na rodada seguinte.
- **Identificação vazia por outro motivo** (paciente sem nome, consumo sem atendimento) sai como "—" e o e-mail vai.
- **O e-mail** sai pelo modelo `template_slug` (criado pela clínica — ver Instalação), com as linhas nas variáveis do
  modelo. Sem anexo.
- **Falha ao ler o fornecedor ou ao enviar:** log + `acao_bloqueada`; a próxima rodada tenta de novo.

Resumo da rodada: `linhas`, `fornecedores`, `enviados`, `deduplicados`, `agendados`, `sem_email`, `nao_encontrado`,
`paciente_incompleto`, `falhas_envio`, `sem_envio`, `semana`, `dias_janela` (+ `acao_bloqueada`, `etapa`). **Nunca** o
e-mail do fornecedor nem a identificação do paciente.

### Variáveis que o modelo de e-mail recebe

| Variável | Conteúdo |
|---|---|
| `fornecedor_nome` | nome do fornecedor no cadastro |
| `periodo_desde`, `periodo_ate` | a janela (dd/mm/aaaa) |
| `semana` | a semana ISO do envio (ex.: `2026-W44`) |
| `total_linhas`, `total_quantidade` | quantas linhas e a soma das quantidades |
| `linhas_omitidas` | linhas que não couberam (`max_linhas_email`, padrão 300) — o resto está no relatório do estoque |
| `linhas` | lista; cada uma com `data`, `produto`, `codigo`, `lote`, `validade`, `serie`, `quantidade`, `remessa_nf` e `paciente` (a identificação escolhida no estoque, ou "—") |

## Capabilities que pede (superfície de consentimento)

| Papel (service-account) | Grants | Para quê |
|---|---|---|
| `botfn-estoque-avisos` | `estoque:ler`, `notificacao:enviar`, `notificacao:broadcast` | ler os alertas, avisar os papéis (ou todos, com "Avisar toda a equipe conectada") e marcar o que foi avisado |
| `botfn-estoque-reposicao` | `estoque:ler`, `tarefas:criar` | ler os alertas abaixo do mínimo sem tarefa, abrir a tarefa e marcar o alerta (a marca não muda o estoque) |
| `botfn-estoque-relatorio` | `estoque:consignado`, `fornecedor:list`, `mensageria_mensagem:enviar_intencao`, `notificacao:enviar` | ler o consumo do consignado, ler o e-mail do fornecedor, enviar o e-mail e avisar a gestão |

As ações citam as capabilities `estoque.listar_alertas`, `estoque.marcar_alertas_avisados`,
`estoque.listar_alertas_sem_tarefa`, `estoque.consumo_consignado_aguardando`, `financeiro.obter_fornecedor`,
`tarefas.criar`, `mensageria.enviar_intencao`, `notificacao.notificar_grupo` e `notificacao.notificar`. O endereço
real é resolvido em privado na instalação.

## Cartão de risco: **alto** (por causa do relatório ao fornecedor)

| | `estoque_avisos` | `estoque_reposicao` | `estoque_relatorio_fornecedor` |
|---|---|---|---|
| Fala com quem | equipe (sino da Central) | equipe (tarefa) | **terceiro externo** — o fornecedor, **por e-mail** |
| Dado de paciente | não | não | **sim, mínimo**: a identificação escolhida no estoque (padrão = nº do atendimento) ligada ao material usado |
| Age sozinho | sim, no horário | sim, no horário | sim, no horário |
| Muda dado | marca "avisado" | abre tarefa, marca "com tarefa" | não (não marca "reposto") |
| Risco | baixo | baixo | **alto** |

**Base legal do relatório ao fornecedor (LGPD — Lei 13.709/2018,
[texto no Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm), conferido em
30/10/2026):**

- "o paciente X usou o material Y" é **dado pessoal sensível referente à saúde** (art. 5º, II); mandar ao fornecedor é
  **tratamento** (art. 5º, X).
- **Base:** **art. 11, II, "d"** — exercício regular de direitos em contrato (a prestação de contas do material
  consignado ao fornecedor, que só fatura e repõe o que foi usado) — e **art. 11, §4º, II** — comunicação/uso
  compartilhado permitido para as **transações financeiras e administrativas** decorrentes da prestação do serviço de
  saúde.
- **Não** é obrigação legal: o Ajuste SINIEF 2/2024 (retorno simbólico do consignado) **não** exige identificar o
  paciente (a cláusula 10ª deixa a UF exigir mais — confira a da clínica).
- **Minimização** (art. 6º, III): o padrão é o **nº do atendimento**; iniciais ou nome só se a clínica escolher na
  configuração do consignado no estoque. **Nunca** diagnóstico, CID ou prontuário.
- **Guarda:** a mensageria **guarda as variáveis** de cada mensagem enviada (o histórico do envio) — inclusive a
  identificação escolhida. Ela fica no histórico da mensagem da clínica.
- O e-mail do fornecedor é usado **só como destinatário**; não vai para log nem para o resumo da execução.

## Valores da clínica (na instalação)

| Valor | Padrão | O que faz |
|---|---|---|
| Papéis que recebem o aviso | `administrador` | um ou mais papéis da equipe (vários: separados por vírgula) |
| Avisar toda a equipe conectada | desligado | ligado: avisa todos que estão na Central, no lugar dos papéis |
| Avisar lote vencido ou perto de vencer | ligado | desliga os dois tipos de validade |
| Avisar saldo abaixo do mínimo do local | ligado | desliga o tipo do mínimo (no resumo; a tarefa de reposição é do outro agente) |
| Avisar consignado vencido ou perto do prazo | ligado | desliga os dois tipos do consignado |
| Também como notificação do Windows/navegador | ligado | além do cartão na Central (resumo e aviso à gestão) |
| `papel_reposicao` — papel que recebe a tarefa de reposição | `administrador` | um papel só |
| `cron_reposicao` — quando abrir as tarefas | `30 7 * * 1-5` | cron de 5 campos, fuso de São Paulo |
| `papel_gestao` — papel avisado quando o relatório não pode ir | `administrador` | um papel só |
| `dias_janela` — janela do relatório (dias) | `90` | de 1 a 366 |
| `template_slug` — modelo de e-mail do relatório | `estoque_relatorio_fornecedor` | o modelo criado no passo 3 da instalação |
| `cron_relatorio` — quando mandar o relatório | `0 9 * * 1` | cron de 5 campos, fuso de São Paulo |

Outros ajustes (configuração do agente, sem redeploy):
- `estoque_avisos`: `tipos` (liga/desliga cada um dos 5 tipos), `max_linhas` (`10`, até 30), `link`;
- `estoque_reposicao`: `max_por_rodada` (`50`, até 200), `link` (`/financeiro/estoque`; a tarefa leva
  `?item=<produto>`);
- `estoque_relatorio_fornecedor`: `max_linhas_email` (`300`, até 1000), `link` (para o aviso à gestão),
  `fuso_horas` (`-3`: o "hoje" e a semana ISO do envio).

A **antecedência** dos avisos de validade e de consignado é da configuração do estoque, não deste time. O
**horário** também pode ser mudado no "Quando roda" de cada agente.

## Instalação (Central → Inteligência Artificial → Importar)

1. **Antes:**
   - o estoque com os alertas e a **marca por canal** deployado (a 1.1 usa a marca "com tarefa" e o campo de
     identificação incompleta do relatório do consignado);
   - o serviço de agentes com as capabilities do estoque e do fornecedor, e com acesso ao estoque;
   - o **e-mail do fornecedor** no cadastro do financeiro (fornecedor sem e-mail não recebe — a gestão é avisada);
   - o **consignado ligado** no estoque, e a **identificação do paciente** escolhida (padrão: nº do atendimento),
     se a clínica usar o relatório ao fornecedor.
2. Importe este `manifest.json`, escolha os papéis e conceda aos 3 service-accounts os grants acima.
3. **Crie o modelo de e-mail** no designer de mensagens da Central, canal **e-mail**, com o slug
   `estoque_relatorio_fornecedor` (ou outro, e informe em `template_slug`). O modelo aceita laço sobre as linhas;
   um ponto de partida:

   ```text
   Assunto: Consumo de material consignado — {{ fornecedor_nome }} ({{ periodo_desde }} a {{ periodo_ate }})

   Olá, {{ fornecedor_nome }}.
   Segue o material consignado usado na clínica que ainda aguarda reposição ({{ total_linhas }} itens):

   {% for l in linhas %}- {{ l.data }} · {{ l.produto }}{% if l.codigo %} ({{ l.codigo }}){% endif %}{% if l.lote %} · lote {{ l.lote }}{% endif %}{% if l.serie %} · série {{ l.serie }}{% endif %} · qtd {{ l.quantidade }} · NF remessa {{ l.remessa_nf }} · atendimento {{ l.paciente }}
   {% endfor %}{% if linhas_omitidas %}… e mais {{ linhas_omitidas }} linhas (peça o relatório completo).{% endif %}

   Por favor, emita o faturamento e a reposição. Este e-mail se repete toda semana até a reposição ser registrada.
   ```
   Não coloque no modelo nada além do que as variáveis trazem (nada de diagnóstico ou procedimento).
4. Ligue os agentes que a clínica quer. Confira a primeira execução de cada um em "execuções":
   - `estoque_avisos`: `alertas` e `marcados` devem bater;
   - `estoque_reposicao`: `tarefas` e `marcados` devem bater, e as tarefas aparecem no quadro do papel;
   - `estoque_relatorio_fornecedor`: `enviados` + `sem_envio` = `fornecedores`; rode de novo na mesma semana e veja
     `deduplicados`.
