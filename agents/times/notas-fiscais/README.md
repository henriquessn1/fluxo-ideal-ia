# notas-fiscais — emissão automática da NFS-e (nota de serviço)

Time de **4 agentes `script`** que cuida da nota fiscal de serviço do pagamento até o e-mail. Ele
segue a regra de mercado:
- a nota é do **serviço feito**, com a data do atendimento;
- sai no nome de **quem pagou**;
- **nunca passa do que foi pago**.

As decisões ficam em **tabelas de regras** que a própria clínica edita. Nenhuma regra está no
código.

> **Padrão seguro:** depois de instalado, **nenhuma nota vai sozinha ao governo**. Toda nota fechada
> cai em **Revisar** até a clínica escrever, na tabela do Confirmador, uma regra que transmita direto.

## Os agentes

| Agente | Quando acorda | O que faz |
|---|---|---|
| **Registrador de notas** | a cada pagamento recebido, parcela paga, estorno ou troca de quem pagou | decide pela tabela se nasce a **nota prevista** (o saldo de quem pagou) e mantém esse saldo em dia |
| **Confirmador de notas** | quando um serviço é feito ou cancelado, e todo dia às **00:10** | o serviço feito vira **nota em formação** (por venda + quem pagou + dia ou mês); no fechamento, a tabela decide entre **Revisar** e **transmitir ao governo** |
| **Enviador de notas** | quando a nota é autorizada, com repescagem a cada 15 min | decide pela tabela se **envia a nota por e-mail** a quem pagou (o mesmo envio do botão da tela) |
| **Vigia de notas previstas** | **na hora** em que o governo recusa uma nota ou a transmissão para, e dias úteis às 8h | avisa a equipe no sino da Central: a recusa ou falha no minuto em que acontece, e um resumo diário das recusadas, com falha, paradas em Revisar e previstas paradas |

Regras que o sistema garante, independentemente das tabelas:
- Nota com **pendência** sempre vai para Revisar. São pendências: valor a revisar, saldo
  insuficiente e atendimento cancelado.
- Um **estorno** depois da nota autorizada vira pendência para uma pessoa resolver (cancelar ou
  substituir). O agente **nunca cancela** uma nota.
- Produtos e multas não viram NFS-e.

## Tabelas de regras (editáveis na Central, valem na hora em que são salvas)

Cada tabela é lida de cima para baixo: a primeira linha que bate decide. A última linha é
"qualquer outro caso".

| Tabela | Colunas que a clínica pode usar | Padrão |
|---|---|---|
| `regras_registro` (Registrador) | formas de pagamento, valor pago, profissional, procedimento, quem pagou (paciente/outra pessoa), tem CPF/CNPJ, particular/convênio, pagamentos cobrem a venda | **sempre gera a prevista** |
| `regras_confirmacao` (Confirmador) | valor da nota, formas de pagamento, profissional, procedimento, tem CPF/CNPJ, mais de um pagador, pago em mês diferente do serviço, atendimento cancelado, tem pendência | **sempre Revisar** |
| `regras_envio` (Enviador) | como a nota nasceu (agentes/venda/manual), quem pagou tem e-mail, valor | **envia se tem e-mail** |

Outros ajustes:
- `agrupar_por`: `dia` (padrão) ou `mes`, a nota por dia de atendimento ou por mês.
- Vigia: `avisar_na_hora` (`true`), `alvo_papel` (`administrador`), `dias_revisao_parada` (`2`) e `dias_parada` (`15`).
  `alvo_papel` aceita um ou mais papéis da equipe separados por vírgula (ex.: `administrador,financeiro`); cada papel
  recebe o mesmo aviso no sino da Central. Na Central, a variável abre um seletor de papéis.
- `esperar_antes` (`false`) e `esperar_minutos` (`30`) do Enviador, para dar tempo de revisar antes do e-mail.

Exemplo de regra do Confirmador para transmitir direto, a combinar com o contador da clínica:
*"Pix ou cartão, até R$ 500, com CPF, um só pagador → Transmitir ao governo"*, e o resto em Revisar.

## O que este time pede (permissões)

| Papel | Grants | Para quê |
|---|---|---|
| `botfn-nfse-registrador` | `nota_fiscal:registrar_prevista`, `nota_fiscal:read`, `pagador:read`, `venda:read` | criar e manter a nota prevista a partir dos pagamentos |
| `botfn-nfse-confirmador` | `nota_fiscal:emitir_automatico`, `nota_fiscal:read`, `venda:read` | formar e fechar a nota (Revisar ou transmitir) |
| `botfn-nfse-enviador` | `nota_fiscal:enviar_automatico`, `nota_fiscal:read` | enviar a nota autorizada por e-mail a quem pagou |
| `botfn-nfse-vigia` | `nota_fiscal:read`, `notificacao:enviar` | avisar a equipe (recusas na hora e resumo diário) |

## Capabilities usadas

`vendas.listar_pagadores`, `vendas.buscar_venda`, `financeiro.registrar_prevista`,
`financeiro.pagamento_atualizado`, `financeiro.pagamento_estornado`, `financeiro.situacao_venda`,
`financeiro.item_executado`, `financeiro.notas_para_fechar`, `financeiro.fechar_nota`,
`financeiro.listar_notas`, `financeiro.envio_info`, `financeiro.enviar_nota`,
`notificacao.notificar_grupo`.

O endereço real de cada uma é resolvido em privado na instalação.

## Risco: **alto**

- 🧾 **Pode emitir documento fiscal sozinho**, mas só se a clínica escrever uma regra de
  "transmitir" no Confirmador. No padrão, tudo passa por uma pessoa em Revisar.
- ✉️ **Envia e-mail para fora**: a nota vai a quem pagou, que pode não ser o paciente.
- 👁️ **Lê dados de quem pagou** (nome, documento, e-mail) para montar a nota. Os agentes não
  devolvem documento no resultado nem no log.
- ⏰ Age sozinho, nos eventos de pagamento, de serviço e de nota recusada, e nos horários agendados.

## Antes de instalar

1. **Configuração fiscal completa e conferida pelo contador**, em Mesa de Notas → Configuração
   fiscal: códigos do serviço, carga aproximada de tributos, dados da reforma tributária (IBS/CBS).
   Também o **momento da nota**: "na execução" (padrão) ou "no recebimento", conforme o município.
2. Emissor de NFS-e da clínica habilitado: certificado digital A1 e emissor autorizado no
   município.
3. Ligue **"Emissão automática pelos agentes"** na Configuração fiscal. Com ela ligada, a emissão
   antiga na venda quitada para, e as duas não emitem a mesma venda.

## Instalação (Central → Inteligência Artificial → Importar)

1. Cole o link deste `manifest.json` na tela de importar e confira o cartão de risco.
2. Conceda os grants acima aos service-accounts do time.
3. Abra cada agente e ajuste as tabelas de regras com o contador. Em especial a do Confirmador,
   que decide o que vai direto ao governo.

> Reimportar uma versão nova do time **mantém as tabelas e os ajustes** que a clínica já fez.
