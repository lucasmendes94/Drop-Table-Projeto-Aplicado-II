# Drop Table - Projeto Aplicado II

Projeto do 3º semestre do curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

## Tema

Análise de sentimentos e classificação de avaliações de e-commerce utilizando o conjunto de dados público da Olist.

O projeto simula uma necessidade da empresa fictícia **ConectaShop**: compreender padrões de satisfação e insatisfação dos clientes a partir das notas e dos comentários textuais de pedidos.

## Acesso rápido

- [Relatório da Etapa 1 revisado](%5BPA2%5D%20Etapa%201%20-%20Drop%20Table%20-%20V270826-R2.docx)
- [Cronograma completo e editável](Cronograma%20-%20V270826.xlsx)
- [Validação dos comentários do professor](VALIDACAO_COMENTARIOS.md)

Este repositório é público. Os links acima podem ser abertos e baixados sem login no GitHub.

## Objetivo

Aplicar aquisição e preparação de dados, análise exploratória, processamento de linguagem natural e aprendizado de máquina para:

- preparar e documentar avaliações textuais em português;
- analisar a distribuição das notas e os principais termos;
- classificar sentimentos em positivo, neutro e negativo;
- identificar temas recorrentes de insatisfação;
- apresentar métricas, visualizações e recomendações de negócio.

## Fonte dos dados

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Os arquivos brutos do conjunto de dados não são versionados neste repositório. As instruções de obtenção e preparação serão mantidas na documentação e nos notebooks.

## Estrutura

```text
.
|-- data/
|   |-- raw/                 # dados originais locais
|   `-- processed/           # dados tratados locais
|-- docs/
|   `-- rascunhos/           # versões anteriores preservadas
|-- notebooks/               # EDA, preparação, NLP e modelagem
|-- reports/
|   `-- figures/             # gráficos e imagens dos relatórios
|-- src/                     # funções e pipeline reutilizável
|-- Cronograma - V270826.xlsx
|-- [PA2] Etapa 1 - Drop Table - V270826-R2.docx
|-- VALIDACAO_COMENTARIOS.md
|-- requirements.txt
`-- README.md
```

## Equipe

- Igor Eduardo Dallan do Couto - RA 10748144
- Jaqueline de Oliveira Alves - RA 10755023
- Kayo Oliveira Nukui — RA 10356420
- Lucas de Lima Mendes — RA 10756562

## Situação

- [x] Definição do grupo, organização fictícia e área de atuação
- [x] Seleção e descrição inicial do conjunto de dados
- [x] Objetivos, metas e cronograma inicial
- [x] Comentários do professor atendidos no relatório e documentados no repositório
- [ ] Aquisição, qualidade e preparação dos dados
- [ ] Análise exploratória
- [ ] Modelos de classificação e análise de tópicos
- [ ] Relatório, storytelling e apresentação final
