# laudo-liberacao-automatica — libera o resultado laudado sem a revisão da médica

Time de **1 agente `script`** que, quando o **laudo é ligado ao exame**, pede ao serviço de exames para **liberar o
resultado ao paciente** (ele passa a ver no portal) — **sem a revisão da médica**.

Só funciona nos **tipos de exame** que a clínica marcou com **"Liberação automática" = sim** no cadastro do tipo. A
trava é do serviço de exames, não deste agente: o agente pede, o serviço confere o tipo e recusa quando não pode.
Por isso não há lista de tipos de exame na configuração do agente — quem decide é o campo do tipo.

**Quando ele age (e quando não):** o agente só acorda quando o exame fica **laudado** (o documento de laudo foi ligado
ao resultado). O serviço de exames também aceitaria liberar um resultado **sem** laudo (tipo sem modelo de laudo, ou
clínica que não exige o laudo), mas este agente **não** age nesses casos: resultado sem laudo continua esperando a
liberação da equipe.

## O que faz

| Gatilho | Comportamento |
|---|---|
| O exame mudou de estado e ficou **laudado** (evento do serviço de exames, filtrado por `estado = laudado`) | pede a liberação do resultado mandando **só o id do exame** |

- **Liberou:** o resultado fica disponível ao paciente no portal, registrado como "liberado automaticamente pelo
  agente da clínica" (nunca em nome de um médico).
- **Recusas normais** (não são erro; o exame segue o fluxo de sempre, esperando a médica):
  - `TIPO_SEM_LIBERACAO_AUTOMATICA` — o tipo do exame não tem a liberação automática ligada;
  - `SEM_RESULTADO` — o exame ainda não tem resultado;
  - `LAUDO_EXIGIDO` — a clínica exige o laudo para liberar e ele ainda não está ligado.

  A execução termina com `skip` e o código da recusa.
- **Já liberado antes:** o serviço responde sucesso sem mudar nada — rodar de novo é seguro.
- **Falha aparece:** qualquer outra resposta (erro, exame não encontrado, serviço fora do ar) sai com log de aviso e
  `acao_bloqueada` no resumo da execução — nunca vira "liberado".
- **Avisa o paciente?** A liberação dispara o mesmo evento da liberação feita pela médica. Se a clínica tiver o time
  [`laudo-aviso`](../laudo-aviso/) instalado e ligado, o paciente recebe "Há um resultado novo no portal".

O resumo de cada execução mostra só se liberou ou o código da recusa — sem dado do paciente e sem o exame.

## O que este time pede (permissões)

| Permissão | Para quê |
|---|---|
| `exame_realizado:liberar_automatico` | pedir a liberação do resultado sem a revisão da médica |

É uma permissão **própria** desta liberação, dada só ao papel do agente: quem só pode mudar o estado do exame não
consegue liberar sem revisão. O agente **não lê** o resultado, o laudo nem o cadastro do paciente. A ação cita a
capability `exames.liberar_laudo` — o endereço real é resolvido em privado na instalação.

## Risco: **alto**

- ⚠️ **Libera resultado de saúde ao paciente sem a revisão da médica.** O paciente vê o resultado no portal assim
  que o laudo é ligado, sem ninguém da clínica conferir antes.
- 🤖 **Age sozinho**, a cada exame laudado.
- 🔒 Só nos tipos de exame marcados com "Liberação automática" = sim. Tipo sem essa marcação nunca é liberado por
  este agente, mesmo ligado.
- ✅ **Não** envia nada para fora por conta própria (o aviso ao paciente é do time `laudo-aviso`).

## Como ligar

O time **vem desligado**. Ligar em produção precisa do **ok do responsável pela clínica** — é a decisão de deixar o
paciente ver resultados sem a revisão da médica.

1. No cadastro de **tipos de exame**, marque "Liberação automática" = sim **só** nos tipos que podem sair sem
   revisão. Os demais ficam como estão (o padrão é não).
2. Importe este `manifest.json` (Central → Inteligência Artificial → Importar) e conceda ao papel do agente a
   permissão acima.
3. Com o ok do responsável, ligue o agente `laudo_liberacao_automatica` na lista de agentes (Central →
   Inteligência Artificial → agentes → ligar). É ali que ele liga e desliga, a qualquer momento.
4. (Opcional) Instale e ligue o time [`laudo-aviso`](../laudo-aviso/) para o paciente ser avisado.

> **Reimportar não mexe no ligado:** importar de novo este time atualiza o comportamento, mas **não** liga nem desliga
> o agente: vale o que a clínica deixou na lista de agentes. O "desligado" do manifesto só vale na primeira importação.

> **Publicação:** este time entra no catálogo depois que a release 2026.11.7 estiver em produção (ele depende da
> liberação automática do serviço de exames, que sobe nela).
