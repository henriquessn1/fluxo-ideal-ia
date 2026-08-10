# confirmacao-diaria — varredura diária de confirmação de consulta

Time de **1 agente `script`** que, **uma vez por dia**, junta os agendamentos de **hoje + amanhã**
que o paciente **ainda não confirmou** e dispara **uma campanha de WhatsApp** convidando à
confirmação (1 mensagem por agendamento). É só a **ida** — a resposta do paciente (o clique do
botão) é tratada pelo time [confirmacao-presenca](../confirmacao-presenca/), que confirma o
agendamento. Os dois se complementam: este **convida**, aquele **recebe**.

## O que faz

| Gatilho | Comportamento |
|---|---|
| `cron` (1×/dia) | lista os agendamentos **não confirmados** de hoje+amanhã → monta 1 destinatário por agendamento (levando o vínculo do agendamento) → dispara a campanha com o template de confirmação |

- **Quem entra:** agendamento **público**, ainda **não confirmado** (nem pela recepção, nem pelo
  paciente) e sem recusa, fora dos status terminais (`Cancelado`/`Falta`/…).
- **Antecedência mínima (mesmo dia):** para HOJE, só entram consultas que começam a partir de
  `agora + min_lead_minutos` (não faz sentido pedir confirmação de algo perto demais). Para AMANHÃ,
  sem filtro de horas.
- **Uma mensagem por agendamento:** quem tem consulta hoje **e** amanhã recebe as duas, e confirma
  cada uma — o vínculo do agendamento viaja em cada envio para a resposta cair no lugar certo.

## Capabilities que pede (superfície de consentimento)

| Grant | Para quê |
|---|---|
| `agendamento:list` | listar os agendamentos não confirmados da janela |
| `campanha:disparar` | criar/agendar a campanha em lote |

As ações citam as capabilities `agendamento.listar_agendamentos` e `interacoes.agendar_campanha` —
o endereço real é resolvido em privado na instalação. **Risco: médio** (envia mensagem ao paciente;
não lê prontuário; age sozinho no horário configurado).

## Config editável por-clínica (sem redeploy)

- `min_lead_minutos` (`120`): antecedência mínima para o mesmo dia (2h).
- `tz_offset` (`-03:00`): fuso da clínica — usado para decidir "que dia é" e para exibir o horário.
- `status_pular`: status ignorados (`Cancelado`, `Falta`, `Atendido`, `Realizado`).
- `per_page` (`100`): tamanho de página da varredura.
- `canal_policy` (`so_whatsapp`): política de canal da campanha.
- `template_slug` (`confirmar_presenca`): o template de confirmação (o mesmo que arma o time de volta).
- `nome_campanha`: prefixo do nome da campanha do dia.

> **Fuso é levado a sério:** a decisão de dia e o horário exibido saem do **instante absoluto** de
> cada agendamento trazido para o `tz_offset` da clínica — não de fatiar texto — para não errar a
> virada de meia-noite quando o horário vier em UTC.

## Instalação (Central → Inteligência Artificial → Importar)

1. Importe este `manifest.json` (cole o link na tela de importar).
2. Conceda ao service-account os grants `agendamento:list` e `campanha:disparar`.
3. Ajuste, se quiser, a **hora do disparo** (o `cron`) e o `min_lead_minutos`.

> **Atenção ao ligar:**
> - **Hora do cron** é avaliada no fuso do agendador — confira se `0 12` corresponde às 9h locais.
> - **Não duplicar:** se a clínica já envia confirmação por consulta (véspera), decida qual fica —
>   este time é a varredura diária em lote (rede de segurança), não some com a outra automaticamente.
