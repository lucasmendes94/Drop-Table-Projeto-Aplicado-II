# Drop Table - Projeto Aplicado II

Projeto do 3º semestre do curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

## Tema

Análise de sentimentos e classificação de avaliações de e-commerce utilizando o conjunto de dados público da Olist.

O projeto simula uma necessidade da empresa fictícia **ConectaShop**: compreender padrões de satisfação e insatisfação dos clientes a partir das notas e dos comentários textuais de pedidos.

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
|-- [PA2] Etapa 1 - Drop Table - V270826.docx
|-- requirements.txt
`-- README.md
```

## Equipe

- Igor Eduardo Dallan do Couto
- Jaqueline de Oliveira Alves
- Kayo Oliveira Nukui
- Lucas de Lima Mendes

## Situação

- [x] Definição do grupo, organização fictícia e área de atuação
- [x] Seleção e descrição inicial do conjunto de dados
- [x] Objetivos, metas e cronograma inicial
- [ ] Aquisição, qualidade e preparação dos dados
- [ ] Análise exploratória
- [ ] Modelos de classificação e análise de tópicos
- [ ] Relatório, storytelling e apresentação final
