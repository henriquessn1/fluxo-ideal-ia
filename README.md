# Fluxo Ideal — Skills & Agents

Biblioteca **pública** de IA do Fluxo Ideal — a plataforma de gestão para clínicas (agendamento,
atendimento, vendas/preços, documentos, mensageria, etc.). Duas zonas:

- **`skills/`** — _pacotes de conhecimento de domínio_ que ajudam qualquer IA a **entender** como o
  produto funciona (raciocinar antes de agir).
- **`agents/`** — _times de agentes instaláveis_ que uma clínica pode **importar** e pôr para **agir**
  (ver [`agents/README.md`](agents/README.md)).

> **Este repositório é público e sanitizado por design** — e cada zona tem o seu nível:
> - As **skills** (`skills/`) NÃO contêm código, endpoints internos, IPs, segredos, matrizes de
>   permissão (RBAC) nem modelo de dados sensível/LGPD. Só o _domínio conceitual_.
> - Os **times de agentes** (`agents/`) têm um charter próprio: por serem instaláveis, **declaram as
>   permissões que pedem** (é a superfície de consentimento da clínica) e trazem o **comportamento**
>   (instrução/roteiro, como dado). Mas **também** não contêm endereços, rotas internas nem segredos —
>   cada ação cita uma **capability por nome**, e o endpoint real é resolvido em privado na instalação.
>
> Se algo permite a alguém **atacar** ou **clonar comercialmente** o produto, saiu do escopo — veja
> [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Para quem é isto

- **IAs / agentes** (com ou sem credencial) que precisam raciocinar sobre o domínio antes de agir.
  O ponto de entrada legível por máquina é [`llms.txt`](llms.txt).
- **Humanos** (novos no time, parceiros, integradores) que querem um modelo mental rápido de cada área.

Cada skill serve aos dois públicos no mesmo arquivo — a diferença está na densidade, não na linguagem
(ver "Linguagem" abaixo).

## Como usar

- **Como IA sem credencial:** busque a skill relevante no [`llms.txt`](llms.txt), baixe o `SKILL.md`
  correspondente e use-o como contexto. Cada skill diz explicitamente _quando usar_ e _quando NÃO usar_.
- **Como agente do Fluxo Ideal (com acesso ao MCP):** a skill é o "mapa mental"; as _ações_ reais
  continuam vindo das ferramentas autorizadas do MCP Gateway. A skill te diz **o que existe e por quê**;
  o MCP te dá o **como fazer** com permissão.

## Skills

| Skill | Papel | Cobre (domínio) | Status |
|---|---|---|---|
| [precificador](skills/precificador/SKILL.md) | Configurar preço → orçamento/venda | catálogo, tabelas de preço, condições e formas de pagamento, favoritos, cobertura de convênio, orçamento, venda | ✅ |
| [secretaria](skills/secretaria/SKILL.md) | Recepção / agenda | cadastro de paciente, agenda (marcar/remarcar/cancelar), disponibilidade, contexto de conversas | ✅ |
| [auxiliar-medico](skills/auxiliar-medico/SKILL.md) | Atendimento clínico (operacional) | check-in, etapas do atendimento, comentários da equipe, pendências, métricas | ✅ |
| [medico](skills/medico/SKILL.md) | Médico (assistencial) | conduzir + documentar o atendimento (adendo write-only), fila do dia — **IA nunca lê prontuário** | ✅ |
| [designer-documentos](skills/designer-documentos/SKILL.md) | Documentos | templates (sistema × design), conteúdo/versão, simular, publicar, documentos por paciente | ✅ |
| [designer-mensageria](skills/designer-mensageria/SKILL.md) | Autoria de mensageria | templates, canais (WhatsApp/HSM, e-mail), aprovação de HSM — **desenhar**, não enviar | ✅ |
| [comunicacao-paciente](skills/comunicacao-paciente/SKILL.md) | Envio governado ao paciente | enviar e-mail por template, intenção governada (quiet-hours/teto/idempotência), checar entrega | ✅ |
| [financeiro](skills/financeiro/SKILL.md) | O dinheiro depois | pagamentos, parcelas, contas a receber/pagar, caixa, fluxo de caixa, break-even, nota fiscal | ✅ |
| [faturamento-convenio](skills/faturamento-convenio/SKILL.md) | Financeiro de convênio (TISS) | faturar guias/lotes, demonstrativo, glosa, recurso | ✅ |
| [designer-agentes](skills/designer-agentes/SKILL.md) | Agentes de IA | reusar um time do registro (`agents/`) ou desenhar comportamento (persona, capabilities, gatilhos, LLM × script) | ✅ |
| [conversas](skills/conversas/SKILL.md) | Atender/triar tickets | filas, atribuição, resolução (CSAT), transferência, observadores, detectar frustração | ✅ |
| [pesquisas-satisfacao](skills/pesquisas-satisfacao/SKILL.md) | CX / NPS | pesquisa e gatilhos, funil de convites, reenviar/antecipar, resultados agregados (NPS) | ✅ |
| [anamnese](skills/anamnese/SKILL.md) | Questionário pré-consulta | configurar modelos (perguntas por procedimento/pacote), criar fichas, acompanhar preenchimento/status — **sem ler as respostas (dado de saúde)** | ✅ |
| [indicadores](skills/indicadores/SKILL.md) | BI / gestão | dashboard executivo cross-domínio, significado dos KPIs, exportação de dados | ✅ |
| [administrador-clinica](skills/administrador-clinica/SKILL.md) | Config da clínica | dados do estabelecimento, branding, profissionais, convênios | ✅ |
| [gestor-tarefas](skills/gestor-tarefas/SKILL.md) | Tarefas internas | criar/atribuir/mover/buscar afazeres da equipe, minhas pendências | ✅ |
| [jornada](skills/jornada/SKILL.md) | Jornada de Cuidado (caso longo) | configurar o modelo (fases/etapas/marcos), acompanhar (fase, pendências/SLA) e operar a jornada do paciente; marcos = tarefas; fase derivada | ✅ |
| [reportar-e-sugerir](skills/reportar-e-sugerir/SKILL.md) | Qualidade (feedback ao sistema) | reportar bug (evidência esperado×obtido) / sugerir melhoria ou capacidade nova / acompanhar o desfecho — seguro, universal, sem PII | ✅ |

## Agents (times de agentes instaláveis)

Enquanto uma _skill_ ajuda uma IA a **entender** o domínio, um **time de agentes** é uma automação
que **age** — a clínica **importa** por link na Central (com um cartão de risco antes de aplicar) e
pronto. Cada ação de um agente cita uma **capability por nome** (sem rota interna); o que ele
realmente consegue fazer é limitado pelas **permissões** de quem instala (a instalação não escala
privilégio). Detalhes e charter em [`agents/README.md`](agents/README.md).

| Time | O que faz | Agentes | Risco |
|---|---|---|---|
| [briefing](agents/briefing/) | Cartão de contexto do paciente antes do atendimento | 1 (IA) | médio |
| [confirmacao-presenca](agents/confirmacao-presenca/) | Confirma presença por WhatsApp e triage a resposta | 3 (2 script + 1 IA) | médio |
| [jornada-cuidado](agents/jornada-cuidado/) | Vincula tarefas à jornada e avança/fecha fases | 2 (script) | médio |
| [jornada-avisos](agents/jornada-avisos/) | Avisa a equipe sobre pendências de SLA da jornada | 1 (script) | médio |

> Estes são os times **oficiais/verificados**. Um tier aberto a **terceiros/não-verificados** (com
> assinatura e travas próprias) ainda não está habilitado.

## Linguagem: humano vs. IA

Mesmo formato (Markdown), enquadramento diferente:

- **Para humano:** prosa, contexto, "por quê".
- **Para IA:** conciso, imperativo, estruturado, com _"quando usar / quando NÃO usar"_ explícito e
  vocabulário canônico. O índice `llms.txt` é o padrão emergente de "sitemap para IAs".

Não inventamos uma linguagem própria: usamos o formato **Agent Skills** (`SKILL.md` com frontmatter +
divulgação progressiva) — o mesmo padrão aberto que ferramentas de IA já consomem.

## Fonte da verdade & atualização

O conteúdo aqui é **derivado e sanitizado** da documentação interna do produto (privada). Regras de
curadoria e o gatilho de atualização estão em [`CONTRIBUTING.md`](CONTRIBUTING.md). Resumo: **quando
o comportamento de uma área muda, as skills que a cobrem são revisadas** — skill desatualizada é pior
que ausente.
