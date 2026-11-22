# Drop Table — Projeto Aplicado II

Projeto do 3º semestre do curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

## Projeto

**Tema:** análise de sentimentos e de temas de insatisfação em avaliações de e-commerce.

O conjunto de dados utilizado é o **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** (arquivo `olist_order_reviews_dataset.csv`). O projeto simula uma aplicação para a empresa fictícia **ConectaShop**, transformando avaliações textuais em informações estruturadas para apoio à experiência do cliente e às operações.

## Navegação rápida

### Entrega e documentação

- [Relatório técnico final](docs/RELATORIO_TECNICO_FINAL.md)
- [Apresentação do storytelling](docs/APRESENTACAO_STORYTELLING.md)
- [Rastreabilidade dos resultados](docs/RASTREABILIDADE_RESULTADOS.md)
- [Como reproduzir os resultados](docs/REPRODUCAO.md)
- [Tratamento da base](docs/TRATAMENTO_BASE_DADOS.md)
- [Guia dos notebooks de análise](notebooks/README.md)
- [Método analítico](docs/METODO_ANALITICO.md)
- [Resultados preliminares e produto](docs/RESULTADOS_PRELIMINARES.md)
- [Análise de temas e otimização](docs/ETAPA3_TEMAS_E_OTIMIZACAO.md)
- [Análise de erros da classe neutra](docs/ANALISE_ERROS_CLASSE_NEUTRA.md)
- [Painel Operacional de CX](docs/PAINEL_OPERACIONAL_CX.md)

### Evidências de execução

- [Manifesto da execução](reports/etapa3/execucao.json)
- [Métricas no teste](reports/etapa3/comparacao_teste.json)
- [Comparação dos valores de C](reports/etapa3/comparacao_c.csv)
- [Resultados dos 45 ajustes de validação cruzada](reports/etapa3/validacao_folds.csv)
- [Tópicos NMF](reports/etapa3/topicos_nmf.json)
- [Cinco temas de insatisfação](reports/etapa3/cinco_temas.json)

### Produto

- [Painel de Voz do Cliente (métricas históricas e triagem ao vivo)](produto/painel_voz_cliente.html)

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
│   ├── raw/                 # base bruta Olist versionada por exceção no .gitignore
│   └── processed/           # bases tratadas, modelo e métricas versionados
├── docs/                    # documentação técnica e relatórios
├── notebooks/               # notebooks Jupyter (01 a 05) e guia de execução
├── produto/                 # protótipo analítico
├── reports/
│   ├── etapa3/              # evidências de execução versionadas
│   └── figures/             # 4 SVGs versionados e saída PNG do script de figuras
├── src/                     # código reproduzível (preparação, treino, análise e API)
├── tests/                   # testes de integração da API de triagem e do painel
├── requirements.txt         # dependências gerais e notebooks
├── requirements-etapa3.txt  # versões usadas nos experimentos da Etapa 3 (+ matplotlib)
└── README.md
```

## Reprodução

1. O arquivo `data/raw/olist_order_reviews_dataset.csv` (fonte oficial: [Kaggle Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)) já acompanha este repositório por exceção explícita no `.gitignore`.
2. Instale as dependências.
3. Execute a sequência a partir da raiz do projeto:

```text
python -m pip install -r requirements-etapa3.txt
python -m src.preparacao
python -m src.treinamento
python -m src.etapa3
python -m src.temas_insatisfacao
python -m src.figuras_resultados
```

Detalhes, saídas esperadas e conferência de hashes estão em [Como reproduzir os resultados](docs/REPRODUCAO.md).

## Demonstração local: API de triagem e painel (Etapa 4)

O painel original já exibia os indicadores históricos do classificador e os cinco temas exploratórios de insatisfação. Na Etapa 4, foi integrado a ele um formulário para triagem de novas avaliações em tempo real via API local.

O serviço em `src/api_triagem.py` usa `http.server.ThreadingHTTPServer` (biblioteca padrão do Python) e as dependências já listadas em `requirements-etapa3.txt` (`joblib`, `scikit-learn`, `pandas`, `numpy`, `scipy`). Na inicialização, o servidor carrega `data/processed/modelo/modelo_sentimento.joblib` uma única vez na memória. Cada requisição `POST /triagem` recebe um JSON com `texto`, valida a entrada, aplica `normalizar_texto` de `src/preparacao.py` e devolve `sentimento` (`negativo`, `neutro` ou `positivo`) e `encaminhar_para_revisao` (`true` quando a previsão é `negativo`). O histórico exibido no painel vale apenas para a sessão aberta no navegador; o MVP não armazena avaliações de forma permanente, não executa monitoramento automático nem se integra à base da Olist em tempo real.

### Iniciar o serviço e rodar os testes locais

Para executar o projeto completo, incluindo a suíte de testes da API, instale as dependências gerais:

```text
python -m pip install -r requirements.txt
python -m src.api_triagem
```

- Painel de Voz do Cliente: `http://127.0.0.1:8000/`
- Endpoint de triagem: `POST http://127.0.0.1:8000/triagem`
- Testes de integração locais: `python -m pytest -v tests/test_api_triagem.py`

