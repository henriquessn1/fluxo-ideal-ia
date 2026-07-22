# Fluxo Ideal — Agents (times de agentes instaláveis)

Catálogo **público** de **times de agentes** oficiais do Fluxo Ideal, prontos para uma clínica
**instalar** na própria conta (Central → Inteligência Artificial → **Importar**, colando o link do
`manifest.json` de um time).

> **Diferença para `../skills/`:** uma _skill_ é conhecimento conceitual (uma IA **entende** o
> domínio). Um _agente_ é uma **automação instalável** — ele **age**. Por isso o manifesto de um
> agente carrega mais do que uma skill, e tem um charter próprio (abaixo).

## Charter desta pasta (o que tem e o que NÃO tem)

Um manifesto de agente é **configuração declarativa** — "comportamento de agente é dado, nunca
código de serviço". Ele **contém**, por necessidade:

- **Declaração de permissões (RBAC)** que o time precisa — é a **superfície de consentimento**: a
  clínica precisa ver o que está autorizando (como um app que pede "acesso à câmera"). Não é a
  matriz de permissões do sistema; é o **pedido** de um time.
- **Comportamento**: a instrução (prompt) de um agente de IA e/ou o roteiro determinístico de um
  agente-script. Isso é **dado editável**, não o código-fonte da plataforma.
- **Capabilities**: cada ação cita uma **capability nomeada** (ex.: `interacoes.comentar`), nunca a
  rota interna. O endereço real do endpoint é resolvido **em privado** pelo backend da clínica na
  hora de instalar.

E **NÃO contém** (por design):

- ❌ endpoints/rotas internas (as ações citam capability, não `service`+`path`);
- ❌ endereços de rede, IPs, portas, hostnames;
- ❌ segredos, tokens ou chaves internas;
- ❌ dados de paciente / conteúdo sensível.

## Segurança da instalação (por que é seguro instalar)

1. **Sem escalonamento de privilégio.** A instalação roda com **o seu acesso** (o do usuário que
   importa). Um manifesto que "pede" acesso a prontuário só recebe se você já puder conceder. Ninguém
   ganha poder novo importando.
2. **O porteiro checa em toda ação.** Em runtime, o RBAC do service-account do agente é a trava real
   — a declaração no manifesto é um _pedido_, não uma _chave_.
3. **Consentimento informado.** A tela de importar mostra um **cartão de risco** (lê dados de
   paciente? envia algo pra fora? age sozinho?) antes de aplicar.

## Duas pastas: produtivos vs. exemplos

- **[`times/`](./times/) — times PRODUTIVOS (para a clínica instalar e usar).** Resolvem problemas
  comuns; são o que uma clínica importa na Central. É aqui que você procura para **reusar**.
- **[`exemplos/`](./exemplos/) — exemplos DIDÁTICOS (para quem desenha agentes).** Mostram *o que dá
  para fazer* e *como*; são ponto de partida para adaptar, **não** produtos para instalar como estão.
  O material conceitual está na skill [`designer-agentes`](../skills/designer-agentes/SKILL.md).

## Times produtivos disponíveis

| Time | O que faz | Agentes | Risco |
|------|-----------|---------|-------|
| [briefing](./times/briefing/) | Cartão de contexto do paciente antes do atendimento | 1 (IA) | médio |
| [confirmacao-presenca](./times/confirmacao-presenca/) | Confirma presença por WhatsApp e triage a resposta | 3 (2 script + 1 IA) | médio |
| [jornada-cuidado](./times/jornada-cuidado/) | Vincula tarefas à jornada e avança/fecha fases | 2 (script) | médio |
| [jornada-avisos](./times/jornada-avisos/) | Avisa a equipe sobre pendências de SLA da jornada | 1 (script) | médio |

Cada pasta tem o `manifest.json` (para importar) e um `README.md` (o que faz, o que pede, o risco).

> **Nota:** estes são os times **oficiais/verificados**. Manifestos de terceiros/não-verificados são
> um tier separado (com assinatura e travas próprias) — ainda não habilitado.

## Exemplos didáticos

| Exemplo | Mostra o padrão de |
|---------|--------------------|
| [avisos-diretivas-ui](./exemplos/avisos-diretivas-ui/) | Diretiva de UI: aviso/ação na tela (toast/modal com botões; link vs. round-trip) |

Veja **[`exemplos/`](./exemplos/)** para o índice e como usá-los — comece pela skill
[`designer-agentes`](../skills/designer-agentes/SKILL.md).
