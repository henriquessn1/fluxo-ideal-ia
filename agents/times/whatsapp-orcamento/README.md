# whatsapp-orcamento — botão para a conversa com o paciente ao abrir o orçamento

Time de **1 agente `script`** (sem IA, sem custo de token). Quando alguém da equipe **abre um orçamento** (a tela do
orçamento ou qualquer aba dela), mostra **a quem abriu** um **botão** no canto inferior esquerdo, **"Conversa com o
paciente"**, que leva à conversa do paciente na **Central de Conversas** (onde a equipe fala com ele pelo WhatsApp).

É um time de **snippet** com **gatilho de navegação**: ele acorda quando a tela é aberta e põe uma peça nela. Veja a
capability "avisos e botões na tela" na skill [`designer-agentes`](../../../skills/designer-agentes/SKILL.md).

## O que faz

| Gatilho | Comportamento |
|---|---|
| navegação em `/orcamento/:id` e `/orcamento/:id/:tab` | lê o orçamento (para saber o paciente) → mostra o botão a quem abriu, com o link interno `/conversas/cliente/<paciente>` |

- **Só para quem abriu** e **só nesta tela:** o botão some ao trocar de tela. Não é guardado (abrir de novo mostra de
  novo).
- **Link interno:** o botão navega dentro da Central; não abre nada fora dela.
- **Sem dado pessoal na peça:** o botão não traz nome nem telefone; a referência leva só ids opacos.
- **Orçamento sem paciente:** sai limpo, sem botão.
- **Falha visível:** se não conseguir ler o orçamento ou mostrar o botão, a execução fica com `acao_bloqueada` e a
  `etapa`.

O resumo de cada execução (Central → Inteligência Artificial → execuções) mostra `botao` (+ `pulado`,
`acao_bloqueada`, `etapa` e `http` quando for o caso). Sem id e sem dado pessoal.

## Quem vê

O botão só chega a quem tem **leitura do orçamento** (`orcamento:read`): o agente lê o orçamento com o papel dele,
então o botão exige a mesma leitura de quem o vê. Para **usar** a conversa, a pessoa ainda precisa ter acesso à
Central de Conversas; sem ele, a tela de conversas mostra que falta permissão.

## Capabilities que pede (superfície de consentimento)

| Papel (service-account) | Grants | Para quê |
|---|---|---|
| `botfn-whatsapp-orcamento` | `notificacao:emitir_ui`, `notificacao:emitir_snippet` | pôr o botão na tela |
| | `orcamento:read` | ler o orçamento aberto (para saber o paciente) |

As ações citam as capabilities `vendas.buscar_orcamento` e `notificacao.emitir_snippet`. O endereço real é resolvido
em privado na instalação. O manifesto **declara** o botão (componente, tela, canto da tela e permissão de quem vê); a
plataforma recusa qualquer peça fora do declarado.

**Risco: baixo.** Não lê cadastro do paciente, não envia nada para fora, não muda dado. Age sozinho a cada abertura
de orçamento.

## Valores da clínica (na instalação)

Nenhum. O gatilho pode ser restrito a alguns papéis (ex.: só `recepcao` e `comercial`) na Central.

## Instalação (Central → Inteligência Artificial → Importar)

1. **Antes:** a clínica precisa estar com a opção **"Avisos dos agentes na tela"** (`snippets_enabled`) **ligada**
   nas opções do sistema da Central. Com a opção desligada, o time importa, mas nada aparece.
2. Importe este `manifest.json` (cole o link na tela de importar).
3. Conceda ao service-account `botfn-whatsapp-orcamento` os grants acima.
4. **O time entra desligado.** Todo time que põe peças na tela ou reage à abertura de uma tela entra desligado na
   importação: ligue o agente `whatsapp_orcamento` na Central depois dos grants e da opção da clínica.
5. Abra um orçamento e confira a execução: `botao: true`.
