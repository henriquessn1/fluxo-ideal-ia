# Time: confirmacao-presenca

**Confirma a presença do paciente por WhatsApp — e cuida da resposta sozinho.**

Quando um agendamento se aproxima, este time arma a confirmação, e quando o paciente responde (pelo
botão do WhatsApp), triage: confirmou → confirma o agendamento e resolve o ticket; pediu ajuda →
encaminha à recepção; respondeu algo fora do padrão → escala para a IA interpretar.

## Agentes
- **armar_confirmacao** (script): prepara a confirmação e inscreve o bot como observador da conversa.
- **triagem_confirmacao** (script): lê a resposta do paciente e decide o desfecho (confirmar /
  escalar / encaminhar).
- **confirmador_presenca** (IA): entra quando a resposta é livre (não-estruturada) e precisa de
  interpretação.

## O que este time pede (permissões)
- `agendamento:confirm` — confirmar o agendamento quando o paciente confirma.
- `conversa:operar`, `conversa:observar_terceiros` — ler/comentar a conversa e observar respostas.
- `ticket:assign`, `ticket:resolve`, `ticket:transfer` — atribuir/resolver/transferir o atendimento.
- `mensageria:enviar_intencao` — disparar a mensagem de confirmação.

## Risco: **médio**
- 👁️ **Toca dados de atendimento/conversa do paciente** (operar conversa, confirmar agendamento).
- ✅ **Não** envia dados para fora do sistema (só usa os canais internos/oficiais). **Não** age em
  modo automático silencioso — segue o roteiro de confirmação.

## Capabilities usadas
`agendamento.confirmar_agendamento`, `interacoes.ler_conversa`, `interacoes.resolver_conversa`,
`interacoes.comentar`, `interacoes.inscrever_observador`, `interacoes.desinscrever_observador`,
`interacoes.atribuir_ticket`, `interacoes.resolver_ticket`, `interacoes.transferir_fila`.
