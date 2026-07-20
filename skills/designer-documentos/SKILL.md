---
name: designer-documentos
description: O sistema de documentos do Fluxo Ideal — como se desenha, versiona, previsualiza e publica o MODELO de um documento (receita, atestado, laudo, orçamento, TCLE…) e como esses modelos viram documentos gerados por paciente. Cobre BLOCOS REUTILIZÁVEIS (cabeçalho/rodapé/assinatura/cláusula incluídos em vários modelos — sempre reaproveitar em vez de duplicar HTML), nascer um corpo do zero (inclusive migrar DOCX→HTML, herdando as habilitações do legado pra o documento não sumir do picker), GERIR HABILITAÇÕES (quem pode emitir cada documento) e os TEMPLATES DE TERMOS (o texto legal versionado de aceite/intercorrências/itens não inclusos/TCLE que entra nos orçamentos) — o CONTEÚDO, distinto da fôrma HTML. Use para entender "como esse documento fica", para criar/editar/publicar um template com segurança, reaproveitar blocos e redigir/versionar os termos.
audience: [ia, humano]
depends_on: [documentos-clinicos, templates, catalogo-documentos, termos-orcamento]
version: 0.4.3
updated: 2026-07-20
---

# Designer de Documentos

Desenhar e manter os **modelos de documento** de uma clínica — o que a receita, o atestado, o
laudo, o orçamento ou o TCLE mostram e como ficam quando impressos/emitidos — e enxergar os
documentos que já foram **gerados por paciente**. Desenhar aqui **não é** só escrever um texto:
é operar um **ciclo de vida** (conteúdo → versão → preview → publicação) que faz o modelo certo
chegar à geração real sem quebrar o que já está em produção.

## Quando usar
- "Como esse documento fica?" / "quero mudar o cabeçalho da receita" / "trocar o logo do atestado".
- Criar um **tipo de documento** novo e habilitá-lo para geração.
- Editar o **conteúdo** de um modelo, **previsualizar** com dados fictícios e **publicar** a versão oficial.
- Ver quais **modelos um profissional pode emitir**, e quais **documentos um atendimento já tem**.
- Cuidar dos **modelos de sistema** globais (Orçamento e TCLE).
- **Redigir/versionar os termos** que entram nos orçamentos — o **texto** da declaração de aceite, das
  intercorrências, dos itens não inclusos, do **TCLE**: criar, editar, marcar o **padrão** do tipo.
- **Reaproveitar um bloco** (cabeçalho, rodapé, assinatura, cláusula padrão) em vários documentos, em vez
  de copiar o mesmo HTML em cada modelo.
- **Começar um documento do zero** (quando não há um parecido para copiar) — inclusive **trazer um
  documento antigo (DOCX) para o editor novo (HTML)**.

## Quando NÃO usar
- **Enviar** o documento ao paciente (e-mail/WhatsApp/link) → skill de mensageria/envio.
- **Preço** dentro do orçamento (itens, tabelas, cobertura, condições) → skill `precificador`.
  Aqui cuida-se só de **como o orçamento fica** (o modelo), não de **quanto custa**.
- **Assinatura eletrônica** do paciente e o fluxo do link de assinatura → fora desta skill.
- **Baixar/abrir o PDF** de um documento gerado — a leitura aqui é só de **quais** documentos
  existem; abrir o arquivo é pela Central.

## Modelo mental

Um documento no Fluxo Ideal nasce de um **modelo (template)** e termina como um **arquivo gerado
por paciente**. No meio há um ciclo de vida de design que existe justamente para você poder mexer
no modelo sem estragar o que já está sendo usado:

```
  TIPO de documento (receita, atestado, laudo, orçamento…)
        │
        ├── estrutura de dados (quais campos o modelo preenche)
        │
        └── vínculo tipo↔template  ── liga o tipo a um MODELO (digital e/ou impresso)
                     │
                     ▼
             TEMPLATE (o modelo em si)
                     │  ciclo de conteúdo:
                     │   rascunho ──edita──► rascunho ──publica──► VERSÃO OFICIAL
                     │   (preview a qualquer momento, com dados fictícios)
                     ▼
         geração real ──► DOCUMENTO por paciente (fica no atendimento)
```

