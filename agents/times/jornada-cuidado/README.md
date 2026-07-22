# Time: jornada-cuidado

**Mantém a Jornada de Cuidado do paciente andando — sozinha.**

A Jornada é o caso longo do paciente (uma cirurgia/procedimento com pré e pós). Este time cuida da
mecânica: **vincula** as tarefas certas à jornada e **fecha/avança** as fases conforme os marcos são
cumpridos (a fase é sempre derivada dos marcos, que são tarefas).

## Agentes
- **jornada_binder** (script): liga as tarefas ao contexto da jornada e trata impedimentos.
- **jornada_closer** (script): move o estado das tarefas e recalcula a fase da jornada quando um marco
  fecha.

## O que este time pede (permissões)
- `jornada:read`, `jornada:write` — ler e avançar a jornada do paciente.
- `tarefas:listar`, `tarefas:editar`, `tarefas:mover` — operar as tarefas que são os marcos.

## Risco: **médio**
- 👁️ **Toca a jornada do paciente** (`jornada:write`) e as tarefas do caso.
- ✅ **Não** envia dados para fora. Age dentro do fluxo da jornada (sem saída externa).

## Capabilities usadas
`atendimento.buscar_jornada_ativa`, `atendimento.recompute_fase`, `tarefas.listar_tarefas`,
`tarefas.mudar_estado`, `tarefas.set_contexto`, `tarefas.criar_impedimento`.
