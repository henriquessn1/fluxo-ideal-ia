# Exemplos de agentes (para quem DESENHA)

Esta pasta é **didática**. Os times aqui **não** são produtos prontos para uma clínica instalar e
usar no dia a dia — são **exemplos de referência** que mostram **o que dá para fazer** e **como se
faz**, para quem está **desenhando** um agente novo.

> **Procurando algo para instalar e usar?** Vá para os **[times produtivos](../times/)** — esses sim
> resolvem problemas comuns e são pensados para a clínica importar. Aqui é o "showroom para
> construtores", não a "prateleira para clientes".

## Como usar um exemplo
1. **Leia o README do exemplo** — ele explica *o que foi feito*, *como foi feito* e *o que dá para
   mudar*.
2. **Leia o `manifest.json`** como um molde: veja o gatilho, a lista de capabilities (por nome), o
   roteiro do script e os knobs.
3. **Clone e adapte** para o seu caso — troque o gatilho, o alvo, o conteúdo, os botões. Um exemplo é
   ponto de partida, não algo para instalar como está.

## Antes de desenhar do zero: leia a skill de design
O "como se pensa" um agente (persona, capabilities, gatilhos, LLM vs. script, reuso antes de criar)
está na **skill [`designer-agentes`](../../skills/designer-agentes/SKILL.md)** — é o material
conceitual que sustenta estes exemplos. Comece por ela; depois use os exemplos aqui como concretização
dos conceitos.

## Exemplos disponíveis

| Exemplo | Mostra o padrão de | O que ensina |
|---------|--------------------|--------------|
| [avisos-diretivas-ui](./avisos-diretivas-ui/) | **Diretiva de UI** (aviso/ação na tela) | Um agente empurrar um toast/modal com botões para a tela de um papel; botão que navega (link) vs. botão que chama o agente de volta (round-trip). |

> Se você criar um exemplo genérico e útil que vira **produto**, promova-o para
> [`../times/`](../times/) (vira um time produtivo, com o charter de instalação).