Algumas ideias sustentam tudo:

- **Modelo ≠ documento gerado.** O template é a fôrma; o documento do paciente é o que sai da fôrma
  numa emissão. Mudar o template **não** reescreve documentos já gerados.
- **Conteúdo é versionado — rascunho vs. publicado.** Você edita **rascunhos** à vontade (reversível);
  só a **publicação** vira a versão **oficial** usada na geração real. Versão já publicada **não se
  edita** — cria-se um rascunho novo. Publicar é a ação de **maior alcance** (blast radius): confirme
  sempre, e **previsualize antes**.
- **Nasce inativo, ativa-se de propósito.** Tipo novo, vínculo tipo↔template e estrutura de dados
  nascem **inativos** — invisíveis à geração real. Só a **ativação** (também de alto alcance, confirme)
  os torna emissíveis. Isso deixa você montar/testar sem risco de alguém emitir um modelo meio-pronto.
- **Template de SISTEMA ≠ template de DESIGN.** A maioria dos modelos passa pelo ciclo de catálogo
  (tipo → dados → vínculo → ativação) e é o que a skill chama de **design** (customizável). **Dois**
  modelos são de **sistema** — globais e admin-only: **Orçamento** e **TCLE**. Eles são versionados e
  publicáveis igual, mas **não** passam pelo fluxo de tipo↔template, então **não aparecem** no catálogo
  de design — têm um caminho próprio.
- **A fôrma ≠ o conteúdo do termo (o "caso do TCLE").** Um documento como o **TCLE** tem **duas
  camadas** que vivem em **lugares diferentes**: (1) a **fôrma** — o template HTML de **sistema** acima,
  que diz *como o papel fica* (cabeçalho, layout, onde o texto entra); e (2) o **conteúdo do termo** — o
  **texto legal em si** ("Declaro que fui informado…"), que é **versionado à parte** e é o que o paciente
  lê e assina. Esse conteúdo mora nos **Templates de Termos** (uma tela própria, nas configurações da
  clínica), **não** no catálogo de design. Mexer na fôrma HTML **não** muda o texto do termo,
  e vice-versa. Cada **tipo de termo** (declaração de aceite, intercorrências, itens não inclusos, TCLE,
  outros) pode ter vários templates, e **um** deles é o **padrão** — o que o orçamento novo já traz.
- **O tipo TCLE tem caminho próprio — é o que muda de verdade.** Os tipos declaração de aceite,
  intercorrências, itens não inclusos e outros são **blocos de texto** que entram no orçamento e pronto.
  O **TCLE** é diferente: seu template é o **molde de um consentimento assinável**. Quando o TCLE é
  aplicado a uma venda, ele vira um **documento próprio, juridicamente forte** — com o **texto travado**
  (snapshot), assinaturas do **médico e do paciente**, e obrigatoriedade/validade. Ou seja: aqui você
  **redige e versiona o molde do TCLE** (o texto + os itens de consentimento + o tempo de leitura); a
  **coleta das assinaturas** e a geração do documento assinável **não** são desta skill (é a plataforma,
  ato jurídico). É a diferença entre **escrever a minuta** e **assinar o contrato**. Nos outros tipos
  essa segunda camada nem existe.

- **Blocos reutilizáveis — não repita HTML.** Partes que se repetem em vários documentos — o **cabeçalho**
  da clínica, o **rodapé**, o **bloco de assinatura**, uma **cláusula padrão** — **não** devem ser copiadas
  em cada modelo. Elas viram **blocos reutilizáveis** próprios, e cada modelo os **inclui** pelo nome (uma
  chamada de inclusão no HTML, em vez do HTML colado). Ganhos: mudar o cabeçalho **num lugar só** atualiza
  **todos** os documentos que o incluem, e some o risco de versões divergentes do mesmo pedaço. Um bloco é
  um modelo como outro — só que **marcado como reutilizável** (não é um documento completo, então **não**
  aparece para emissão) e é chamado de dentro dos outros. **🧩 Regra de ouro do design: antes de escrever
  um trecho de HTML, procure um bloco reutilizável que já o resolva; se um trecho vai aparecer em mais de
  um documento, transforme-o num bloco e inclua-o — nunca duplique.** Ao **inspecionar as variáveis** de um
  modelo, as variáveis dos blocos incluídos **vêm junto** (o sistema resolve o bloco publicado ao renderizar).

