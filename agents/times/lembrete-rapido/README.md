# lembrete-rapido — lembrete pelo WhatsApp ~2h antes do agendamento

Time de **1 agente `script`** (perfil `mensageiro`) que, **a cada 15 minutos**, manda um lembrete pelo
WhatsApp para os agendamentos cujo horário de envio já chegou:

> "Olá, Maria! Lembrete: seu agendamento com Dra. Beatriz é hoje, às 15:30. Até já!"

O texto **não cita o tipo de serviço** (o agendamento pode ser consulta, exame, retorno, cirurgia…).
Substitui o lembrete rápido que hoje mora no orquestrador ([fluxo-ideal#788](https://github.com/henriquessn1/fluxo-ideal/issues/788)).

## O que faz

| Gatilho | Comportamento |
|---|---|
| `cron` a cada 15 min (`America/Sao_Paulo`) | lista os agendamentos que começam até daqui a `antecedencia_minutos` → para cada um cujo **horário de envio** já chegou, pede o envio à mensageria (intenção de envio, 1 por agendamento) |

- **Horário de envio** = o mais tarde entre *início − `antecedencia_minutos`* e *`hora_minima` do dia da
  consulta*. Ex.: consulta 15:30 → 13:30; consulta 08:30 → 08:00 (nunca antes das 8h).
- **Quem recebe:** agendamento **público**, fora de status terminal (`Cancelado`/`Falta`/`Finalizado`),
  com paciente, que ainda não começou. **Confirmados e não confirmados** recebem.
- **Quem NÃO recebe (pula):**
  - **marcado em cima da hora** — criado depois do horário de envio (já dentro das 2h);
  - **atrasado** — passou mais de `atraso_max_minutos` do horário de envio (ex.: o agente ficou parado):
    melhor não mandar do que mandar "2h antes" a 20 minutos da consulta.
- **Sem duplicar:** cada envio leva a chave `lembrete_rapido:<agendamento>:<início em UTC>`. Rodar de novo devolve
  `deduplicado`; **reagendar** muda o início e gera um lembrete novo; **cancelar** antes do envio não envia.
- **Falha aparece:** se listar falhar, ou o envio voltar com erro (ex.: template ausente) ou com status fora de
  `aceito`/`deduplicado`/`agendado`, a rodada conta como **falha**, loga WARNING e marca `acao_bloqueada` no
  resumo da execução — nunca vira "enviado".

O resumo de cada rodada (Central → Inteligência Artificial → execuções) mostra `candidatos`, `enviados`,
`deduplicados`, `agendados`, `aguardando`, `pulado_em_cima`, `pulado_atrasado`, `sem_janela` (consulta antes da hora mínima) e `falhas` (+ `truncado` se a lista passar de 20 páginas) — sem dado pessoal.

## Capabilities que pede (superfície de consentimento)

| Grant | Para quê |
|---|---|
| `agendamento:list` | listar os agendamentos da janela |
| `cliente:read:full` | 1º nome do paciente para a mensagem |
| `profissionais:read` | apelido do profissional para a mensagem |
| `mensageria_mensagem:enviar_intencao` | pedir o envio (intenção com deduplicação) |

As ações citam as capabilities `agendamento.listar_janela`, `clientes.buscar_cliente`,
`estabelecimento.buscar_profissional` e `mensageria.enviar_intencao` — o endereço real é resolvido em
privado na instalação. **Risco: médio** (envia mensagem ao paciente; não lê prontuário; age sozinho a cada 15 min).

## Config editável por clínica (sem redeploy)

- `template` (`lembrete_rapido`): template da mensageria (precisa do HSM **aprovado** e vinculado).
- `canal` (`whatsapp`).
- `antecedencia_minutos` (`120`): quanto antes do início mandar.
- `hora_minima` (`8`): nunca mandar antes desta hora (fuso da clínica).
- `atraso_max_minutos` (`60`): até quanto depois do horário de envio ainda vale mandar.
- `tz_offset` (`-03:00`): fuso da clínica.
- `status_pular`: status que não recebem.
- `per_page` (`100`, máximo da API).

## Instalação (Central → Inteligência Artificial → Importar)

1. Confira o template `lembrete_rapido` na mensageria: HSM **APPROVED** e vinculado com as variáveis
   `cliente_nome`, `profissional_apelido`, `hora` (nessa ordem).
2. **Antes de ligar, desligue o lembrete rápido do orquestrador** (senão o paciente recebe dois):
   `NOTIF_LEMBRETE_RAPIDO_ENABLED=false` em escopo **global** (Configurações do Sistema → orquestrador) e
   suprima os lembretes rápidos já pendentes no orquestrador. ⚠️ Gravar só para a clínica não basta: o
   orquestrador lê a configuração global.
3. Importe este `manifest.json` e conceda ao service-account os 4 grants acima.
4. Ligue o agente.

> **Atenção:**
> - **Reagendamento para dentro das 2h** (ex.: remarcado para daqui a 90 min) recebe o lembrete na hora.
> - **Consulta antes da `hora_minima`** (ex.: 07:30) não recebe lembrete — o horário de envio cairia depois do início.
> - A mensageria pode **adiar** o envio (status `agendado`) se a clínica tiver horário permitido configurado;
>   o adiamento pode passar do início da consulta. Hoje essa política não tem tela (mensageria#201).
> - O agente usa a **janela do cron** como "agora": uma rodada perdida é recuperada na seguinte, dentro do
>   `atraso_max_minutos`.
