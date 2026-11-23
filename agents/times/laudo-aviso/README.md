# laudo-aviso — avisa o paciente que há um resultado novo no portal

Time de **1 agente `script`** que, quando o resultado de um exame é **liberado ao paciente**, manda a ele o aviso:

> "Há um resultado novo no portal."

O aviso **nunca cita o exame** (nem o nome, nem o tipo): o paciente abre o portal para ver. Exame + paciente é
dado de saúde (LGPD), e o agente nem recebe o nome do exame — só os identificadores.

Substitui o aviso fixo de resultado que existia dentro do serviço de mensagens (aposentado na release 2026.11.7):
o comportamento agora é deste time, que a clínica liga e desliga na Central.

## O que faz

| Gatilho | Comportamento |
|---|---|
| Resultado de exame liberado ao paciente (evento do serviço de exames) | pede ao serviço de mensagens **1 aviso por exame** para o paciente, com o modelo `resultado_exame`, sem variáveis |

- **Toda liberação conta:** a feita pela médica na tela **e** a feita pelo time
  [`laudo-liberacao-automatica`](../laudo-liberacao-automatica/) (se instalado).
- **Canais:** WhatsApp, pelo modelo aprovado pelo WhatsApp para este aviso, quando houver; senão, **e-mail**. Quem
  escolhe o canal é o serviço de mensagens (entrega com alternativa). Sem o modelo de WhatsApp aprovado, o aviso sai
  só por e-mail.
- **Sem duplicar:** cada aviso leva a chave `resultado_exame:<paciente>:<exame>` (só identificadores, sem dado
  pessoal). O mesmo exame liberado de novo, ou o mesmo evento entregue duas vezes, volta `deduplicado`: o paciente
  recebe **um** aviso por exame.
- **Horário e limite da clínica:** o serviço de mensagens pode **adiar** o aviso (status `agendado`) para o horário
  permitido e respeita o limite de envios da clínica.
- **Falha aparece:** envio que volta com erro, ou com status fora de `aceito`/`deduplicado`/`agendado`, conta como
  **falha**: log de aviso e `acao_bloqueada` no resumo da execução — nunca vira "enviado".

O resumo de cada execução (Central → Inteligência Artificial → execuções) mostra só o status do envio
(`enviado`, `deduplicado`, `agendado`) ou a falha — sem dado do paciente e sem o exame.

## O que este time pede (permissões)

| Permissão | Para quê |
|---|---|
| `mensageria_mensagem:enviar_intencao` | pedir o envio do aviso (com deduplicação, horário e limite da clínica) |

Só isso. O agente **não lê** o cadastro do paciente nem o exame: o serviço de mensagens encontra o contato do
paciente sozinho. A ação cita a capability `mensageria.enviar_intencao` — o endereço real é resolvido em privado na
instalação.

## Risco: **médio**

- 📤 **Envia mensagem ao paciente** (WhatsApp ou e-mail), sozinho, a cada resultado liberado.
- ✅ **Não** lê prontuário, cadastro nem resultado. O texto **não** tem dado de saúde.
- ⚠️ Se a clínica liberar resultados por engano, o paciente recebe o aviso; o aviso só diz que há um resultado no
  portal.

## Config editável por clínica (sem redeploy)

- `template_slug` (`resultado_exame`): modelo da mensagem no serviço de mensagens.

## Como ligar

O time **vem desligado**. Para usar:

1. Confira o modelo `resultado_exame` no serviço de mensagens. Para sair por WhatsApp, o modelo de WhatsApp deste
   aviso precisa estar **aprovado** e vinculado (sem variáveis). Sem ele, o aviso vai só por e-mail.
2. Importe este `manifest.json` (Central → Inteligência Artificial → Importar) e conceda ao papel do agente a
   permissão acima.
3. Ligue o agente `laudo_aviso` na lista de agentes (Central → Inteligência Artificial → agentes → ligar). É ali que
   ele liga e desliga, a qualquer momento.

> **Reimportar não mexe no ligado:** importar de novo este time (por exemplo, numa versão nova) atualiza o
> comportamento, mas **não** liga nem desliga o agente: vale o que a clínica deixou na lista de agentes. O
> "desligado" do manifesto só vale quando o agente é criado (primeira importação ou depois de apagado).

> **Publicação:** este time entra no catálogo depois que a release 2026.11.7 estiver em produção (ele depende do
> evento e do modelo de mensagem que sobem nela).