**Distinção digital × impresso:** um vínculo pode ter um modelo para a via **digital** e outro para a
**impressa**. São dois templates para o mesmo tipo, escolhidos conforme a saída.

## Glossário

**Catálogo de design**
- **Tipo de documento**: a categoria — receita, atestado, laudo, orçamento, TCLE… É o que o profissional
  escolhe antes de emitir.
- **Estrutura de dados**: quais campos o modelo espera preencher (o "formulário" por trás do documento),
  identificada por nome + versão. Inclui os **campos de digitação** que a **tela de emissão** mostra para
  preencher — cada campo tem **nome** (a variável), **rótulo**, um **tipo** (texto, área de texto, data,
  seleção, etc.), **obrigatoriedade**, **grupo** (é o grupo que separa, por ex., a *observação do paciente*
  da *observação da empresa*) e **opções** quando é seleção. Esse contrato de tela é **rico e pertence à
  interface** — a plataforma o guarda **como está**, sem simplificar; a tela de emissão **já o renderiza**.
- **Vínculo tipo↔template**: a ligação que diz "este tipo usa **este** modelo" (digital e/ou impresso) com
  **esta** estrutura de dados. É o que torna um tipo realmente emissível quando **ativo**.
- **Ativo/inativo**: um recurso do catálogo só entra na geração real quando **ativado**; nasce inativo.

**Ciclo de conteúdo do template**
- **Template (modelo)**: o documento-fôrma em si, com layout e campos a preencher.
- **Versão**: cada estado do conteúdo do template. Há **rascunhos** (editáveis) e, no máximo, uma
  versão **publicada** (a oficial).
- **Rascunho**: versão em edição, reversível, que **não** é usada em geração real.
- **Publicação**: promover uma versão a **oficial** — passa a ser a usada de fato. Alcance amplo.
- **Preview / simulação**: renderização fiel do modelo com **dados fictícios** e marca d'água de amostra,
  **sem efeito** (não grava nada, não emite nada). É a rede de segurança antes de publicar/ativar. O preview
  chega como um **link temporário** (abre/baixa; expira em ~30 min) — repasse-o ao usuário para ele ver; o
  arquivo em si não vem embutido na conversa.

**Blocos reutilizáveis**
- **Bloco reutilizável**: um modelo HTML **marcado como reutilizável** — um pedaço (cabeçalho, rodapé,
  bloco de assinatura, cláusula padrão) feito para ser **incluído** em outros modelos, **não** emitido
  sozinho (por isso não aparece nos seletores de emissão). Editar/publicar o bloco reflete em **todos** os
  modelos que o incluem. Também é versionado (rascunho → publicado), como qualquer template.
- **Inclusão**: um modelo completo **puxa** um bloco reutilizável pelo nome; ao renderizar, o sistema
  resolve a **versão publicada** do bloco. As **variáveis** que o bloco espera contam junto com as do
  modelo (a inspeção de variáveis do modelo já traz as dos blocos incluídos).

**Assets**
- **Asset**: arquivo usado no design — **imagem/logo** (ex.: logo no cabeçalho) ou **folha de estilo (CSS)**
  do design system. Um asset em uso não some sem confirmação explícita (o sistema avisa onde ele é
  referenciado). Dá para **ler o conteúdo** de um asset antes de mexer nele: os de **texto** (CSS, SVG)
  vêm com o conteúdo **à mão** para você propor a mudança; os **binários** (imagens) vêm como **referência**
  (a leitura fiel do texto é o que permite editar sem sobrescrever às cegas).

**Modelos de sistema**
- **Orçamento** e **TCLE**: os dois modelos **globais** (admin-only) que fogem do catálogo de design.
  Versionados e publicáveis, mas com caminho próprio. Cuidam da **fôrma** (como o papel fica).

