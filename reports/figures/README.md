# Figuras

Esta pasta reúne quatro gráficos em SVG já versionados (`desempenho_modelo.svg`, `distribuicao_sentimentos_resumo.svg`, `otimizacao_c.svg` e `temas_insatisfacao.svg`), derivados dos resultados do projeto.

Três figuras equivalentes em formato PNG (`desempenho_modelo.png`, `otimizacao_c.png` e `temas_insatisfacao.png`) podem ser geradas localmente a partir das evidências em `reports/etapa3/` com:

```text
python -m src.figuras_resultados
```

O script lê diretamente os arquivos de evidência em `reports/etapa3/`, garantindo que os gráficos sejam rastreáveis aos mesmos números utilizados no relatório e na apresentação.
