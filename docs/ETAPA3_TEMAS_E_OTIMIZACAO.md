# Etapa 3 — Temas de insatisfação e otimização da regressão logística

Responsável: Lucas de Lima Mendes. Execução: 22/10/2026.

Foram identificados cinco temas recorrentes nas avaliações negativas e comparados nove valores de C. A seleção por validação cruzada manteve C = 1, já usado no modelo-base. As evidências e os comandos abaixo permitem reproduzir os dois itens atribuídos a Lucas.

## Base e escopo

Foram reutilizados os arquivos de treino e teste produzidos na Etapa 2: 27.918 avaliações para treino e 6.980 para teste. A análise temática utiliza exclusivamente as 8.196 avaliações negativas do treino, sem consultar comentários do teste. Os hashes dos arquivos e as versões das bibliotecas estão em [execucao.json](../reports/etapa3/execucao.json).

O rótulo negativo corresponde às notas 1 e 2; neutro à nota 3; positivo às notas 4 e 5. Esses rótulos são aproximações do sentimento baseadas na nota, não anotações humanas do texto. A preparação anterior removeu comentários vazios, textos conflitantes e duplicatas. Por isso, as frequências abaixo descrevem a amostra textual tratada e não representam todos os pedidos da Olist.

## Cinco temas recorrentes

Primeiro foi executada NMF com cinco componentes sobre TF-IDF dos comentários negativos do treino. A leitura dos 20 termos principais e de 12 exemplos representativos por componente mostrou que quatro componentes se concentravam em variantes de não recebimento e atraso. Não seria adequado apresentá-los como cinco problemas de negócio distintos.

Os termos e exemplos foram então usados para orientar uma categorização interpretativa. Para produzir contagens auditáveis, foram aplicadas regras lexicais explícitas em `src/temas_insatisfacao.py`, permitindo múltiplos temas por comentário. Foram lidos 15 exemplos sorteados por categoria, com semente 42, como revisão qualitativa assistida; essa leitura não equivale a validação humana independente nem mede a precisão do método.

| Tema | Correspondências lexicais | % das 8.196 negativas de treino | Exemplo observado no treino |
|---|---:|---:|---|
| Atraso ou não recebimento | 2.700 | 32,94% | “não recebi minha encomenda ainda” |
| Atendimento, troca ou reembolso | 926 | 11,30% | “solicitei a troca e ainda não fui atendida” |
| Defeito, avaria ou baixa qualidade | 625 | 7,63% | “péssima qualidade estarei devolvendo o produto” |
| Produto diferente do solicitado | 592 | 7,22% | “o produto é de boa qualidade mas veio errado” |
| Pedido incompleto ou peças faltantes | 520 | 6,34% | “produto não veio lacrado veio faltando peça” |

Ao todo, 4.661 avaliações apresentaram pelo menos uma correspondência; 649 apresentaram mais de uma categoria e 3.535 não foram capturadas pelas regras. As categorias se sobrepõem e os percentuais não devem somar 100%. Não são os cinco temas mais frequentes de uma taxonomia exaustiva; são cinco temas recorrentes com evidência textual nesta amostra.

### Limitações das contagens

As regras detectam menções, não comprovam a ocorrência do problema. A revisão encontrou, por exemplo, “devolução demorada” capturada como atraso de entrega e “pergunta que não corresponde” capturada como produto divergente. Menções a troca também podem indicar apenas uma solicitação, e não falha do atendimento. Há ainda sinônimos, erros de escrita e negações que podem gerar falsos negativos ou positivos. Os números devem ser apresentados como resultados exploratórios, sem convertê-los em taxas oficiais de falhas operacionais.

Os exemplos completos e as marcações por avaliação ficam localmente em `data/processed/etapa3/`. Para validação operacional, a equipe poderá rotular uma amostra independente e medir precisão/recall por tema. A presente entrega fornece a descoberta temática e suas evidências, não um classificador de reclamações validado.

## Otimização do parâmetro C

C controla inversamente a intensidade da regularização: valores menores regularizam mais. Mantiveram-se TF-IDF com unigramas e bigramas, `min_df=2`, `max_df=0.95`, `sublinear_tf=True`, remoção de acentos na vetorização, regressão logística com `class_weight="balanced"`, `max_iter=2000` e semente 42.

Foram comparados C = 0,01; 0,03; 0,1; 0,3; 1; 3; 10; 30; 100, em validação cruzada estratificada de cinco divisões do treino, com embaralhamento e semente 42. O critério definido antes da execução foi maximizar o F1 médio da classe negativa, alinhado à meta do projeto; em empate, escolher o menor C. O F1 macro foi registrado como indicador secundário.