### Exemplo de requisição

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/triagem" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"texto": "Produto chegou atrasado e com defeito na embalagem."}'
```

Resposta esperada (`200 OK`):

```json
{
  "sentimento": "negativo",
  "encaminhar_para_revisao": true
}
```

### Roteiro curto de demonstração ao vivo

1. Execute `python -m src.api_triagem` na raiz do repositório e abra `http://127.0.0.1:8000/` no navegador.
2. Mostre os indicadores históricos no topo do painel (acurácia de 80,40%, F1 negativo de 80,69% e F1 neutro de 33,72%) e as barras dos cinco temas de insatisfação.
3. No formulário *Triagem de avaliação em tempo real*, envie `"Produto chegou atrasado e com defeito."` para mostrar o retorno `sentimento: "negativo"` e `encaminhar_para_revisao: true`.
4. Envie `"Entrega rápida, produto excelente!"` (`encaminhar_para_revisao: false`) e depois envie `"!!!"` ou o campo vazio para mostrar a validação retornando erro (`HTTP 400`) sem interromper o serviço.
5. Abra [Análise de erros da classe neutra](docs/ANALISE_ERROS_CLASSE_NEUTRA.md) e apresente o caso `f29bbead1034936360ff92f70abbe8f6` (nota 2, `"Produto demorou muito para chegar"`), previsto como `neutro`. Explique que a classe de referência neutra vem da nota 3, que nota e comentário podem divergir e que uma previsão neutra pode deixar uma reclamação sem alerta automático no MVP.

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


## Como validar o projeto

O projeto pode ser validado localmente a partir do conteúdo disponível neste repositório.

### 1. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 2. Executar os testes automatizados

```bash
python -m pytest -v tests/test_api_triagem.py
```

A execução deve validar a disponibilidade da API, o carregamento do painel, classificações positivas, negativas e neutras, além do tratamento de entradas inválidas.

### 3. Iniciar a API e o Painel Operacional de CX

```bash
python -m src.api_triagem
```

Com o servidor iniciado, acesse:

```text
http://127.0.0.1:8000/
```

### 4. Validar o endpoint de saúde

Com o servidor em execução, acesse:

```text
http://127.0.0.1:8000/health
```

O retorno esperado é:

```json
{"status":"ok"}
```

### Reprodução completa

Os procedimentos para reprodução das etapas de preparação, treinamento, avaliação e análise dos resultados estão documentados em [`docs/REPRODUCAO.md`](docs/REPRODUCAO.md).

A relação entre os principais resultados, os códigos que os produziram e os respectivos arquivos de evidência está disponível em [`docs/RASTREABILIDADE_RESULTADOS.md`](docs/RASTREABILIDADE_RESULTADOS.md).
