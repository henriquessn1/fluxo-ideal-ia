---
name: pesquisas-satisfacao
description: O instrumento de SATISFAÇÃO do paciente no Fluxo Ideal — criar/editar/ativar a pesquisa de CX/NPS (perguntas, gatilho, anonimato), configurar o disparo automático (ligar/desligar, atraso), acompanhar quem foi convidado e como caminhou o convite, e ler os resultados AGREGADOS (NPS, notas médias, distribuição). Use para "cria uma pesquisa de NPS", "liga o disparo pós-consulta", "qual o NPS deste mês?", "qual a taxa de resposta?", "por que o paciente não recebeu?", "reenvia/antecipa o convite".
audience: [ia, humano]
depends_on: [pesquisa-cx, satisfacao, nps]
version: 0.2.0
updated: 2026-07-13
---

# Pesquisas de satisfação

Operar o **instrumento de medição da experiência do paciente** (CX): entender a pesquisa em si,
acompanhar os **convites** enviados e ler os **resultados agregados** (NPS, notas, distribuição).
O foco é a **satisfação**, não a operação do dia a dia da clínica.

## Quando usar
- **Criar / editar / ativar** uma pesquisa: as perguntas (vários tipos), o **gatilho** e o **modo de
  anonimato** — com pré-visualização e confirmação.
- **Configurar o disparo automático**: ligar/desligar e ajustar o **atraso** (horas/minutos).
- "Qual o NPS deste mês?", "qual a nota média do atendimento?", "como estão as respostas?".
- "Qual a taxa de resposta?", "quantos convites saíram / foram respondidos / falharam?".
- "Por que o paciente não recebeu a pesquisa?", "o disparo automático está ligado?".
- Fazer **um** convite específico sair agora (antecipar) ou sair de novo (reenviar).

## Quando NÃO usar
- Escrever/ajustar o **texto** da mensagem de convite ou o canal por onde ela vai → `designer-mensageria`.
  Aqui é o **instrumento** (perguntas, convites, resultados); lá é **como se fala** com o paciente.
- Painel executivo geral da clínica (agenda, comercial, financeiro juntos) → `indicadores`. O NPS
  aparece lá como **um** número num dashboard maior; aqui é a leitura completa da pesquisa.
- **Apagar** uma pesquisa ou ler **respostas individuais** (quem respondeu o quê) — ficam de fora:
  exclusão é destrutiva e a resposta individual é dado sensível. Aqui se **cria/edita/ativa** e se lê o
  **agregado**.

## Modelo mental

Uma pesquisa de satisfação é um **instrumento que dispara sozinho** e cujas respostas viram
**número agregado**. Três peças, em fila:

```
   PESQUISA (o instrumento)          CONVITE / ENVIO (por paciente)        RESULTADO (agregado)
   perguntas + gatilho + anonimato →  agendado → enviado → respondido  →   NPS · média · distribuição
                                              └──────────→ falha
```

- **A pesquisa tem um gatilho.** Ela não é enviada à mão em massa: cada evento que a arma
  (o **atendimento finalizado**, ou um **ticket de conversa resolvido** — a CSAT do inbox) gera
  **um convite** para aquele paciente. Há no máximo **uma pesquisa ativa** por gatilho, por clínica.
- **O convite tem um ciclo de vida**: nasce **agendado** (aguardando o atraso configurado), vira
  **enviado** quando o convite sai, **respondido** quando o paciente responde, ou **falha** quando o
  envio deu erro (ex.: e-mail devolvido). A **taxa de resposta** sai desse funil.
- **O disparo é automático e tem atraso.** Depois do gatilho, o convite espera um tempo configurado
  (horas + minutos) antes de sair — dá um respiro ao paciente. Um **motor** cuida disso; se ele estiver
  desligado ou parado, nada sai — e silêncio **não** é sinal de que está tudo bem.
- **Resultado é sempre agregado.** A leitura de satisfação é NPS, nota média e distribuição — nunca
  "o que o paciente Fulano respondeu". A resposta individual é dado sensível e não é o instrumento de
  gestão.

## Glossário
- **Pesquisa**: o instrumento — um conjunto de **perguntas** ligado a um **gatilho** e a um **modo de anonimato**. No máximo **uma ativa por gatilho** por clínica.
- **Pergunta**: pode ser de vários tipos — **escala** / **estrelas** / **likert** (nota numérica, entram no NPS/média), **múltipla escolha** / **sim-não** / **seleção múltipla** (contagem por opção) e **texto livre** (comentário).
- **Gatilho**: o que arma a pesquisa — **atendimento finalizado** (pós-consulta) ou **ticket resolvido** (CSAT do inbox, a satisfação do atendimento por conversa).
- **Modo de anonimato**: **identificada** (resposta ligada ao paciente), **anônima** (sem vínculo) ou **o paciente escolhe** na hora. Decidido no cadastro da pesquisa.
- **Envio / convite**: o registro de que um paciente foi convidado a responder — com seu **status** no ciclo.
- **Disparo automático**: a automação que agenda e envia os convites após o gatilho, respeitando o **atraso** configurado.
- **Taxa de resposta**: respondidos ÷ enviados — o quanto do público convidado de fato respondeu.
- **NPS**: índice de -100 a 100 derivado das notas (promotores − detratores). A leitura-síntese da lealdade do paciente.
- **CSAT**: satisfação com o atendimento (média das notas) — o "quão satisfeito".

