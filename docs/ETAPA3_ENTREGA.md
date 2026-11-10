# Etapa 3 — Aplicação do método, acurácia, resultados preliminares e storytelling

Este documento consolida os itens solicitados para a etapa anterior do Projeto Aplicado II.

## 1. Método analítico aplicado à base

Foi aplicado um modelo de classificação de sentimentos baseado em **TF-IDF + Regressão Logística**.

A base textual tratada foi dividida de forma estratificada em 27.918 registros para treino e 6.980 para teste. O pipeline completo está implementado em `src/preparacao.py` e `src/treinamento.py`.

A Etapa 3 também avaliou nove valores do hiperparâmetro C por validação cruzada estratificada em cinco folds. O critério de escolha foi o maior F1-score médio da classe negativa. O melhor valor foi **C = 1**, confirmando o baseline.

Detalhamento: [Método analítico aplicado](METODO_ANALITICO.md).

## 2. Medidas de acurácia

Resultados no conjunto de teste:

| Métrica | Resultado |
|---|---:|
| Acurácia | 80,40% |
| Precisão — negativo | 78,79% |
| Recall — negativo | 82,67% |
| F1 — negativo | 80,69% |
| F1 macro | 68,06% |
| F1 — neutro | 33,72% |
| F1 — positivo | 89,79% |

O resultado atende à meta de F1 mínimo de 0,80 para a classe negativa. A classe neutra permanece como principal ponto de melhoria.

As evidências estão em `reports/etapa3/comparacao_teste.json`, `comparacao_c.csv` e `validacao_folds.csv`.

## 3. Resultados preliminares e produto

Foram analisadas 8.196 avaliações negativas do treino. Cinco temas exploratórios foram documentados:

| Tema | Menções | % das negativas de treino |
|---|---:|---:|
| Atraso ou não recebimento | 2.700 | 32,94% |
| Atendimento, troca ou reembolso | 926 | 11,30% |
| Defeito, avaria ou baixa qualidade | 625 | 7,63% |
| Produto diferente do solicitado | 592 | 7,22% |
| Pedido incompleto ou peças faltantes | 520 | 6,34% |

Como produto preliminar é proposto o **Painel de Voz do Cliente da ConectaShop**, voltado a consolidar sentimento, avaliações negativas e temas de insatisfação para apoiar Customer Experience, atendimento e operações.

Detalhamento: [Resultados preliminares](RESULTADOS_PRELIMINARES.md) e [Modelo de negócios](MODELO_NEGOCIO.md).

## 4. Esboço do storytelling

A narrativa proposta segue:

**Problema → dados → preparação → modelo → resultados → principal descoberta → produto → valor de negócio → limitações → próximos passos.**

O ponto central do storytelling é mostrar a evolução de comentários textuais dispersos para informação acionável.

Detalhamento: [Esboço do storytelling](STORYTELLING.md).

## 5. Limitações registradas

- sentimento derivado da nota, sem anotação humana independente;
- baixo desempenho da classe neutra;
- análise de temas exploratória e baseada em regras lexicais;
- 19 pedidos aparecem em treino e teste, embora sem textos idênticos;
- ainda não foi realizada validação operacional externa.

Essas limitações devem permanecer explícitas no relatório final para evitar conclusões além do que os experimentos suportam.
