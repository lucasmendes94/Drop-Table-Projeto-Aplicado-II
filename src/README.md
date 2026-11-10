# Código-fonte

- `preparacao.py`: valida, limpa e rotula as avaliações; remove duplicidade e cria conjuntos estratificados de treino e teste.
- `treinamento.py`: ajusta o baseline TF-IDF com regressão logística, avalia o teste e salva modelo, previsões e métricas.
- `etapa3.py`: executa exploração NMF e busca do hiperparâmetro C por validação cruzada.
- `temas_insatisfacao.py`: identifica cinco temas exploratórios de insatisfação por regras lexicais multirrótulo.
- `etapa3_validacao.py`: realiza auditoria de pedidos compartilhados, divisão agrupada por `order_id`, validação cruzada agrupada, calibração e estudo de limiares.
- `eda_final.py`: gera as figuras e o resumo da análise exploratória final.
- `finalizar_analise.py`: executa EDA final e validação operacional em sequência.

## Execução principal

Com o CSV bruto disponível em `data/raw/`:

```text
python -m src.preparacao
python -m src.treinamento
python -m src.etapa3
python -m src.temas_insatisfacao
python -m src.finalizar_analise
```

Para executar apenas as análises finais, quando `treino.csv` e `teste.csv` já existirem:

```text
python -m src.finalizar_analise
```

O detalhamento das decisões está na pasta [`docs/`](../docs/).