**Termos do orçamento (o conteúdo)**
- **Template de termo**: o **texto legal versionado** que entra num orçamento — o **conteúdo**, não a
  fôrma. Tem um **código** (ex.: `TCLE-BIOPSIA-INC`), um **nome**, um **tipo**, o **texto** em si e,
  opcionalmente, os **itens de consentimento** e um **tempo mínimo de leitura**.
- **Tipo de termo**: a categoria do termo — **declaração de aceite**, **intercorrências**, **itens não
  inclusos**, **TCLE** (consentimento) e **outros**. Cada tipo pode ter vários templates; **um** é o
  **padrão**. ⚠️ **O TCLE é o tipo especial**: enquanto os outros são blocos de texto no orçamento, o
  molde de TCLE gera um **documento assinável** (texto travado + assinaturas médico/paciente) quando
  aplicado a uma venda. Aqui você cuida do **molde**; o assinável é da plataforma.
- **Padrão do tipo**: o template que o **orçamento novo já traz** para aquele tipo. Definir um novo
  padrão **desmarca** o anterior (é sempre **um** por tipo).
- **Versão do termo**: como no design, o conteúdo é **versionado** — mas aqui a regra é automática:
  **mudar o texto cria uma versão nova** e preserva a anterior no histórico (imutável). Orçamentos que
  já usaram um termo guardam o **snapshot** do texto — reeditar o template **não** reescreve o que já
  foi assinado.
- **Itens de consentimento**: as frases "**Li e entendo que…**" que viram **checkbox** na assinatura do
  paciente (cada clique é carimbado). Vazio = sem checklist.
- **Tempo mínimo de leitura**: segundos que o paciente precisa ficar no termo antes de a assinatura
  habilitar (0 = sem trava).

**Documentos gerados**
- **Documento do paciente**: o arquivo que saiu de uma emissão real (receita/atestado/laudo/orçamento/
  TCLE…), guardado no **atendimento**. A leitura aqui lista **quais** existem (nome, tamanho, data, tipo)
  — sem baixar o arquivo.
- **Modelos habilitados por profissional**: dentre os tipos ativos, quais **este** profissional pode emitir.
- **Habilitação (quem pode emitir)**: o vínculo **profissional ↔ tipo-template** que faz um documento
  aparecer no **picker de emissão** daquele profissional. Um tipo-template ativo mas **sem habilitação**
  não aparece pra ninguém. Ao **substituir** um documento (migração), o vínculo novo **não herda** as
  habilitações do antigo sozinho — peça pra **herdar** na hora de vincular, ou **habilite** depois.

## Ferramentas (tarefa → ferramenta)
> Ensine a intenção e o _quando_. A **execução depende de autorização** — o MCP aplica permissão;
> a skill nunca promete acesso, só a intenção. Ler é uma coisa; **desenhar/publicar** exige alçada maior.

**Descobrir e ler o design**
- **Ver o catálogo de design** (tipos + vínculos tipo↔template, com status e versão) → ferramenta que
  **lista os templates de design**. É o **ponto de partida** para editar um modelo ou montar um tipo novo.
- **Ler UM modelo** (suas versões e o HTML de uma versão; opcionalmente o vínculo e a estrutura de dados,
  **incluindo os campos de tela**) → ferramenta que **lê o template**.
- **Ver quais variáveis/placeholders** um modelo espera (validar o template × a estrutura de dados)
  → ferramenta que **lista as variáveis** do template.

**Editar conteúdo com segurança**
- **Criar/editar um rascunho** de conteúdo do modelo → ferramenta que **faz upsert do conteúdo**. Sem
  versão informada, cria rascunho novo; com versão, edita o rascunho. **Versão publicada não se edita** —
  crie um rascunho novo. Ela roda em modo **pré-visualização por padrão** (mostra o que faria sem gravar).
- **Previsualizar antes de publicar** → ferramenta que **simula** o modelo com dados fictícios. **Sem
  efeito**. Devolve um **link temporário** do preview (não o arquivo embutido) — **repasse o link ao
  usuário** para ele abrir/baixar. Regra de ouro: **simule sempre antes** de publicar ou ativar.
