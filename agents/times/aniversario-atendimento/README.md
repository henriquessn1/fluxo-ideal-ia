# aniversario-atendimento — selo e mensagem de parabéns ao abrir o atendimento

Time de **1 agente `script`** (sem IA, sem custo de token). Quando alguém da equipe **abre um atendimento** (a tela do
atendimento ou qualquer aba dela) e **hoje é o aniversário do paciente**, mostra **a quem abriu**:

- um **selo** "Aniversário hoje" no cabeçalho, ao lado do nome;
- um **cartão** no topo da lateral com a **mensagem de parabéns pronta** (com o primeiro nome do paciente).

É um time de **snippet** com **gatilho de navegação**: ele acorda quando a tela é aberta e põe peças nela. Veja a
capability "avisos e botões na tela" na skill [`designer-agentes`](../../../skills/designer-agentes/SKILL.md).

## O que faz

| Gatilho | Comportamento |
|---|---|
| navegação em `/atendimento/:id` e `/atendimento/:id/:tab` | lê o atendimento (para saber o paciente) → lê a data de nascimento do paciente → se for hoje (fuso da clínica), mostra o selo e o cartão a quem abriu |

```text
 Maria da Silva  [🎂 Aniversário hoje]            ┌──────────────────────────────────────┐
                                                  │ 🎁 Mensagem de aniversário            │
                                                  │ Hoje é o aniversário de **Maria**.    │
                                                  │ Mensagem pronta para mandar:          │
                                                  │ > Feliz aniversário, Maria! Toda a    │
                                                  │ > equipe deseja um dia muito especial │
                                                  │ > para você.                          │
                                                  └──────────────────────────────────────┘
```

- **Só para quem abriu** e **só enquanto está no atendimento:** as peças ficam nas abas do mesmo atendimento e somem
  ao sair dele. Não são guardadas (abrir de novo mostra de novo).
- **Copiar a mensagem:** por ora o cartão traz **só o texto** da mensagem (selecione e copie). Os **botões de copiar**
  chegam numa versão futura da Central; o time vai ganhar o botão quando ela sair.
- **29/02:** em ano que não é bissexto, o aniversário é comemorado em 28/02.
- **Sem data de nascimento** no cadastro, ou não sendo o dia: sai limpo, sem peça.
- **Falha visível:** se não conseguir ler o atendimento ou o paciente, ou mostrar as peças, a execução fica com
  `acao_bloqueada` e a `etapa`.

O resumo de cada execução (Central → Inteligência Artificial → execuções) mostra `aniversario`, `selo` e `cartao` (+
`pulado`, `acao_bloqueada`, `etapa` e `http` quando for o caso). Sem id e sem dado pessoal.

## Quem vê

As peças só chegam a quem tem **leitura do atendimento** (`atendimento:read`) **e do cadastro completo do paciente**
(`cliente:read:full`). O agente lê esses dados com o papel dele, então a peça exige as mesmas leituras de quem a vê:
ninguém vê na tela um dado que não poderia abrir. Quem não tem as duas não vê nada (e não há erro na tela).

## Capabilities que pede (superfície de consentimento)

| Papel (service-account) | Grants | Para quê |
|---|---|---|
| `botfn-aniversario` | `notificacao:emitir_ui`, `notificacao:emitir_snippet` | pôr o selo e o cartão na tela |
| | `atendimento:read` | ler o atendimento aberto (para saber o paciente) |
| | `cliente:read:full` | ler a **data de nascimento** e o nome do paciente |

> ⚠️ **`cliente:read:full` é leitura de dado sensível do paciente.** Só conceda com o **ok de quem administra a
> clínica**. Sem esse grant o time não funciona (não há como saber o aniversário).

As ações citam as capabilities `atendimento.buscar_atendimento`, `clientes.buscar_cliente` e
`notificacao.emitir_snippet`. O endereço real é resolvido em privado na instalação. O manifesto **declara** as duas
peças (componente, tela, espaço e permissões de quem vê); a plataforma recusa qualquer peça fora do declarado.

**Risco: médio.** Lê dado de paciente (data de nascimento e nome) e o mostra na tela da equipe que já pode ler o
cadastro. Não envia nada para fora, não muda dado. Age sozinho a cada abertura de atendimento.

## Valores da clínica (na instalação)

| Valor | Padrão | O que faz |
|---|---|---|
| `mensagem` — Mensagem de parabéns | `Feliz aniversário, {nome}! Toda a equipe deseja um dia muito especial para você.` | o texto pronto do cartão; `{nome}` vira o primeiro nome do paciente |

Outros ajustes (configuração do agente, sem redeploy): `tz_offset` (`-03:00`), o fuso usado para decidir "que dia é
hoje". O gatilho pode ser restrito a alguns papéis (ex.: só `recepcao`) na Central.

## Instalação (Central → Inteligência Artificial → Importar)

1. **Antes:** a clínica precisa estar com a opção **"Avisos dos agentes na tela"** (`snippets_enabled`) **ligada**
   nas opções do sistema da Central. Com a opção desligada, o time importa, mas nada aparece.
2. Importe este `manifest.json` (cole o link na tela de importar) e ajuste a mensagem, se quiser.
3. Conceda ao service-account `botfn-aniversario` os grants acima (o `cliente:read:full` com o ok de quem administra).
4. **O time entra desligado.** Todo time que põe peças na tela ou reage à abertura de uma tela entra desligado na
   importação: ligue o agente `aniversario_atendimento` na Central depois dos grants e da opção da clínica.
5. Abra o atendimento de um paciente que faz aniversário hoje e confira a execução: `aniversario: true`, `selo: true`,
   `cartao: true`.
