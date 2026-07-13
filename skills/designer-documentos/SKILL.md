---
name: designer-documentos
description: O sistema de documentos do Fluxo Ideal — como se desenha, versiona, previsualiza e publica o MODELO de um documento (receita, atestado, laudo, orçamento, TCLE…) e como esses modelos viram documentos gerados por paciente. Use para entender "como esse documento fica" e para criar/editar/publicar um template com segurança.
audience: [ia, humano]
depends_on: [documentos-clinicos, templates, catalogo-documentos]
version: 0.2.1
updated: 2026-07-12
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

Quatro ideias sustentam tudo:

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
  **sem efeito** (não grava nada, não emite nada). É a rede de segurança antes de publicar/ativar.

**Assets**
- **Asset**: imagem/logo usada no design (ex.: logo no cabeçalho). Um asset em uso não some sem confirmação
  explícita (o sistema avisa onde ele é referenciado).

**Modelos de sistema**
- **Orçamento** e **TCLE**: os dois modelos **globais** (admin-only) que fogem do catálogo de design.
  Versionados e publicáveis, mas com caminho próprio.

**Documentos gerados**
- **Documento do paciente**: o arquivo que saiu de uma emissão real (receita/atestado/laudo/orçamento/
  TCLE…), guardado no **atendimento**. A leitura aqui lista **quais** existem (nome, tamanho, data, tipo)
  — sem baixar o arquivo.
- **Modelos habilitados por profissional**: dentre os tipos ativos, quais **este** profissional pode emitir.

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
  efeito**. Regra de ouro: **simule sempre antes** de publicar ou ativar.
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
- **Montar/gerir um modelo (bundle)** — o invólucro que junta corpo **digital** + corpo **impresso** +
  estrutura de dados como uma unidade → ferramentas de **modelo** (listar/gerir). Só HTML/DB — **DOCX e
  HTML-em-disco ficam fora**.

**Gerir imagens do design**
- **Listar/enviar/excluir assets** (logos/imagens) e **ver onde um asset é usado** (antes de excluir)
  → ferramenta que **gerencia assets** (+ consulta de uso). Excluir um asset **em uso** exige
  confirmação/forçar (o sistema mostra onde ele é referenciado).

**Modelos de sistema (Orçamento e TCLE)**
- **Listar os modelos de sistema** e ver se estão publicados → ferramenta que **lista os templates de
  sistema**. Lembre: eles **não** aparecem no catálogo de design.
- **Ler UM modelo de sistema** (versões e o HTML de uma versão, inclusive a publicada) → ferramenta que
  **lê o template de sistema**. A edição dos modelos de sistema é pela Central.

**Do lado do paciente (leitura)**
- **Quais modelos um profissional pode emitir** → ferramenta que **lista os templates disponíveis** para
  o profissional.
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

### Trocar um logo/imagem do design
1. **Envie** o asset novo (ou liste os existentes).
2. **Ajuste o rascunho** do template para referenciar o asset.
3. **Simule** e **publique**. Para **excluir** um asset em uso, o sistema **avisa onde** ele aparece —
   só sai com confirmação/forçar.

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
- **Digital e impresso podem ter modelos distintos** para o mesmo tipo.
- **Asset em uso não some por acidente** — exclusão avisa onde é referenciado e exige confirmação/forçar.
- **Leitura de documento do paciente é só listagem** — nunca link de download; abrir é pela Central.
- **Ler ≠ desenhar ≠ publicar** — cada nível exige mais alçada; a execução depende de autorização.

## Limites / o que esta skill NÃO cobre
- **Envio** do documento ao paciente (e-mail/WhatsApp/link) → skill de mensageria/envio.
- **Preço** do orçamento (itens, tabelas, cobertura, condições, aceite) → skill `precificador`.
  Aqui só o **modelo** do orçamento (como ele fica).
- **Assinatura eletrônica** e o fluxo do link de assinatura → fora desta skill.
- **Gerar** o documento do paciente e **baixar/abrir** o PDF → pela Central; aqui só se **lista** o que existe.
- Não expõe como os modelos são renderizados/armazenados por dentro — só como **desenhá-los, versioná-los,
  publicá-los e pensá-los**.