- **Publicar a versão oficial** → ferramenta que **publica**. Alcance amplo → **exige confirmação humana**.

**Montar o catálogo (tipo novo)**
- **Criar/editar tipo, definir/editar a estrutura de dados, vincular tipo↔template, ativar/desativar** →
  ferramenta que **gerencia o catálogo**. Criar/vincular/definir dados **nascem inativos** (reversível, em
  pré-visualização por padrão). **Ativar** torna o recurso emissível → **exige confirmação**.
- **Definir os campos de digitação** do documento (o que o operador preenche na emissão — ex.: observação
  para o paciente e outra para a empresa) → **edite a estrutura de dados** com os campos no **contrato real**
  (nome, rótulo, tipo, obrigatório, **grupo**, opções) — passe a estrutura **como ela é**, sem inventar
  formato. Ao **ler** o template, os **campos de tela** vêm junto (inspeção). A tela de emissão **já
  renderiza** esses campos — não é preciso mexer no front.
- **Nascer um corpo/bloco novo do zero** (um modelo HTML novo, ou um **bloco reutilizável**) → ferramenta
  que **cria um corpo de template**. É como você começa um documento que **não** tem um parecido para
  copiar — por exemplo, **trazer um documento antigo (DOCX) para o HTML** — ou como você cria um **bloco
  reutilizável** (cabeçalho/rodapé/assinatura/cláusula) para depois **incluí-lo** nos modelos. O corpo
  nasce com um conteúdo inicial em **rascunho** (publique quando estiver pronto). Depois é só **vincular**
  ao tipo (se for um documento) ou **incluí-lo** de outros modelos (se for um bloco).
  > **Clonar × criar do zero:** se **já existe** um modelo parecido, **clone-o** (a cópia é
  > **independente** — editar o clone **não** mexe no original) e ajuste. Só **crie do zero** quando não há
  > de onde clonar (ex.: migração de DOCX). Em ambos, **reaproveite os blocos** que já existirem.
- **Montar/gerir um modelo (bundle)** — o invólucro que junta corpo **digital** + corpo **impresso** +
  estrutura de dados como uma unidade → ferramentas de **modelo** (listar/gerir). Só HTML/DB — **DOCX e
  HTML-em-disco ficam fora**.

**Gerir imagens e estilos do design**
- **Ler o conteúdo de um asset** (a folha de estilo/CSS ou um SVG vigente) **antes de sobrescrevê-lo**
  → ferramenta que **gerencia assets** (ação de **leitura de conteúdo**). É o passo que fecha o ciclo
  **ler → modificar → gravar**: nunca reenvie um asset por cima sem ler o conteúdo atual antes — o envio
  com sobrescrita substitui **às cegas**. Texto (CSS/SVG) vem **à mão** para propor o diff; binário vem
  como **referência**.
- **Listar/enviar/excluir assets** (logos/imagens/estilos) e **ver onde um asset é usado** (antes de
  excluir) → a mesma ferramenta (+ consulta de uso). Excluir um asset **em uso** exige confirmação/forçar
  (o sistema mostra onde ele é referenciado).

