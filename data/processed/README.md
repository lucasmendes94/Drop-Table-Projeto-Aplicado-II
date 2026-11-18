# Dados processados

Esta pasta armazena os dados e artefatos produzidos pelos módulos `src.preparacao` e `src.treinamento`:

- `avaliacoes_preparadas.csv`: base limpa e rotulada;
- `treino.csv` e `teste.csv`: partição estratificada;
- `relatorio_preparacao.json`: contagens e verificações da preparação;
- `modelo/modelo_sentimento.joblib`: pipeline TF-IDF e regressão logística;
- `modelo/metricas_modelo.json`: métricas no conjunto de teste;
- `modelo/previsoes_teste.csv`: rótulos reais e previstos.

Esses oito artefatos fazem parte da entrega e são versionados por exceção explícita no `.gitignore`. Novos arquivos fora dessa lista permanecem ignorados.
