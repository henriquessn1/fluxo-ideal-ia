# Exemplo: avisos-diretivas-ui

**Padrão que este exemplo mostra:** um agente empurrar um **aviso acionável para a tela** de um
usuário ou papel — um **toast** simples ou um **modal** com título, texto e **botões** — e os botões
ou **abrem uma entidade** (link) ou **chamam o agente de volta** (round-trip).

> Isto é um **exemplo didático**, não um time para instalar e usar como está. Ele existe para você
> ver *como* o padrão de "diretiva de UI" funciona e adaptá-lo ao seu caso. Para o material
> conceitual, veja a skill [`designer-agentes`](../../../skills/designer-agentes/SKILL.md).

## O que foi feito
Um agente-**script** que, quando um **orçamento é aprovado**, mostra na tela da equipe um modal
*"Orçamento aprovado"* com um botão **"Ver o orçamento"**. É o "hello world" das diretivas de UI:
o mínimo para provar o caminho **evento → agente → aviso na tela**.

## Como foi feito (anatomia do manifesto)
- **Gatilho:** `vendas.orcamento_aprovado` — o evento que acorda o agente.
- **Capability:** `notificacao.emitir_ui` — a ação curada que empurra a diretiva para a tela. (No
  manifesto ela é citada **por nome**; o endereço interno é resolvido pela plataforma na instalação.)
- **Roteiro (script):** lê o id/número do orçamento do evento e chama `emitir_ui` com o **conteúdo**
  da diretiva:
  - `kind`: `toast` (passa) ou `modal` (fica até dispensar);
  - `titulo` + `corpo` (o corpo aceita **markdown**);
  - `botoes`: cada um com `label`, `estilo` e uma `acao`:
    - `{ tipo: 'link', href }` → **navega** para a entidade;
    - `{ tipo: 'evento', event_type, payload }` → **chama o agente de volta** (round-trip);
  - `alvo`: `{ role }` e/ou `{ user_id }` — quem vê;
  - `persistencia`: `persistente` (sobrevive a recarregar até dispensar) ou `efemero`.
- **Knob `alvo_role`:** o papel que recebe o aviso é **escolhido na instalação** (`{{knob.alvo_role}}`),
  para a clínica apontar para a role certa sem editar o script.

## O que dá para mudar (é aqui que você aprende)
- **Outro gatilho:** troque `vendas.orcamento_aprovado` por qualquer evento (venda fechada, prazo
  vencido, pagamento recebido…).
- **Outro alvo:** mude o knob `alvo_role`, ou mire um `user_id` específico em vez de um papel.
- **Toast vs modal:** avisos triviais podem ser `toast` efêmero; decisões importantes, `modal`
  persistente.
- **Botão de link → botão de evento (round-trip):** troque `{tipo:'link'}` por
  `{tipo:'evento', event_type:'...'}` e crie um **segundo agente** que reage a esse clique — o clique
  vira um gatilho (`notificacao.diretiva_respondida`). Ex.: *"Orçamento aprovado → [Enviar link ao
  cliente]"*, onde o clique aciona o agente que manda o link. Isso é um **time** (um avisa, outro age
  no clique, a pessoa no meio é o consentimento).
- **Rota do botão (`base_path`):** ajuste para a tela certa da sua Central.

## Regras herdadas (valem para qualquer diretiva de UI)
- O **alvo por papel** só chega a quem está logado com aquele papel.
- O agente age com o **próprio acesso** (nunca o do usuário); o clique fica **registrado** (quem
  autorizou) — é consentimento humano, não delegação de poder.
- Curar `notificacao.emitir_ui` **não concede acesso** — a permissão é aplicada pela plataforma na
  hora de agir (o agente precisa do grant `notificacao:emitir_ui`, que a instalação provisiona).