**Prontuário gráfico (diagramas anatômicos, #1129)**
- **Navegar a biblioteca de diagramas** — as imagens-base (rosto, corpo, arcada dentária, olho…) sobre
  as quais o profissional desenha os procedimentos no prontuário **gráfico/anotável**, filtrando por
  **especialidade** e vendo os **globais da frota** + os do estabelecimento → ferramenta que **lista
  os diagramas**. Traz só metadados (nome, escopo, dimensões, especialidade), não os bytes da imagem.
- **Montar o tipo de prontuário gráfico** — criar/editar o **tipo de prontuário** cuja tela carrega um
  **widget de diagrama** que referencia um desses diagramas → ferramenta de **gestão de tipo de
  prontuário** (pré-visualiza antes de gravar; o sistema **valida** o widget). Aqui se define o
  **molde**; o **desenho** em si é ato clínico no atendimento (fora do design). Esse mesmo tipo também
  é gerível pelo papel `administrador-clinica`.

**Modelos de sistema (Orçamento e TCLE)**
- **Listar os modelos de sistema** e ver se estão publicados → ferramenta que **lista os templates de
  sistema**. Lembre: eles **não** aparecem no catálogo de design.
- **Ler UM modelo de sistema** (versões e o HTML de uma versão, inclusive a publicada) → ferramenta que
  **lê o template de sistema**. A edição dos modelos de sistema é pela Central.

**Termos do orçamento — o CONTEÚDO (aceite, intercorrências, itens não inclusos, TCLE, outros)**
> Aqui você mexe no **texto legal**, não na fôrma HTML. É a tela **Templates de Termos** (nas configurações da clínica).
- **Listar/buscar os termos** (por tipo, por texto, incluindo inativos ou só os padrão) → ferramenta que
  **lista os templates de termos**. A lista é leve — **sem** o texto; traz código, nome, tipo, versão,
  se é padrão e se está ativo.
- **Ler UM termo** (o **texto** completo, os itens de consentimento, a versão) → a mesma ferramenta,
  informando o **id** do termo. Para o **histórico**, peça as **versões** — vem o texto de cada uma.
- **Ver o termo PADRÃO de um tipo** (o que o orçamento novo já traz) → a mesma ferramenta, pedindo o
  **padrão do tipo**. Se nenhum é padrão, ela diz isso (não inventa).
- **Criar/editar um termo, definir o padrão, desativar/reativar** → ferramenta que **gerencia o termo**.
  Roda em **pré-visualização por padrão** (mostra o que gravaria sem gravar). Ao **criar**, informe
  código + nome + tipo + o **texto** (mínimo de alguns caracteres); opcionalmente os **itens de
  consentimento** e o **tempo mínimo de leitura**. Ao **editar**, lembre: **mudar o texto cria uma versão
  nova** (a anterior fica no histórico). **Definir padrão** troca qual termo daquele tipo o orçamento traz
  por default. **Desativar** é reversível (reativar traz de volta); orçamentos que já usaram o termo
  guardam o snapshot.

**Do lado do paciente (leitura)**
- **Quais modelos um profissional pode emitir** → ferramenta que **lista os templates disponíveis** para
  o profissional.
- **Gerir quem pode emitir um documento** (habilitações) → ferramenta que **lista/habilita/desabilita**
  profissional↔tipo-template: ver quem está habilitado num tipo-template, ver o que um profissional emite,
  e **habilitar/desabilitar** um profissional. É como você diagnostica e corrige quando um documento
  (migrado ou novo) **não aparece** pra quem deveria. Escritas em pré-visualização por padrão.
- **Herdar habilitações ao substituir** (migração) → ao **vincular** um tipo-template que substitui um
  legado, indique o legado para **copiar as habilitações** dele — o documento migrado não some do picker.
- **Quais documentos um paciente (ou um atendimento) já tem** ("a receita foi gerada?") → ferramenta que
  **lista os documentos** por **paciente** ou por **atendimento**. Devolve a lista (nome, tamanho, data,
  tipo) — **sem** link de download nem chave interna do arquivo; abrir/baixar é pela Central.

## Fluxos comuns

### Editar um modelo existente e publicar
1. **Ache o modelo** no catálogo de design (liste os templates → identifique o tipo/vínculo).
2. **Leia** as versões do template e o HTML da versão atual.
3. **Crie um rascunho** com a mudança (upsert de conteúdo, em pré-visualização primeiro; depois grave).
   Se for editar uma versão **publicada**, não dá — **crie um rascunho novo**.
4. **Simule** o rascunho com dados fictícios e **confira o render**.
5. **Publique** a versão (confirmação humana). A partir daí, novas emissões usam o novo modelo;
   documentos já gerados **não** mudam.

### Criar um tipo de documento novo e habilitá-lo
1. **Crie o tipo** (nasce inativo).
2. **Defina a estrutura de dados** (nome + versão) — os campos que o modelo preenche.
3. **Desenhe o conteúdo** do template (rascunho → simule → publique).
4. **Vincule** o tipo ao(s) template(s) — digital e/ou impresso — com a estrutura de dados (nasce inativo).
5. **Simule** para conferir.
6. **Ative** o vínculo (confirmação) — só então o tipo fica emissível na geração real.

### Criar um documento com campos de digitação (ex.: atestado com observação)
1. **Crie o tipo** (atestado) e defina a **estrutura de dados**.
2. **Declare os campos** na estrutura, no contrato real — nome, rótulo, **tipo** (texto/área de texto/
   data/seleção…), obrigatório, e **grupo** (é o grupo que separa *observação do paciente* × *observação
   da empresa*); opções, se for seleção. Passe a estrutura **como ela é**.
3. **Desenhe o conteúdo** do template referenciando os dados do paciente **+** esses campos.
4. **Simule** e **publique**. A **tela de emissão já mostra** os campos para o operador digitar.

### Reaproveitar um bloco (cabeçalho/rodapé/assinatura) em vários documentos
1. **Procure primeiro** se o bloco já existe como **bloco reutilizável** (liste os modelos; blocos são os
   marcados como reutilizáveis). Se existir, **reutilize** — não recrie.
2. Se ainda não existe, **nasça o bloco do zero** marcado como **reutilizável** (conteúdo do bloco →
   rascunho → **simule** → **publique**).
3. Em cada modelo que deve usá-lo, **inclua o bloco** pelo nome no rascunho do modelo (em vez de colar o
   HTML). **Simule** para conferir o render com o bloco incluído e **publique**.
4. Dali em diante, editar/publicar **o bloco** atualiza **todos** os modelos que o incluem — sem tocar em
   cada um.

### Trazer um documento antigo (DOCX) para o editor novo (HTML)
1. **Nasça um corpo novo do zero** (criar corpo de template) — é o ponto de partida quando não há um modelo
   parecido para clonar. (Se houver um parecido, **clone-o** — a cópia é independente.)
2. Traga o conteúdo como **rascunho** e **reaproveite os blocos** que já existirem (cabeçalho/rodapé/
   assinatura) em vez de recriá-los; extraia para **bloco** o que for reaparecer em outros documentos.
3. **Simule**, ajuste, **publique**.
4. **Vincule** ao tipo — e, como você está **substituindo** um documento legado, peça pra **herdar as
   habilitações do legado** (indique o tipo-template antigo que este substitui). Sem isso, o documento
   migrado **some do picker** dos profissionais até você re-habilitar um a um. **Ative** quando estiver
   pronto — só então fica emissível.
5. Se algum profissional ainda ficou de fora (ou o legado não tinha as habilitações certas), **habilite/
   desabilite** direto (gerir habilitações) e confira **quem pode emitir** o tipo-template.

### Trocar um logo/imagem ou ajustar um estilo (CSS) do design
1. Se vai **sobrescrever** um asset existente (ex.: editar a folha de estilo do design system), **leia o
   conteúdo atual primeiro** — texto (CSS/SVG) vem à mão para você propor a mudança sobre ele. **Nunca**
   reenvie por cima às cegas (a sobrescrita substitui o conteúdo vigente sem volta).
2. **Envie** o asset (novo, ou a versão ajustada a partir do que você leu), ou liste os existentes.
3. **Ajuste o rascunho** do template para referenciar o asset, se for o caso.
4. **Simule** e **publique**. Para **excluir** um asset em uso, o sistema **avisa onde** ele aparece —
   só sai com confirmação/forçar.

### Redigir ou atualizar um termo (ex.: o texto do TCLE)
1. **Ache o termo** pelo tipo (ex.: `tcle`) ou pela busca — ou veja o **padrão** do tipo.
2. **Leia** o texto atual (informe o id) — e, se precisar, o **histórico de versões**.
3. **Edite** com a mudança, em **pré-visualização** primeiro; depois grave. **Mudar o texto cria uma
   versão nova** — a anterior fica preservada; documentos já assinados **não** mudam.
4. Se for um termo novo, **crie** (código + nome + tipo + texto; itens de consentimento e tempo de
   leitura se fizer sentido).
5. Se ele deve ser o que o orçamento traz por default, **defina como padrão** do tipo (desmarca o anterior).
6. ⚠️ Não confunda com a **fôrma**: se o que muda é o *layout do papel* (cabeçalho, logo), isso é o
   **template de sistema do TCLE/Orçamento**, não o termo. O **texto** do consentimento é o termo.

### Conferir se o documento de um atendimento saiu
1. **Liste os documentos do atendimento** → veja se a receita/atestado/orçamento está lá (nome, data).
2. Para **abrir/baixar**, vá à Central — o link de arquivo não trafega por aqui.

### Ordem mental para "mudar como um documento fica"
tipo/modelo aplicável → ler a versão atual → **rascunho** com a mudança → **simular** (sempre) →
**publicar** (confirmar) → só novas emissões usam o novo modelo.

## Regras e invariantes
- **Modelo ≠ documento gerado** — editar/publicar um template **não** reescreve documentos já emitidos.
- **Versão publicada não se edita** — para mudar, crie um **rascunho novo** e publique.
- **Publicar e ativar são de alto alcance** — sempre **confirmação humana** e **simulação antes**.
- **Recursos de catálogo nascem inativos** — montar/testar é seguro; só a **ativação** torna emissível.
- **Simulação não tem efeito** — dados fictícios, marca d'água de amostra; nada é gravado ou emitido.
- **Template de sistema (Orçamento/TCLE) é à parte** — global, admin-only, **fora** do catálogo de design.
- **Fôrma ≠ conteúdo do termo** — o **texto** do TCLE/aceite/intercorrências/itens é um **template de
  termo** (a tela **Templates de Termos**); a **fôrma HTML** é o template de sistema. Editar um **não** mexe no outro.
- **Termo: mudar o texto cria versão nova** — a anterior fica no histórico; documento já assinado guarda
  o snapshot. **Um padrão por tipo** — definir outro desmarca o anterior.
- **Reaproveite blocos, não duplique HTML** — cabeçalho/rodapé/assinatura/cláusula que se repete vira um
  **bloco reutilizável** incluído nos modelos; muda **num lugar**, reflete em **todos**. Antes de escrever
  HTML novo, **procure um bloco** que já resolva; se um trecho vai reaparecer, **transforme-o em bloco**.
- **Clonar dá cópia independente** — clonar um modelo copia os corpos como **cópias próprias**; editar o
  clone **não** altera o original. Só **crie do zero** quando não há de onde clonar (ex.: migração de DOCX).
- **Digital e impresso podem ter modelos distintos** para o mesmo tipo.
- **Asset em uso não some por acidente** — exclusão avisa onde é referenciado e exige confirmação/forçar.
- **Leia um asset antes de sobrescrevê-lo** — o envio com sobrescrita substitui às cegas; para editar um
  estilo/CSS ou SVG, leia o conteúdo vigente primeiro e proponha a mudança sobre ele (texto vem à mão,
  binário vem como referência).
- **Leitura de documento do paciente é só listagem** — nunca link de download; abrir é pela Central.
- **Ler ≠ desenhar ≠ publicar** — cada nível exige mais alçada; a execução depende de autorização.

## Limites / o que esta skill NÃO cobre
- **Envio** do documento ao paciente (e-mail/WhatsApp/link) → skill de mensageria/envio.
- **Preço** do orçamento (itens, tabelas, cobertura, condições, aceite) → skill `precificador`.
  Aqui só o **modelo** do orçamento (como ele fica) e o **texto dos termos** (o conteúdo).
- **Escolher qual termo entra num orçamento específico** e o **aceite/assinatura** do paciente →
  `precificador` / plataforma. Aqui você **redige e versiona** os termos (o catálogo de textos), não os
  aplica a um orçamento concreto nem coleta a assinatura.
- **Assinatura eletrônica** e o fluxo do link de assinatura → fora desta skill.
- **Gerar** o documento do paciente e **baixar/abrir** o PDF → pela Central; aqui só se **lista** o que existe.
- Não expõe como os modelos são renderizados/armazenados por dentro — só como **desenhá-los, versioná-los,
  publicá-los e pensá-los**.
