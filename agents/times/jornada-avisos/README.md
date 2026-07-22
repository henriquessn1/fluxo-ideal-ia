# Time: jornada-avisos

**Avisa a equipe quando uma etapa da jornada está atrasada.**

Roda de tempos em tempos (agendado), procura as jornadas com pendências de SLA (marcos parados/
vencendo) e **avisa a equipe** — para ninguém deixar um paciente travado no meio do caminho.

## Agentes
- **jornada_avisos** (script): consulta as pendências de SLA da jornada e dispara o aviso à equipe.

## O que este time pede (permissões)
- `jornada:read` — ler o estado/pendências da jornada.
- `notificacao:enviar`, `notificacao:broadcast` — avisar a equipe (individual e em grupo).

## Risco: **médio**
- 👁️ **Lê o estado da jornada** do paciente (para saber o que atrasou).
- 🔔 Notifica **a equipe** (interno) — **não** manda nada para fora do sistema, **não** notifica o
  paciente. Roda no horário agendado.

## Capabilities usadas
`atendimento.listar_pendencias_sla`, `atendimento.buscar_fase`, `notificacao.notificar`,
`notificacao.notificar_grupo`.
