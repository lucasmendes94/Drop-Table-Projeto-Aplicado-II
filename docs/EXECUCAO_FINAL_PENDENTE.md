# Execução final pendente

Os códigos necessários já estão no repositório. A única etapa técnica que ainda precisa ser executada no ambiente que possui os arquivos processados é:

```text
python -m src.finalizar_analise
```

## Pré-requisitos

Devem existir localmente:

- `data/processed/treino.csv`;
- `data/processed/teste.csv`.

Esses arquivos são gerados por:

```text
python -m src.preparacao
```

## O comando final executa

1. `src.eda_final`
2. `src.etapa3_validacao`

## Arquivos esperados

### EDA

Em `reports/figures/`:

- `distribuicao_notas.png`;
- `distribuicao_sentimentos.png`;
- `comprimento_comentarios.png`;
- `top_termos_negativo.png`;
- `top_termos_neutro.png`;
- `top_termos_positivo.png`;
- `eda_resumo.json`.

### Validação operacional

Em `reports/etapa3/validacao_operacional/`:

- `validacao_operacional.json`;
- `limiares_validacao.csv`;
- `limiares_teste.csv`;
- tabelas de confiabilidade;
- `confiabilidade_teste.png`;
- `limiares_validacao.png`.

## Depois da execução

Somente os resultados e figuras reproduzíveis devem ser versionados. Os CSVs individuais de treino e teste permanecem fora do GitHub.

As métricas de `validacao_operacional.json` devem substituir o bloco pendente na seção 10 do relatório e no slide 9 da apresentação.
