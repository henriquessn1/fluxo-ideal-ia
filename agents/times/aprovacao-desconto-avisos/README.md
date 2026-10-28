# aprovacao-desconto-avisos — aprovação de desconto pelo aviso

Time de **5 agentes `script`** que cuida do ciclo de um desconto que passou do teto da clínica: avisa
quem aprova, abre a tarefa na fila de aprovação, decide pelo aviso **em nome de quem clicou**, avisa a
equipe da decisão e fecha a tarefa.

> "A venda **1234** tem um desconto aguardando a sua aprovação. Paciente: Maria · Total: R$ 1.200,00 ·
> Desconto: 25% (R$ 300,00)" — **[Aprovar] [Rejeitar] [Abrir aprovações]**

## O que faz

| Agente | Quando roda | O que faz |
|---|---|---|
| `desconto_requer_aprovacao_aviso` | uma venda pede desconto acima do teto | mostra um **aviso na tela** (modal persistente) para o papel `alvo_role`, com paciente, total, desconto, quem pediu e até 5 itens; botões **Aprovar**, **Rejeitar** e **Abrir aprovações** |
| `desconto_classificador` | idem | cria a **tarefa de aprovação** ligada à venda, com prioridade pela faixa do desconto (baixa / média a partir de `faixa_media_pct` / alta a partir de `faixa_alta_pct`) |
| `desconto_executor` | alguém clica em Aprovar ou Rejeitar no aviso | aprova ou recusa o desconto **em nome da pessoa que clicou** — a decisão fica registrada no nome dela, e só vale se ela mesma puder aprovar desconto. Sem saber quem clicou, **não decide** |
| `desconto_remediador` | o desconto é recusado | faz o que a clínica configurou em `acao_rejeicao`: `manter` (a venda segue, com o desconto de volta ao teto) ou `cancelar` a venda |
| `desconto_fechador` | o desconto é decidido (aprovado ou recusado, pelo aviso **ou** pela tela de aprovações), ou a venda é cancelada | fecha o aviso **para toda a equipe** (só o daquela venda), avisa o mesmo papel **quem decidiu** ("Desconto de 25% da venda 1234 aprovado por Ana") e **conclui a tarefa** de aprovação daquela venda que o time abriu. Se a venda for **cancelada com o desconto ainda aguardando aprovação**, fecha o aviso e conclui a tarefa, sem aviso de decisão |

- Cada passo do fechador degrada sozinho: se fechar o aviso falhar, ainda avisa e conclui a tarefa.
- O fechador só conclui as tarefas **abertas que o próprio time criou** para a venda; outras tarefas da
  venda ficam como estão.
- Na venda cancelada, o fechador confere na venda se o desconto ainda aguardava aprovação; se já tinha
  sido decidido (ou se não der para conferir), não mexe em nada.
- Sem permissão para ler o paciente ou o nome de quem pediu, o aviso sai sem esse dado (não falha).

## Config editável por clínica (knobs)

| Knob | Padrão | Para quê |
|---|---|---|
| `alvo_role` | `administrador` | papel que recebe o aviso, aprova e é avisado de quem decidiu. **Precisa poder aprovar desconto** |
| `faixa_media_pct` | `10` | a partir deste % a tarefa nasce com prioridade média |
| `faixa_alta_pct` | `20` | a partir deste % a tarefa nasce com prioridade alta |
| `acao_rejeicao` | `manter` | o que fazer quando o desconto é recusado: `manter` ou `cancelar` a venda |

## Capabilities que pede (superfície de consentimento)

Um service-account (`botfn-desconto-aprovacao`) com:

| Grant | Para quê |
|---|---|
| `notificacao:emitir_ui` | mostrar o aviso com botões e fechá-lo para todos |
| `notificacao:enviar` | avisar o papel de quem decidiu |
| `tarefas:criar` | abrir a tarefa de aprovação |
| `tarefas:listar` | achar a tarefa de aprovação da venda |
| `tarefas:mover` | concluir a tarefa |
| `desconto:aprovar` | aprovar ou recusar o desconto (em nome de quem clicou) |
| `venda:read` | itens e valores da venda para o aviso; conferir o desconto quando a venda é cancelada |
| `venda:cancel` | cancelar a venda, **só** com `acao_rejeicao=cancelar` |
| `cliente:read:full` | nome do paciente no aviso |
| `usuario:read_nome` | nome de quem pediu e de quem decidiu |

As ações citam as capabilities `notificacao.emitir_ui`, `notificacao.dismiss_diretiva`,
`notificacao.notificar_grupo`, `vendas.buscar_venda`, `vendas.aprovar_desconto`,
`vendas.rejeitar_desconto`, `vendas.cancelar`, `clientes.buscar_cliente`,
`estabelecimento.buscar_usuario`, `tarefas.criar`, `tarefas.listar_por_vinculo` e
`tarefas.mudar_estado` — o endereço real é resolvido em privado na instalação.

## Risco: **alto**

- 💸 **Decide desconto em nome de uma pessoa**: o clique no aviso vira a aprovação (ou a recusa) daquela
  pessoa. A trava é tripla: só quem pode aprovar desconto consegue decidir, o time nunca decide sem
  saber quem clicou, e cada clique gera um recibo que vale uma vez só, para aquela venda e aquele %.
- 🛑 **Pode cancelar venda sozinho** quando `acao_rejeicao=cancelar`. No padrão (`manter`) não cancela.
- 👁️ **Lê o nome do paciente** e os itens da venda para montar o aviso (fica só no aviso da equipe;
  o resumo da execução não leva dado pessoal).
- ⚡ Age sozinho, nos eventos de desconto pedido, de clique no aviso, de desconto decidido e de venda
  cancelada.

## Requisitos de versão

| Módulo | Mínimo | Por quê |
|---|---|---|
| vendas | **0.1.96** | aceitar a decisão **em nome de quem clicou** só com o recibo do clique |
| notification-center | **0.6.632** | informar quem clicou no aviso e gerar o recibo do clique |
| agentes | **0.3.102** | repassar o recibo do clique |
| estabelecimento | **0.8.794** | nome de quem pediu e de quem decidiu |

> ⚠️ Com versões mais antigas, a decisão pelo aviso é recusada (sem o recibo, o vendas não aceita a
> decisão em nome de ninguém). A tela de aprovações continua funcionando. Confira as versões antes de ligar.

## Versões

| Versão | O que mudou |
|---|---|
| **3.6** | Cada clique no aviso gera um recibo de uso único, e a decisão só vale com ele: para aquela venda, aquele % e um aviso do próprio time. Os botões do aviso levam o % do desconto |
| 3.5 | Venda cancelada com o desconto ainda aguardando aprovação: o aviso fecha e a tarefa de aprovação é concluída (antes ficava aberta). Textos do aviso e da tarefa com acento. Scripts mais enxutos |
| 3.4 | Decide pelo aviso em nome de quem clicou, avisa a equipe de quem decidiu e conclui a tarefa |

## Instalação (Central → Configuração → Agentes → Importar)

1. Escolha **Aprovação de desconto** no catálogo oficial (ou cole o link deste `manifest.json`) e confira
   o cartão de risco.
2. Ajuste os knobs: o `alvo_role` precisa ser um papel que **pode aprovar desconto**.
3. Conceda ao service-account os grants acima.
4. Ligue os agentes.

> Reimportar uma versão nova do time **atualiza o mesmo time** (mesma chave `aprovacao-desconto-avisos`)
> e mantém as variáveis que a clínica já ajustou nos agentes.
