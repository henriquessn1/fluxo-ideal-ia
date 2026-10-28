# pedido-carteirinha — a IA lê a carteirinha que o paciente mandou

Quando a clínica **pede a carteirinha** ao paciente pelo WhatsApp (botão "Pedir carteirinha" da fila de
autorizações de convênio), o paciente costuma responder com uma **foto** da carteirinha ou com o **número e a
validade por escrito**. Este time lê essa resposta e deixa uma **solicitação de convênio** pronta para a
recepção **aprovar** — a mesma tela das solicitações que chegam pelo portal e pelo link do pedido.

**Nunca grava direto no cadastro do paciente.** Se não entender, não grava nada e passa a conversa para a
recepção, dizendo o motivo.

## Agentes

| Agente | Tipo | Quando age | O que faz |
|---|---|---|---|
| `armar_pedido_carteirinha` | script | o modelo `pedido_carteirinha_convenio` sai pelo WhatsApp | passa a acompanhar a conversa do paciente (por `ttl_seg`, padrão 7 dias), guardando o item da venda do pedido |
| `ler_carteirinha` | script | o paciente manda mensagem nessa conversa | lê as mensagens dele desde a última da clínica e cria a solicitação (detalhe abaixo) |
| `carteirinha-convenio-texto` | IA | chamado pela leitura, quando o paciente **escreveu** em vez de mandar foto | extrai número, validade e plano do texto, com a mesma saída da leitura de foto |

A **foto** é lida pelo agente de visão `carteirinha-convenio` (o mesmo do botão "Extrair carteirinha" no
Conversas). Uma clínica pode calibrar a leitura importando um agente com o mesmo nome: o da clínica vale
antes do global.

### O que a leitura decide

1. Acha o pedido (item da venda) e o **convênio pedido**; confere que a conversa é do paciente do pedido.
2. Se já há uma solicitação **pendente** desse convênio para o paciente (ex.: veio pelo link), não duplica:
   comenta na conversa e para de acompanhar.
3. Junta as mensagens do paciente desde a última da clínica (frente e verso chegam juntos: o gatilho espera
   `coalesce_seg`). Com foto, lê a foto; só com texto, lê o texto.
4. Leu número e validade (e a carteirinha não está vencida) → cria a solicitação com origem **"lida pela
   IA"**: `alterar` se o paciente já tem esse convênio ativo, senão `adicionar`. Na **observação**: foto ou
   texto, a confiança, os campos para conferir e um aviso se a operadora lida não parece ser a do pedido.
   Comenta na conversa e para de acompanhar.
5. Não entendeu (não é carteirinha, sem número, **sem validade**, vencida, leitura falhou ou demorou) →
   transfere a conversa para a fila `fila_recepcao` com o motivo (sem fila aberta: comentário interno).
   Continua acompanhando até o fim do prazo: uma foto melhor tenta de novo.

## Capabilities que pede (superfície de consentimento)

| Grant | Para quê |
|---|---|
| `conversa:operar` | ler as mensagens da conversa do pedido e comentar |
| `conversa:observar_terceiros` | acompanhar (e deixar de acompanhar) a conversa |
| `ticket:transfer` | passar a conversa para a fila da recepção |
| `carteirinha:extrair` | a leitura da carteirinha (foto ou texto) |
| `autorizacao_convenio:fila` | achar o convênio e o paciente do item pedido |
| `convenio:list` | ver se o paciente já tem esse convênio (alterar × adicionar) |
| `convenio_solicitacao:list` | não duplicar uma solicitação pendente |
| `convenio_solicitacao:create` | criar a solicitação para a recepção aprovar |

As ações citam as capabilities `vendas.buscar_autorizacao_item`, `clientes.listar_solicitacoes_cliente`,
`clientes.listar_convenios_cliente`, `clientes.criar_solicitacao_convenio`, `interacoes.ler_conversa`,
`interacoes.extrair_carteirinha`, `interacoes.resultado_carteirinha`, `interacoes.comentar`,
`interacoes.transferir_fila`, `interacoes.inscrever_observador` e `interacoes.desinscrever_observador`.

**Risco: médio.** 👁️ Lê a conversa do paciente (só a do pedido) e manda a foto/texto para a IA ler.
✅ Não grava no cadastro (só solicitação, a recepção aprova); não manda mensagem ao paciente; não põe número
da carteirinha nem dado do paciente em log ou nota.

## Config editável por clínica (sem redeploy)

- `template_slug` (`pedido_carteirinha_convenio`): o modelo de mensagem do pedido.
- `fila_recepcao` (`recepcao`): fila para onde vai o que a IA não entendeu.
- `ttl_seg` (`604800` = 7 dias): por quanto tempo acompanhar a conversa depois do pedido.
- `coalesce_seg` (`20`): espera para juntar mensagens seguidas (frente e verso).
- `espera_seg` (`12`): quanto esperar a leitura (o script desiste em 15 s).
- `llm_modelo` (`claude-haiku-4-5`): modelo da leitura por texto.

## Instalação (Central → Inteligência Artificial → Importar)

Requer: interacoes ≥ 0.6.910, clientes ≥ 0.7.599, agentes ≥ 0.3.103 e o pedido de carteirinha (H4) configurado.

1. Importe este `manifest.json` e conceda ao service-account os grants acima.
2. Confira a chave da IA (cofre da Central) — sem ela a leitura falha e tudo vai para a recepção.
3. Ligue os agentes.

> **Atenção:**
> - O agente de texto precisa se chamar `carteirinha-convenio-texto` (é por esse nome que a leitura o chama).
>   Renomear na Central faz a leitura por texto falhar.
> - Carteirinha **sem validade impressa** vai para a recepção (o cadastro exige a validade).
