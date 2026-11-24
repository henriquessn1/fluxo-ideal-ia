# tcle-concluido-aviso — cartão na tela quando o TCLE fica completo

Time de **1 agente `script`** (sem IA, sem custo de token). Quando o **TCLE** de uma venda fica completo (todas as
assinaturas), mostra um **cartão** no canto inferior direito da tela de quem tem o **papel escolhido** (padrão:
`medico`), com o botão para **abrir o TCLE na venda** e baixar o documento.

É um time de **snippet**: uma peça visual que o agente põe na tela da Central (selo, faixa, botão ou cartão). Veja a
capability "avisos e botões na tela" na skill [`designer-agentes`](../../../skills/designer-agentes/SKILL.md).

## O que faz

| Gatilho | Comportamento |
|---|---|
| evento `vendas.tcle_concluido` | lê a venda do evento → lê o número da venda (opcional) → mostra o cartão ao papel escolhido |

```text
┌─────────────────────────────────────────────┐
│ 📄 TCLE assinado · venda V-2026-0042        │
│ O termo de consentimento foi assinado por   │
│ todos. Abra a venda para ver e baixar o     │
│ documento.                                  │
│                    [ Abrir o TCLE da venda ]│
└─────────────────────────────────────────────┘
```

- **Onde aparece:** cartão flutuante no **canto inferior direito**, em qualquer tela da Central.
- **Até fechar e persistente:** o cartão fica até a pessoa fechar. Quem não estava na Central vê ao entrar.
- **Só quem pode ver a venda:** a pessoa do papel precisa ter acesso de leitura às vendas. Sem ele, o cartão não
  chega.
- **Sem cartão repetido:** o mesmo TCLE não gera dois cartões (a referência do cartão é a venda e o papel, nunca
  nome ou CPF).
- **Sem dado pessoal:** o cartão não traz o nome do paciente, só o número da venda. Sem acesso ao número, sai sem ele.
- **Falha visível:** se o cartão não puder ser mostrado, a execução fica com `acao_bloqueada` e o log diz em que
  etapa.

O resumo de cada execução (Central → Inteligência Artificial → execuções) mostra `avisado` e `com_numero` (+
`pulado`, `acao_bloqueada`, `etapa` e `http` quando for o caso). Sem id e sem dado pessoal.

## Capabilities que pede (superfície de consentimento)

| Papel (service-account) | Grants | Para quê |
|---|---|---|
| `botfn-tcle-aviso` | `notificacao:emitir_ui`, `notificacao:emitir_snippet` | pôr o cartão na tela |
| | `venda:read` | ler o número da venda que vai no título |

As ações citam as capabilities `notificacao.emitir_snippet` e `vendas.buscar_venda`. O endereço real é resolvido em
privado na instalação. O manifesto **declara** o cartão que o agente pode mostrar (componente, canto da tela e
permissão de quem vê); a plataforma recusa qualquer peça fora do declarado.

**Risco: baixo.** Não lê dado de paciente, não envia nada para fora, não muda dado. Age sozinho a cada TCLE concluído.

## Valores da clínica (na instalação)

| Valor | Padrão | O que faz |
|---|---|---|
| `papel_alvo` — Quem vê o aviso | `medico` | o papel da equipe que recebe o cartão (um papel só) |

## Instalação (Central → Inteligência Artificial → Importar)

1. **Antes:** a clínica precisa estar com a opção **"Avisos dos agentes na tela"** (`snippets_enabled`) **ligada**
   nas opções do sistema da Central. Com a opção desligada, o time importa, mas nenhum cartão aparece.
2. Importe este `manifest.json` (cole o link na tela de importar) e escolha o papel que vê o aviso.
3. Conceda ao service-account `botfn-tcle-aviso` os grants acima.
4. **O time entra desligado.** Todo time que põe peças na tela entra desligado na importação: ligue o agente
   `tcle_cartao` na Central depois dos grants e da opção da clínica.
5. Confira a primeira execução em "execuções": `avisado: true`.
