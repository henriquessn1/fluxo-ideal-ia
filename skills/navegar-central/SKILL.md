---
name: navegar-central
description: Como a IA GUIA o usuário até a tela certa da Central (o painel web da clínica) — sem navegar por ele. Para ações que são do humano por design (importar um time de agentes, conceder um acesso/permissão, configurar algo), a IA diz o CAMINHO e os PASSOS, e monta um link clicável quando sabe o endereço que o usuário usa pra abrir a Central. Use para "como eu importo esse time?", "onde concedo essa permissão?", "onde configuro X?".
audience: [ia, humano]
depends_on: [central, navegacao]
version: 0.1.0
updated: 2026-07-17
---

# Navegar na Central

Você (a IA) **não opera** a Central — o painel web da clínica é do humano, e várias ações são
**deliberadamente manuais** porque criam poder (importar um time de agentes cria acessos; conceder
uma permissão muda quem-pode-o-quê). Seu papel nesses casos não é *fazer*, é **guiar**: dizer com
precisão **onde clicar** e **o que fazer** — de preferência com um **link clicável**.

## Quando usar
- O usuário quer fazer algo que é **ação dele na Central**, não sua: **importar um time de agentes**,
  **conceder um acesso/permissão** a uma função, **configurar** uma parte da clínica.
- Você acabou de fazer algo que **depende de um passo do dono** — o caso clássico: uma capacidade
  nova (ex.: uma ferramenta que só aparece depois que o administrador **concede a permissão** à
  função). Aí você guia o usuário até a tela de acessos.
- O usuário pergunta **"onde eu faço X?"** / **"como eu chego em Y?"** na Central.

## Quando NÃO usar
- **A ação tem ferramenta.** Se dá pra fazer por uma ferramenta do seu papel (marcar consulta, montar
  orçamento, abrir tarefa…), **faça** — não mande o usuário clicar na tela à toa.
- **Conteúdo/dados** (o "o quê"), não o "onde". Isso é a skill do papel (`secretaria`, `precificador`,
  etc.). Aqui é só **como chegar na tela**.

## Modelo mental

Guiar é **apontar o caminho**, não andar por ele:

```
   o usuário precisa fazer algo que é ação DELE na Central
                         │
                         ▼
        pegue o CAMINHO + PASSOS atuais  (ferramenta de navegação — fonte viva)
                         │
                         ▼
        precisa da BASE?  ──não sei──►  PERGUNTE: "qual endereço você usa
        (endereço da Central)            pra abrir a Central da clínica?"
                         │
                         ▼
        ENTREGUE: link clicável {base}{caminho}  (ou o caminho + passo a passo)
```

Ideias que sustentam tudo:

- **Você guia, não navega.** O sistema **não opera a tela** por você. Ações privilegiadas (importar
  time, conceder acesso) ficam com o **humano** — de propósito. Nunca diga "já importei"; diga "abra
  aqui e faça assim".
- **Nunca decore nem invente caminhos.** As telas da Central **mudam**. Um caminho que você "lembra"
  pode estar morto amanhã. **Sempre** pegue o caminho pela **ferramenta de navegação** — ela é a
  fonte viva e atual. Se a ferramenta não tem o destino, **diga isso** em vez de chutar uma URL.
- **O endereço-base é do usuário — pergunte se não souber.** A Central é **white-label**: cada
  clínica abre por um endereço próprio (o seu pode ser `clinica.suamarca.com.br`). O sistema **não**
  sabe qual é o seu. Para virar um link clicável, você precisa da **base**. Se você não a conhece na
  conversa, **pergunte**: *"Qual endereço você usa pra abrir a Central da clínica?"* — e junte com o
  caminho. Sem a base, entregue o **caminho + o passo a passo** do menu (o usuário já está logado; ele
  sabe a base dele).
- **Dê o passo a passo, não só a URL.** Um link clicável é ótimo; mas explique também o caminho do
  menu (ex.: *Configuração → Agentes → Importar*) — funciona mesmo se o link falhar, e ensina o
  usuário.

