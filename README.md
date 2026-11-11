# Drop Table — Projeto Aplicado II

Projeto do 3º semestre do curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

## Projeto

**Tema:** análise de sentimentos e de temas de insatisfação em avaliações de e-commerce.

O conjunto de dados utilizado é o **Brazilian E-Commerce Public Dataset by Olist**. O projeto simula uma aplicação para a empresa fictícia **ConectaShop**, transformando avaliações textuais em informações estruturadas para apoio à experiência do cliente e às operações.

## Navegação rápida

### Entrega e documentação

- [Relatório técnico final — versão de trabalho](docs/RELATORIO_FINAL_RASCUNHO.md)
- [Storytelling — versão de trabalho](docs/APRESENTACAO_STORYTELLING_RASCUNHO.md)
- [Rastreabilidade dos resultados](docs/RASTREABILIDADE_RESULTADOS.md)
- [Como reproduzir os resultados](docs/REPRODUCAO.md)
- [Tratamento da base](docs/TRATAMENTO_BASE_DADOS.md)
- [Método analítico](docs/METODO_ANALITICO.md)
- [Resultados preliminares e produto](docs/RESULTADOS_PRELIMINARES.md)
- [Análise de temas e otimização](docs/ETAPA3_TEMAS_E_OTIMIZACAO.md)

### Evidências de execução

- [Manifesto da execução](reports/etapa3/execucao.json)
- [Métricas no teste](reports/etapa3/comparacao_teste.json)
- [Comparação dos valores de C](reports/etapa3/comparacao_c.csv)
- [Resultados dos 45 ajustes de validação cruzada](reports/etapa3/validacao_folds.csv)
- [Tópicos NMF](reports/etapa3/topicos_nmf.json)
- [Cinco temas de insatisfação](reports/etapa3/cinco_temas.json)

### Produto

- [Protótipo — Painel de Voz do Cliente](produto/painel_voz_cliente.html)

### Histórico

- [Relatório revisado da Etapa 1](%5BPA2%5D%20Etapa%201%20-%20Drop%20Table%20-%20V280826.pdf)
- [Validação dos comentários do professor](VALIDACAO_COMENTARIOS.md)
- [Cronograma mais recente](Cronograma%20-%20V191026.xlsx)

## Resultados principais

O pipeline tratado e avaliado apresentou:

- **34.898** avaliações textuais válidas;
- **27.918** registros de treino;
- **6.980** registros de teste;
- **80,40%** de acurácia;
- **80,69%** de F1 para a classe negativa;
- **82,67%** de recall para a classe negativa;
- melhor valor de regularização **C = 1** na grade avaliada.

Na exploração das 8.196 avaliações negativas de treino, atraso ou não recebimento foi o tema mais frequente entre as cinco categorias definidas, com **2.700 menções (32,94%)**.

Cada número acima está ligado a código e evidência em [Rastreabilidade dos resultados](docs/RASTREABILIDADE_RESULTADOS.md).

## Estrutura do repositório

```text
.
├── data/
│   ├── raw/                 # instruções; dados brutos não versionados
│   └── processed/           # instruções; artefatos locais não versionados
├── docs/                    # documentação técnica e relatórios
├── produto/                 # protótipo analítico
├── reports/
│   ├── etapa3/              # evidências de execução versionadas
│   └── figures/             # figuras derivadas dos resultados
├── src/                     # código reproduzível
├── requirements-etapa3.txt  # versões usadas nos experimentos da Etapa 3
└── README.md
```

## Reprodução

1. Baixe o conjunto público da Olist a partir do Kaggle.
2. Coloque `olist_order_reviews_dataset.csv` em `data/raw/`.
3. Instale as dependências.
4. Execute a sequência:

```text
python -m pip install -r requirements-etapa3.txt
python -m src.preparacao
python -m src.treinamento
python -m src.etapa3
python -m src.temas_insatisfacao
python -m src.figuras_resultados
```

Detalhes, saídas esperadas e conferência de hashes estão em [Como reproduzir os resultados](docs/REPRODUCAO.md).

## Integridade e reprodutibilidade

A execução versionada registra:

- Python **3.12.14**;
- scikit-learn **1.9.1**;
- NumPy **2.5.4**;
- pandas **3.1.0**;
- semente aleatória **42**;
- hashes SHA-256 dos arquivos de treino e teste usados nos experimentos.

Essas informações estão em `reports/etapa3/execucao.json`.

## Equipe

- Igor Eduardo Dallan do Couto — RA 10748144
- Jaqueline de Oliveira Alves — RA 10755023
- Kayo Oliveira Nukui — RA 10356420
- Lucas de Lima Mendes — RA 10756562
