# Tratamento da base de dados

Responsável: Lucas de Lima Mendes

## Escopo

Esta atividade transforma o arquivo `olist_order_reviews_dataset.csv` em conjuntos adequados para treinar e testar um classificador de sentimentos. O rótulo supervisionado é derivado da nota da avaliação: notas 1 e 2 correspondem à classe negativa, nota 3 à classe neutra e notas 4 e 5 à classe positiva.

## Preparação

O script `src/preparacao.py` executa as seguintes etapas:

1. valida a presença dos campos necessários e mantém somente as colunas utilizadas;
2. converte a nota para valor numérico e descarta valores fora da escala de 1 a 5;
3. combina título e mensagem da avaliação;
4. normaliza caixa, espaços, URLs, e-mails, números e pontuação, preservando acentos e palavras de negação;
5. remove registros sem texto útil;
6. elimina textos com rótulos conflitantes e duplicatas textuais, reduzindo o risco de vazamento;
7. cria os conjuntos de treino e teste por amostragem estratificada, com 80% e 20% dos registros e semente 42.

A remoção de stopwords não é aplicada nesta etapa, pois palavras como “não”, “nem” e “nunca” podem alterar o sentimento expresso. A vetorização é ajustada somente com o conjunto de treino, dentro do pipeline do scikit-learn, para evitar que o vocabulário do teste influencie o modelo.

## Treinamento

O script `src/treinamento.py` usa um pipeline com TF-IDF de unigramas e bigramas e regressão logística multiclasse. O parâmetro `class_weight="balanced"` compensa parcialmente o desequilíbrio entre sentimentos. O conjunto de teste permanece isolado até a avaliação final.

São gravados o modelo treinado, as previsões do teste, a matriz de confusão, a acurácia e precisão, recall e F1-score por classe. O F1-score da classe negativa é destacado porque a meta do projeto exige valor mínimo de 0,80 para essa classe.

## Resultado da validação

Em 8 de setembro de 2026, o pipeline foi executado com o arquivo público de avaliações da Olist. Das 99.224 linhas originais, 34.898 avaliações textuais válidas permaneceram após a limpeza: 21.488 positivas, 10.245 negativas e 3.165 neutras. A divisão produziu 27.918 exemplos de treino e 6.980 de teste, sem sobreposição textual.

O modelo-base obteve acurácia de 80,40%. Para a classe negativa, alcançou precisão de 78,79%, recall de 82,67% e F1-score de 80,69%, atendendo à meta mínima de 0,80 definida para o projeto. O desempenho da classe neutra foi inferior (F1-score de 33,72%), o que indica a necessidade de comparar outros modelos, ajustar hiperparâmetros e investigar a ambiguidade das avaliações de nota 3 nas etapas seguintes.

## Execução

Com o ambiente configurado e o CSV bruto salvo em `data/raw/`, execute a partir da raiz do projeto:

```text
python -m src.preparacao
python -m src.treinamento
```

Os arquivos gerados ficam em `data/processed/` e não são versionados, conforme o arquivo `.gitignore`. O relatório `relatorio_preparacao.json` permite auditar as exclusões e confirmar que não há sobreposição de textos entre treino e teste. O arquivo `metricas_modelo.json` registra o desempenho obtido.

## Reprodutibilidade e prevenção de vazamento

A semente fixa torna a divisão reproduzível. A estratificação mantém aproximadamente a mesma proporção de classes nos dois conjuntos. A remoção de textos duplicados ocorre antes da divisão e o treinamento verifica novamente se existe sobreposição textual entre treino e teste. Todo o ajuste do TF-IDF e do classificador acontece apenas com os dados de treino.