O TF-IDF foi ajustado novamente apenas na parcela de treinamento de cada divisão. A mesma matriz desse fold foi reutilizada entre os valores de C, sem compartilhar vocabulário com a parcela de validação. Foram realizados 45 ajustes, todos concluídos sem aviso de falta de convergência.

| C | F1 negativo médio | Desvio entre folds | F1 macro médio |
|---:|---:|---:|---:|
| 0,01 | 0,7672 | 0,0115 | 0,6459 |
| 0,03 | 0,7756 | 0,0111 | 0,6567 |
| 0,1 | 0,7894 | 0,0089 | 0,6697 |
| 0,3 | 0,8016 | 0,0086 | 0,6774 |
| **1** | **0,8034** | **0,0066** | **0,6771** |
| 3 | 0,8018 | 0,0069 | 0,6697 |
| 10 | 0,7958 | 0,0095 | 0,6563 |
| 30 | 0,7907 | 0,0084 | 0,6451 |
| 100 | 0,7847 | 0,0072 | 0,6382 |

O melhor valor na grade foi C = 1. C = 0,3 apresentou F1 macro ligeiramente maior, mas esse não era o critério de seleção. A pequena diferença entre os melhores candidatos não demonstra superioridade estatística; o desvio registrado é desvio amostral entre folds, não intervalo de confiança.

### Comparação no teste

Após a seleção, o modelo foi ajustado com todo o treino e avaliado no teste histórico. O baseline foi reexecutado no mesmo ambiente para uma comparação consistente. Como o C selecionado é igual ao baseline, os resultados são idênticos: acurácia 80,40%; precisão negativa 78,79%; recall negativo 82,67%; F1 negativo 80,69%; F1 macro 68,06%; F1 neutro 33,72%.

A otimização foi concluída e justifica manter C = 1; não houve ganho sobre o baseline. O teste já havia sido utilizado na Etapa 2, portanto esta comparação é uma reavaliação no teste histórico, não validação externa nova. Os resultados de teste não foram usados na escolha de C. A dificuldade com a classe neutra permanece e deve ser considerada pelos responsáveis pela validação operacional e pelos limiares.

A auditoria encontrou 19 identificadores de pedido presentes tanto no treino quanto no teste, embora não existam textos idênticos entre esses conjuntos. A estratificação herdada é por avaliação, não por pedido; avaliações do mesmo pedido podem ser correlacionadas. Os folds também não são agrupados por pedido. Para validar generalização a pedidos novos, recomenda-se uma avaliação adicional com separação por `order_id` e, se disponível, por cliente. Esta execução conserva a divisão da Etapa 2 para comparar C em condições equivalentes e não demonstra independência por pedido.

## Reprodução e arquivos

Com os dados originais disponíveis, execute na raiz do repositório:

```text
python -m pip install -r requirements-etapa3.txt
python -m src.preparacao
python -m src.etapa3
python -m src.temas_insatisfacao
```

Se `treino.csv` e `teste.csv` da Etapa 2 já estiverem disponíveis, pule a preparação. Compare seus hashes com `execucao.json`. `python -m src.etapa3 --somente-temas` executa apenas a exploração NMF. A execução completa regrava os resultados da pasta de saída; conserve cópias de experimentos anteriores antes de comparar novas configurações.

- [Comparação dos valores de C](../reports/etapa3/comparacao_c.csv).
- [Resultados individuais dos 45 ajustes](../reports/etapa3/validacao_folds.csv).
- [Comparação no teste histórico](../reports/etapa3/comparacao_teste.json).
- [Cinco temas e regras de identificação](../reports/etapa3/cinco_temas.json).
- [Termos dos tópicos NMF](../reports/etapa3/topicos_nmf.json).

O modelo selecionado fica localmente em `data/processed/etapa3/modelo_c_otimizado.joblib`. Dados individuais, amostras completas e modelos binários não são publicados no GitHub.

## Encaminhamento ao grupo

Os dois itens de Lucas estão concluídos como análise exploratória e busca de hiperparâmetro. Validação operacional, calibração, limiares, redação geral dos resultados, storytelling e revisão/entrega do PDF continuam com os respectivos responsáveis. Este documento contém material para incorporar ao relatório, mas não substitui essas atividades.

## Referências técnicas

- [Scikit-learn — busca em grade com validação cruzada](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html).
- [Scikit-learn — fatoração de matrizes não negativas](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html).
- [Olist — fonte original dos dados](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
