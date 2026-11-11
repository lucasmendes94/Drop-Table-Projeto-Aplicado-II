# Como reproduzir os resultados

## 1. Obter a base

Fonte oficial utilizada pelo projeto:

**Brazilian E-Commerce Public Dataset by Olist — Kaggle**

Baixe o conjunto de dados e coloque o arquivo:

`olist_order_reviews_dataset.csv`

em:

`data/raw/olist_order_reviews_dataset.csv`

Os dados brutos não são versionados no GitHub.

## 2. Criar o ambiente

O experimento da Etapa 3 registrou Python 3.12.14 e as versões das bibliotecas em `requirements-etapa3.txt`.

Instalação:

```text
python -m pip install -r requirements-etapa3.txt
```

## 3. Preparar a base

```text
python -m src.preparacao
```

Saídas locais:

- `data/processed/avaliacoes_preparadas.csv`
- `data/processed/treino.csv`
- `data/processed/teste.csv`
- `data/processed/relatorio_preparacao.json`

## 4. Treinar e avaliar o modelo-base

```text
python -m src.treinamento
```

O script utiliza TF-IDF + Regressão Logística e grava as métricas e previsões no diretório local de dados processados.

## 5. Reproduzir otimização e análise NMF

```text
python -m src.etapa3
```

Evidências versionadas:

- `reports/etapa3/execucao.json`
- `reports/etapa3/comparacao_c.csv`
- `reports/etapa3/validacao_folds.csv`
- `reports/etapa3/comparacao_teste.json`
- `reports/etapa3/topicos_nmf.json`

## 6. Reproduzir os cinco temas de insatisfação

```text
python -m src.temas_insatisfacao
```

Evidências versionadas:

- `reports/etapa3/cinco_temas.csv`
- `reports/etapa3/cinco_temas.json`

## 7. Conferir integridade

Compare os hashes de `treino.csv` e `teste.csv` com os valores registrados em `reports/etapa3/execucao.json`.

Se os hashes coincidirem, os experimentos estão sendo executados sobre os mesmos conjuntos usados nos resultados apresentados.

## Ordem completa

```text
python -m src.preparacao
python -m src.treinamento
python -m src.etapa3
python -m src.temas_insatisfacao
```

O relatório técnico final utiliza somente resultados ligados a essa cadeia de execução e às evidências versionadas.