## Glossário
- **Central**: o painel web de gestão da clínica (onde o time configura, importa, concede acessos).
- **Base / endereço da Central**: o endereço que **aquele** usuário usa pra abrir a Central da clínica
  dele (white-label — varia por clínica). É a peça que falta pra montar um link clicável.
- **Caminho**: a rota da tela dentro da Central (ex.: `/configuracao/agentes/importar`). Junto com a
  base vira o link completo.
- **Destino**: uma tela de alto valor que a ferramenta de navegação conhece (ex.: *importar um time
  de agentes*, *conceder acesso*).
- **Ação privilegiada**: algo que só o humano faz na Central por criar poder/acesso (importar time,
  conceder permissão) — você **guia**, não executa.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. Guiar é uma ação **segura e universal** — disponível a qualquer
> papel. A execução depende de **autorização** como qualquer outra.

- **Descobrir para onde mandar o usuário** → a **ferramenta de navegação da Central**. Sem alvo, ela
  **lista os destinos** que conhece (e quando usar cada um) — escolha o que casa com o pedido. Com o
  alvo, devolve o **caminho**, a **trilha do menu** e os **passos**. É a **fonte viva** dos caminhos —
  use-a em vez de lembrar/inventar rotas.
- **Montar o link** → componha `{base}{caminho}`. Se você **não sabe a base**, **pergunte** ao usuário
  qual endereço ele usa pra abrir a Central; se ele não quiser dizer, entregue o **caminho + passo a
  passo** (ele conhece a própria base).

**Ordem mental para "onde eu faço X?":** confirme que é **ação na tela** (não algo que você faz por
ferramenta) → pegue o **destino** pela ferramenta de navegação → tenha a **base** (pergunte se não
souber) → **entregue** o link clicável + o passo a passo.

## Fluxos comuns

### Importar um time de agentes
1. Deixe claro que **quem importa é o usuário** (é ação dele — cria acessos; você não faz).
2. Pegue o destino *importar um time de agentes* pela ferramenta de navegação (caminho + passos).
3. Precisa da **base**? Se não a conhece, pergunte o endereço da Central do usuário.
4. Entregue: *"Na sua Central, abra **Configuração → Agentes → Importar** (link: `{base}/configuracao/agentes/importar`) e **cole o endereço do time**; confira o plano e confirme."*

### Conceder um acesso que destrava uma capacidade nova (o "gate do dono")
1. Quando algo que você tentou usar **depende de uma permissão** que o dono ainda não concedeu,
   explique **o que falta** e guie até a tela de **acessos/permissões**.
2. Pegue o destino *conceder acesso* pela ferramenta de navegação.
3. Entregue o caminho + passos: *"Peça a um administrador de acessos pra abrir **Configuração →
   Acessos → Permissões**, escolher a função certa e marcar a permissão — aí a capacidade passa a
   aparecer."*

## Regras e invariantes
- **Guiar, não navegar.** Você aponta o caminho; **quem clica é o humano**. Ações privilegiadas são
  dele por design.
- **Caminho vem sempre da ferramenta de navegação** — nunca de memória ou chute. Telas mudam; a
  ferramenta é a fonte viva. Destino inexistente → diga que não sabe, não invente URL.
- **Base é do usuário.** Não invente o domínio da clínica (é white-label). Se não souber, **pergunte**;
  na falta, entregue caminho + passo a passo.
- **Prefira link clicável + passo a passo juntos** — o link agiliza, o passo a passo resiste a
  mudança e ensina.

## Limites / o que esta skill NÃO cobre
- **Fazer a ação por ele.** Você não opera a Central; ações privilegiadas (importar, conceder acesso)
  são do humano.
- **O conteúdo da tela** (o que preencher clinicamente, quanto cobrar, quem cadastrar) → skills do
  papel. Aqui é só **como chegar lá**.
- **O mapa completo do painel.** A ferramenta de navegação conhece um conjunto **curado** de destinos
  de alto valor — não toda tela. Se o destino não estiver lá, oriente por menu de forma geral e, se
  fizer sentido, sugira que o time adicione o destino.
- **O endereço da clínica.** O sistema não o conhece (white-label) — ele vem do **usuário**.