## Ferramentas (tarefa → ferramenta)
> A execução depende de **autorização** — a plataforma aplica permissão; a skill só ensina a intenção e
> o _quando_. As **escritas pré-visualizam** (dry-run) e aplicam só após confirmar.

**Ler**
- **Ver quais pesquisas existem / qual está ativa / quais perguntas e qual o gatilho** → ferramenta que
  lista as pesquisas (a ativa e, sob pedido, as perguntas e o gatilho configurado).
- **Ler os resultados — NPS, nota média, distribuição, contagem por opção** → ferramenta de resultados
  (filtrável por profissional e período). É a **joia** do módulo.
- **Acompanhar o funil de convites e a taxa de resposta** → ferramenta de envios (contagem por status +
  taxa; opcionalmente uma amostra **sem dados pessoais**).
- **Diagnosticar por que os convites não estão saindo** → ferramenta de estado do disparo (automação
  ligada?, atraso, motor vivo, fila parada). **Não trate silêncio como "ok"** — leia o aviso.

**Configurar (o instrumento — cadastro, com confirmação)**
- **Criar / editar / ativar** a pesquisa: perguntas (escala/estrelas/likert, múltipla escolha/sim-não/
  seleção múltipla, texto livre), **gatilho** e **modo de anonimato** → ferramenta de autoria de pesquisa.
  Pré-visualiza antes de gravar; **apagar** uma pesquisa fica de fora.
- **Ligar/desligar o disparo automático** e ajustar o **atraso** (horas/minutos) → ferramenta de config
  do disparo. Mostra o **atual × a proposta** antes de aplicar.

**Convite (toca o paciente — confirma antes)**
- **Fazer um convite específico sair de novo** (falhou / não respondeu) → ferramenta de reenviar convite.
- **Fazer um convite agendado sair agora**, sem esperar o atraso → ferramenta de antecipar envio.

**Ordem mental para "como está a satisfação?":** pesquisa ativa → resultados (NPS/média) → se os números
parecem magros, olhe o funil de envios (taxa de resposta) → se poucos convites saíram, cheque o estado do disparo.

## Fluxos comuns

### "Qual o NPS / a satisfação deste mês?"
1. Ache a **pesquisa ativa**.
2. Leia os **resultados** dela no período pedido (dá para recortar por profissional).
3. Reporte os agregados: NPS, nota média (CSAT), distribuição — **nunca** respostas individuais.

### "Poucas respostas — por quê?"
1. Veja o **funil de envios**: a taxa de resposta é baixa, ou saíram poucos convites?
2. Se saíram poucos convites, cheque o **estado do disparo**: automação desligada? motor parado? fila agendada represada?
3. Se há um convite específico travado ou que falhou, **reenvie**; se um agendado precisa sair já, **antecipe**.

### "O paciente disse que não recebeu"
1. Cheque o **estado do disparo** (a automação pode estar off ou o motor parado).
2. Localize o **envio** daquele contexto e o status dele (agendado / falha).
3. **Reenvie** (se falhou/não respondeu) ou **antecipe** (se está agendado esperando o atraso).

## Regras e invariantes
- **A pesquisa dispara por gatilho** — não é campanha em massa manual; cada evento (atendimento finalizado / ticket resolvido) gera **um** convite.
- **No máximo uma pesquisa ativa por gatilho** por clínica.
- **Satisfação se lê no agregado** — NPS, média, distribuição. Comentários de **texto livre** do paciente são dado sensível: ficam **omitidos por padrão** (só se sabe **quantos** existem) e, quando lidos, vêm com dados pessoais redigidos. Nunca use o instrumento para identificar quem respondeu o quê.
- **Reenviar e antecipar são ações que atingem o paciente** — o paciente recebe uma mensagem real. **Confirme com o usuário antes.**
- **Antecipar ≠ reenviar**: antecipar só vale para convite **agendado** (pula a espera); reenviar recoloca na fila um convite que **falhou ou não foi respondido**. Nenhum dos dois convida paciente novo nem cria pesquisa — só mexem num convite **que já existe**. Convite **já respondido** não é reenviado.
- **Silêncio não é saúde** — se ninguém recebeu, cheque o estado do disparo antes de concluir que "está calmo".
- **Configurar ≠ disparar.** Criar/editar/ativar a pesquisa e ligar/ajustar o disparo automático é
  **cadastro** (reversível, interno) — a IA faz **com confirmação**. Mas a IA **não sai convidando
  paciente por conta própria**: quem envia é o **motor automático** (por gatilho) ou o humano via
  reenviar/antecipar (que confirmam). **Apagar** uma pesquisa e ler **respostas individuais** ficam **fora**.

## Limites / o que esta skill NÃO cobre
- Não escreve nem ajusta o **texto/canal** do convite → `designer-mensageria`.
- Não é o **dashboard executivo** da clínica (agenda + comercial + financeiro) → `indicadores`.
- **Cria/edita/ativa** a pesquisa e **configura** o disparo (com confirmação), mas **não apaga** uma
  pesquisa nem lê **respostas individuais** (quem respondeu o quê é dado sensível — só o agregado).
- A IA **não dispara convites em massa autonomamente** — o envio é do motor automático (por gatilho) ou
  do humano (reenviar/antecipar, gated). Ligar o motor é config; **ser** o motor não é.
