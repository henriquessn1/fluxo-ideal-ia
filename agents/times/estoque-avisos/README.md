# estoque-avisos — avisa a equipe sobre validade, mínimo e prazo do consignado

Time de **1 agente `script`** que, **uma vez por dia útil (8h, fuso da clínica)**, junta os alertas novos do estoque
num **único resumo** e avisa os papéis da equipe que a clínica escolheu:

```text
Estoque: 3 alertas novos
Urgente: 1 lote vencido.
Atenção: 1 lote perto de vencer, 1 item abaixo do mínimo.
• Vencido: Fio de sutura 3-0 · Sala 1 · lote L123 · validade 20/10/2026 (venceu há 9 dias) · 4 no local
• Vence logo: Anestésico · Sala 2 · lote A9 · validade 05/11/2026 (vence em 7 dias) · 12,5 no local
• Abaixo do mínimo: Gaze · Sala 1 · 3 de mínimo 5
```

O aviso aparece no sino da Central, com o link para o estoque (onde fica o painel de alertas com o detalhe).

## O que faz

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

## Capabilities que pede (superfície de consentimento)

| Grant | Para quê |
|---|---|
| `estoque:ler` | ler os alertas do estoque e marcar o que já foi avisado (a marca não muda o estoque) |
| `notificacao:enviar` | avisar os papéis escolhidos |
| `notificacao:broadcast` | avisar toda a equipe conectada, só com "Avisar toda a equipe conectada" ligado |

As ações citam as capabilities `estoque.listar_alertas`, `estoque.marcar_alertas_avisados`,
`notificacao.notificar_grupo` e `notificacao.notificar`. O endereço real é resolvido em privado na instalação.

## Cartão de risco: **baixo**

- 🏠 **Só interno:** avisa a equipe no sino da Central. **Não** fala com paciente e **não** manda nada para fora do
  sistema (sem WhatsApp, sem e-mail).
- 🔒 **Não lê dado de paciente:** só produto, local, lote, validade, remessa, fornecedor e quantidade.
- ✋ **Ações:** ler os alertas do estoque, avisar a equipe e marcar o alerta como avisado. Não movimenta estoque, não
  altera mínimo nem configuração.
- ⏰ **Age sozinho** no horário agendado.

## Valores da clínica (na instalação)

| Valor | Padrão | O que faz |
|---|---|---|
| Papéis que recebem o aviso | `administrador` | um ou mais papéis da equipe (vários: separados por vírgula) |
| Avisar toda a equipe conectada | desligado | ligado: avisa todos que estão na Central, no lugar dos papéis |
| Avisar lote vencido ou perto de vencer | ligado | desliga os dois tipos de validade |
| Avisar saldo abaixo do mínimo do local | ligado | desliga o tipo do mínimo |
| Avisar consignado vencido ou perto do prazo | ligado | desliga os dois tipos do consignado |
| Também como notificação do Windows/navegador | ligado | além do cartão na Central |

Outros ajustes do agente (configuração, sem redeploy):
- `tipos`: liga/desliga cada um dos 5 tipos separadamente (`validade_vencida`, `validade_proxima`, `abaixo_minimo`,
  `consignado_prazo_vencido`, `consignado_prazo_proximo`);
- `max_linhas` (`10`, até 30): quantas linhas de detalhe entram no aviso;
- `link` (`/financeiro/estoque`): para onde o aviso leva.

A **antecedência** dos avisos de validade e de consignado é da configuração do estoque, não deste time. O **horário**
é o "Quando roda" do agente: a clínica muda o dia e a hora ali (o padrão é dia útil às 8h, no fuso de São Paulo).

## Instalação (Central → Inteligência Artificial → Importar)

1. **Antes:** o estoque com os alertas já deployado (a permissão `estoque:ler` precisa estar registrada), e o serviço
   de agentes com as capabilities do estoque e com acesso ao estoque. Sem isso, a primeira rodada falha ao listar os
   alertas (aparece como `acao_bloqueada` na execução).
2. Importe este `manifest.json`, escolha os papéis que recebem o aviso e conceda ao service-account os 3 grants acima.
3. Ligue o agente. Confira a primeira execução em "execuções": `alertas` e `marcados` devem bater.
