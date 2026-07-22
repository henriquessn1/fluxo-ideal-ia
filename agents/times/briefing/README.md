# Time: briefing

**O cartão de contexto do paciente, pronto antes do atendimento.**

Um agente de IA que, quando a equipe pede, lê o contexto de um atendimento e **grava um briefing** —
o resuminho que o médico/atendente lê **antes** de receber o paciente (aniversário, se é retorno,
última visita, acompanhante, pendências). Foco relacional/logístico, com guarda-rail de LGPD: o
briefing geral é **não-clínico** por construção.

## Agentes
- **gerador_briefing** (IA): lê o contexto (atendimento, cliente, histórico de interações) e grava o
  briefing no atendimento. Dispara quando um briefing é solicitado.

## O que este time pede (permissões)
- `atendimento:read`, `atendimento:update` — ler o atendimento e gravar o briefing.
- `cliente:read:full` — dados do paciente (como chamar, aniversário, vínculos).
- `interacao:list` — histórico de conversas (última visita, faltas).

## Risco: **médio**
- 👁️ **Lê dados de paciente** (`cliente:read:full`, `atendimento:*`) — é o insumo do briefing.
- ✅ **Não** envia nada para fora. **Não** age sozinho (só quando solicitado).

## Capabilities usadas
Nenhuma ação direta: este agente é de IA e alcança o sistema pelas ferramentas autorizadas (MCP),
não por ações de endpoint.
