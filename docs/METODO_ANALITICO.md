# Método analítico aplicado

## Objetivo

O método analítico do projeto tem como objetivo classificar automaticamente avaliações textuais de clientes em três classes de sentimento: **negativo**, **neutro** e **positivo**.

Os rótulos são derivados da nota da avaliação:
- notas 1 e 2: negativo;
- nota 3: neutro;
- notas 4 e 5: positivo.

A classificação é aplicada às avaliações públicas da Olist e serve como base para identificar padrões de satisfação e insatisfação no cenário fictício da ConectaShop.

## Método escolhido

Foi utilizado um pipeline composto por:

1. **TF-IDF** para transformar o texto em representação numérica;
2. **Regressão Logística** para realizar a classificação multiclasse.

O TF-IDF foi configurado com unigramas e bigramas, frequência mínima de 2 documentos, frequência máxima de 95%, normalização sublinear e remoção de acentos durante a vetorização.

A regressão logística foi configurada com:
- `class_weight="balanced"`, para reduzir o efeito do desbalanceamento entre as classes;
- `max_iter=2000`;
- semente aleatória 42.

## Aplicação à base

Após a preparação, a base ficou com 34.898 avaliações textuais válidas:

- 21.488 positivas;
- 10.245 negativas;
- 3.165 neutras.

A divisão estratificada gerou:

- 27.918 avaliações para treino;
- 6.980 avaliações para teste.

Os textos duplicados e os textos com rótulos conflitantes foram removidos antes da divisão. O TF-IDF foi ajustado somente com os dados de treino, evitando que o vocabulário do teste influenciasse o modelo.

## Otimização do modelo

Na Etapa 3 foram avaliados nove valores do parâmetro C da regressão logística:

`0,01; 0,03; 0,1; 0,3; 1; 3; 10; 30; 100`.

A avaliação utilizou validação cruzada estratificada com cinco divisões do conjunto de treino. O critério definido foi maximizar o F1-score da classe negativa.

O melhor resultado médio foi obtido com **C = 1**, que já era o valor utilizado no modelo-base. Portanto, a otimização confirmou a configuração original em vez de produzir uma troca de hiperparâmetro.

## Métricas utilizadas

Como a base possui três classes e distribuição desigual entre elas, a avaliação não considera apenas acurácia.

Foram utilizadas:

- acurácia geral;
- precisão por classe;
- recall por classe;
- F1-score por classe;
- F1 macro;
- matriz de confusão.

O F1-score da classe negativa recebe atenção especial porque o projeto pretende apoiar a identificação de clientes insatisfeitos e havia sido definida uma meta mínima de 0,80 para essa classe.

## Limitações

O rótulo de sentimento é derivado da nota e não de anotação humana independente do texto. A classe neutra apresenta menor desempenho e pode conter avaliações linguisticamente ambíguas.

Também foram identificados 19 `order_id` presentes em treino e teste. Não existem textos idênticos entre os conjuntos, porém avaliações relacionadas ao mesmo pedido podem ter alguma correlação. Por isso, uma futura validação agrupada por pedido é recomendada como aprimoramento metodológico.

## Arquivos relacionados

- `src/preparacao.py`
- `src/treinamento.py`
- `src/etapa3.py`
- `docs/TRATAMENTO_BASE_DADOS.md`
- `docs/ETAPA3_TEMAS_E_OTIMIZACAO.md`
- `reports/etapa3/comparacao_c.csv`
- `reports/etapa3/comparacao_teste.json`
