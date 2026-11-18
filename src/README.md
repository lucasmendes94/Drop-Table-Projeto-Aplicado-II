# Código-fonte

## Cadeia usada nos resultados do relatório

- `preparacao.py`: valida, limpa e rotula as avaliações; remove duplicidades e cria treino e teste. Importado pelo notebook `02_preparacao_textual.ipynb`.
- `treinamento.py`: treina o baseline TF-IDF + Regressão Logística e calcula métricas. Importado pelo notebook `03_modelos_classificacao.ipynb`.
- `etapa3.py`: executa NMF exploratória e a busca do parâmetro C por validação cruzada.
- `temas_insatisfacao.py`: aplica as cinco regras temáticas às avaliações negativas do treino.
- `figuras_resultados.py`: transforma as evidências versionadas em três gráficos PNG (`desempenho_modelo.png`, `otimizacao_c.png`, `temas_insatisfacao.png`).
- `api_triagem.py`: carrega `data/processed/modelo/modelo_sentimento.joblib` uma vez na inicialização, expõe `POST /triagem` e serve `produto/painel_voz_cliente.html` no mesmo endereço local.

Execução:

```text
python -m src.preparacao
python -m src.treinamento
python -m src.etapa3
python -m src.temas_insatisfacao
python -m src.figuras_resultados
```

A relação entre números, código e evidências está em [`docs/RASTREABILIDADE_RESULTADOS.md`](../docs/RASTREABILIDADE_RESULTADOS.md).

## Outros arquivos

`etapa3_validacao.py` contém um experimento adicional de validação operacional. Seus resultados não são utilizados no relatório final enquanto não houver evidência de execução versionada.
