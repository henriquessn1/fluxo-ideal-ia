# Time: confirmacao-presenca

**Confirma a presença do paciente por WhatsApp — e cuida da resposta sozinho.**

Quando um agendamento se aproxima, este time arma a confirmação, e quando o paciente responde (pelo
botão do WhatsApp), triage: confirmou → confere que o agendamento é desse paciente, confirma e
resolve o ticket; pediu ajuda → encaminha à recepção; respondeu algo fora do padrão → escala para a
IA interpretar.

**Atendimento privado** (o paciente está numa conversa privada com um profissional): o time só
confirma pelo botão e deixa uma nota. Não manda para a fila, não troca o responsável e não encerra
o atendimento — o resto fica com o profissional.

## Agentes
- **armar_confirmacao** (script): prepara a confirmação e inscreve o bot como observador da conversa.
- **triagem_confirmacao** (script): lê a resposta do paciente e decide o desfecho (confirmar /
  escalar / encaminhar).
- **confirmador_presenca** (IA): entra quando a resposta é livre (não-estruturada) e precisa de
  interpretação.

## Config editável por clínica (knobs)
- **`fila_humana`** (padrão `atendente`): o **nome do papel** (role) que recebe as conversas que precisam de
  uma pessoa. A conversa aparece em "Minhas" de quem tem esse papel. Precisa ser um papel que existe na
  clínica. Com um nome que nenhum papel tem, a conversa fica parada em "Não atribuídas".

## O que este time pede (permissões)
- `agendamento:confirm` — confirmar o agendamento quando o paciente confirma.
- `agendamento:read` — conferir, antes de confirmar, que o agendamento é do paciente da conversa.
- `conversa:operar`, `conversa:observar_terceiros` — ler/comentar a conversa e observar respostas.
- `ticket:assign`, `ticket:resolve`, `ticket:transfer` — atribuir/resolver/transferir o atendimento.
- `mensageria:enviar_intencao` — disparar a mensagem de confirmação.

## Risco: **médio**
- 👁️ **Toca dados de atendimento/conversa do paciente** (operar conversa, confirmar agendamento).
- ✅ **Não** envia dados para fora do sistema (só usa os canais internos/oficiais). **Não** age em
  modo automático silencioso — segue o roteiro de confirmação.

## Capabilities usadas
`agendamento.confirmar_agendamento`, `agendamento.buscar_agendamento`, `interacoes.ler_conversa`, `interacoes.resolver_conversa`,
`interacoes.comentar`, `interacoes.inscrever_observador`, `interacoes.desinscrever_observador`,
`interacoes.atribuir_ticket`, `interacoes.resolver_ticket`, `interacoes.transferir_fila`.

## Versões
| Versão | O que mudou |
|---|---|
| **1.5** | A fila das conversas que precisam de uma pessoa (`fila_humana`) passa a vir como `atendente`, o papel da recepção. Antes vinha `recepcao`, que não é um papel, e essas conversas ficavam em "Não atribuídas". Quem já instalou: confira o valor na Central |
| 1.4 | Atendimento privado: só confirma pelo botão e deixa uma nota; confere que o agendamento é do paciente antes de confirmar |
