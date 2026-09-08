# Código-fonte

- `preparacao.py`: valida, limpa e rotula as avaliações; remove duplicidade e cria conjuntos estratificados de treino e teste.
- `treinamento.py`: ajusta o baseline TF-IDF com regressão logística, avalia o teste e salva modelo, previsões e métricas.

Execução a partir da raiz do projeto:

```text
python -m src.preparacao
python -m src.treinamento
```

O detalhamento das decisões está em [`docs/TRATAMENTO_BASE_DADOS.md`](../docs/TRATAMENTO_BASE_DADOS.md).
