# Drop Table - Projeto Aplicado II

Projeto do 3º semestre do curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

## Tema

Análise de sentimentos e classificação de avaliações de e-commerce utilizando o conjunto de dados público da Olist.

O projeto simula uma necessidade da empresa fictícia **ConectaShop**: compreender padrões de satisfação e insatisfação dos clientes a partir das notas e dos comentários textuais de pedidos.

## Acesso rápido

- [Relatório da Etapa 1 revisado](%5BPA2%5D%20Etapa%201%20-%20Drop%20Table%20-%20V280826.docx)
- [Cronograma mais recente](Cronograma%20-%20V191026.xlsx)
- [Validação dos comentários do professor](VALIDACAO_COMENTARIOS.md)
- [Tratamento da base de dados](docs/TRATAMENTO_BASE_DADOS.md)
- [Etapa 3 — entrega consolidada](docs/ETAPA3_ENTREGA.md)
- [Método analítico aplicado](docs/METODO_ANALITICO.md)
- [Análise exploratória final](docs/EDA_FINAL.md)
- [Resultados preliminares e produto analítico](docs/RESULTADOS_PRELIMINARES.md)
- [Protótipo — Painel de Voz do Cliente](produto/painel_voz_cliente.html)
- [Modelo de negócios](docs/MODELO_NEGOCIO.md)
- [Esboço do storytelling](docs/STORYTELLING.md)
- [Rascunho do relatório técnico final](docs/RELATORIO_FINAL_RASCUNHO.md)
- [Rascunho da apresentação final](docs/APRESENTACAO_STORYTELLING_RASCUNHO.md)
- [Execução técnica final pendente](docs/EXECUCAO_FINAL_PENDENTE.md)
- [Etapa 3 — cinco temas e otimização de C (Lucas)](docs/ETAPA3_TEMAS_E_OTIMIZACAO.md)
- [Evidências dos experimentos da Etapa 3](reports/etapa3/)
- [Relatório Etapa 1 em PDF](%5BPA2%5D%20Etapa%201%20-%20Drop%20Table%20-%20V280826.pdf)

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
|-- src/                     # preparação e treinamento reproduzíveis
|-- Cronograma - V191026.xlsx
|-- [PA2] Etapa 1 - Drop Table - V280826.docx
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
- [x] Pipeline de preparação e treinamento da base implementado e validado
- [x] Preparação e tratamento da base
- [x] Modelo-base de classificação de sentimentos aplicado
- [x] Métricas de avaliação calculadas
- [x] Etapa 3 (Lucas): cinco temas recorrentes, com evidências e limitações
- [x] Etapa 3 (Lucas): busca de C por validação cruzada; selecionado C = 1
- [x] Etapa 3: resultados preliminares, produto analítico e rascunho de modelo de negócios
- [x] Etapa 3: esboço do storytelling
- [ ] Validação adicional agrupada por pedido (recomendação metodológica)
- [ ] Consolidação da análise exploratória em gráficos finais
- [ ] Relatório técnico final
- [ ] Apresentação final do storytelling
- [ ] Vídeo de apresentação no YouTube


## Execução das análises finais

Depois de preparar os dados localmente, a EDA final e a validação operacional agrupada por pedido podem ser executadas em sequência:

```text
python -m src.finalizar_analise
```

O comando gera as figuras em `reports/figures/` e os resultados da validação em `reports/etapa3/validacao_operacional/`. Os CSVs processados permanecem fora do GitHub.
