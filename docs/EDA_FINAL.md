# Análise exploratória final

## Objetivo

Esta etapa consolida a análise exploratória que será utilizada no relatório técnico e na apresentação final.

O script `src/eda_final.py` trabalha sobre os conjuntos já preparados (`treino.csv` e `teste.csv`) e gera figuras reproduzíveis em `reports/figures/`.

## Figuras geradas

1. **Distribuição das notas (1 a 5)**  
   Mostra a quantidade de avaliações para cada nota original.

2. **Distribuição das classes de sentimento**  
   Apresenta a quantidade de avaliações negativas, neutras e positivas.

3. **Comprimento dos comentários por sentimento**  
   Compara a quantidade de palavras dos comentários entre as três classes.

4. **Termos mais frequentes por sentimento**  
   Gera uma figura separada para negativo, neutro e positivo.

Além das imagens, o script grava `reports/figures/eda_resumo.json`, contendo as contagens e estatísticas usadas nas visualizações.

## Resultado já conhecido da preparação

A base textual tratada contém 34.898 avaliações:

| Sentimento | Quantidade | Percentual |
|---|---:|---:|
| Positivo | 21.488 | 61,57% |
| Negativo | 10.245 | 29,36% |
| Neutro | 3.165 | 9,07% |
| **Total** | **34.898** | **100%** |

A distribuição mostra predominância de avaliações positivas e menor representação da classe neutra. Esse desbalanceamento ajuda a contextualizar o uso de `class_weight="balanced"` no classificador e o desempenho inferior da classe neutra.

## Execução

Com os arquivos processados disponíveis localmente:

```text
python -m src.eda_final
```

Para executar de uma vez a EDA final e a validação operacional agrupada por pedido:

```text
python -m src.finalizar_analise
```

Os CSVs processados não são versionados no GitHub por decisão do projeto. Por isso, as figuras que dependem desses arquivos precisam ser regeneradas no ambiente em que os dados foram preparados.
