# Como reproduzir os resultados

## 1. Obter a base

Fonte oficial utilizada pelo projeto:

**Brazilian E-Commerce Public Dataset by Olist (Kaggle)** (`https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`)

O arquivo `data/raw/olist_order_reviews_dataset.csv` já acompanha o repositório por exceção explícita no `.gitignore`. Caso deseje baixá-lo novamente, salve-o no mesmo caminho.

## 2. Criar o ambiente

Para reproduzir exatamente o ambiente dos experimentos da Etapa 3, use `requirements-etapa3.txt`, que registra as versões das bibliotecas utilizadas junto com Python 3.12.14:

```text
python -m pip install -r requirements-etapa3.txt
```

Para executar também os notebooks e a suíte de testes da API, instale as dependências gerais do projeto:

```text
python -m pip install -r requirements.txt
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

## 7. Gerar figuras em PNG

```text
python -m src.figuras_resultados
```

O script lê as evidências em `reports/etapa3/` e gera três arquivos PNG em `reports/figures/` (`desempenho_modelo.png`, `otimizacao_c.png` e `temas_insatisfacao.png`). Os quatro arquivos SVG já presentes em `reports/figures/` (`desempenho_modelo.svg`, `distribuicao_sentimentos_resumo.svg`, `otimizacao_c.svg` e `temas_insatisfacao.svg`) são versões pré-geradas e versionadas no repositório.

## 8. Conferir integridade

Compare os hashes de `treino.csv` e `teste.csv` com os valores registrados em `reports/etapa3/execucao.json`.

Se os hashes coincidirem, os experimentos estão sendo executados sobre os mesmos conjuntos usados nos resultados apresentados.

## Ordem completa

```text
python -m src.preparacao
python -m src.treinamento
python -m src.etapa3
python -m src.temas_insatisfacao
python -m src.figuras_resultados
```

O relatório técnico final utiliza somente resultados ligados a essa cadeia de execução e às evidências versionadas.

## 9. Executar a API de triagem e os testes locais (Etapa 4)

Após gerar ou manter os artefatos em `data/processed/modelo/`, inicie o serviço local que expõe `POST /triagem` e serve `produto/painel_voz_cliente.html`:

```text
python -m src.api_triagem
```

O painel fica acessível em `http://127.0.0.1:8000/`. Para executar a suíte de testes de integração da API e do painel, com `requirements.txt` instalado:

```text
python -m pytest -v tests/test_api_triagem.py
```

Os testes cobrem a rota `/health`, o carregamento do painel, classificações positivas e negativas, requisições sucessivas e entradas inválidas.

O exemplo de requisição e o roteiro de demonstração ao vivo estão no `README.md` principal.
