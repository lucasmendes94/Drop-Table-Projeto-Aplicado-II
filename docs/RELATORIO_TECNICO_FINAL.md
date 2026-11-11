# Relatório técnico final — Projeto Aplicado II

## Drop Table — Análise de sentimentos em avaliações de e-commerce

### Equipe

- Igor Eduardo Dallan do Couto — RA 10748144
- Jaqueline de Oliveira Alves — RA 10755023
- Kayo Oliveira Nukui — RA 10356420
- Lucas de Lima Mendes — RA 10756562

## 1. Introdução

Este projeto foi desenvolvido no terceiro semestre do curso de Tecnologia em Banco de Dados da Universidade Presbiteriana Mackenzie.

O trabalho utiliza o conjunto público **Brazilian E-Commerce Public Dataset by Olist**, com foco nas avaliações realizadas por clientes após seus pedidos. Para contextualizar a aplicação, foi criada a empresa fictícia **ConectaShop**.

Em uma operação de e-commerce com grande volume de pedidos, a leitura manual das avaliações dificulta a identificação rápida de padrões. O projeto aplica preparação de dados, processamento de linguagem natural e aprendizado de máquina para transformar comentários textuais em informações estruturadas de apoio à decisão.

## 2. Problema e objetivo

A questão central do projeto é:

**Como utilizar avaliações textuais de clientes para identificar automaticamente sentimentos e temas recorrentes de insatisfação em uma operação de e-commerce?**

O trabalho foi desenvolvido para:

- preparar e documentar avaliações textuais;
- analisar a distribuição das classes de sentimento;
- classificar comentários em positivo, neutro e negativo;
- identificar temas recorrentes nas avaliações negativas;
- medir o desempenho do método analítico;
- transformar os resultados em uma proposta de produto para apoio ao negócio.

## 3. Fonte dos dados

Foi utilizado o conjunto público da Olist disponibilizado no Kaggle.

O arquivo principal do projeto é `olist_order_reviews_dataset.csv`, que contém identificadores da avaliação e do pedido, nota, título, comentário e datas relacionadas à avaliação.

Os dados brutos não são versionados no GitHub. A obtenção da base e a sequência de execução estão descritas em `docs/REPRODUCAO.md`.

## 4. Preparação e tratamento

O tratamento foi implementado em `src/preparacao.py`.

Foram executadas as seguintes etapas:

1. validação do esquema mínimo da base;
2. conversão da nota para valor numérico;
3. combinação de título e comentário;
4. normalização textual;
5. remoção de registros sem texto útil;
6. exclusão de textos iguais com rótulos conflitantes;
7. remoção de duplicatas textuais;
8. criação do rótulo de sentimento;
9. divisão estratificada em treino e teste.

Os rótulos foram definidos por nota:

- 1 e 2: **negativo**;
- 3: **neutro**;
- 4 e 5: **positivo**.

Das 99.224 linhas originais, permaneceram **34.898 avaliações textuais válidas**:

| Sentimento | Quantidade | Percentual |
|---|---:|---:|
| Positivo | 21.488 | 61,57% |
| Negativo | 10.245 | 29,36% |
| Neutro | 3.165 | 9,07% |
| **Total** | **34.898** | **100%** |

A divisão gerou **27.918 registros para treino** e **6.980 para teste**. A preparação remove duplicidades antes da divisão e o treinamento verifica novamente a inexistência de textos repetidos entre treino e teste.

## 5. Análise exploratória realizada

A distribuição das classes evidencia predominância das avaliações positivas e menor representação da classe neutra. Essa característica foi considerada na escolha de `class_weight="balanced"` para a regressão logística.

A exploração textual das avaliações negativas também foi realizada por NMF sobre TF-IDF. Foram usados cinco componentes e registrados os termos mais relevantes de cada tópico em `reports/etapa3/topicos_nmf.json`.

A inspeção mostrou que vários componentes convergiam para variações de problemas de entrega, especialmente expressões como “não recebi”, “não entregue”, “prazo”, “ainda não” e “não chegou”. Esse resultado foi utilizado como evidência exploratória para orientar a categorização temática posterior.

## 6. Método analítico

O classificador utiliza um pipeline de **TF-IDF + Regressão Logística** implementado em `src/treinamento.py`.

O TF-IDF usa unigramas e bigramas, com:

- `min_df=2`;
- `max_df=0.95`;
- `sublinear_tf=True`;
- `strip_accents="unicode"`.

A regressão logística utiliza:

- `class_weight="balanced"`;
- `max_iter=2000`;
- `random_state=42`.

O TF-IDF é ajustado somente nos dados de treino.

## 7. Resultados do classificador

No conjunto de teste com 6.980 avaliações, o modelo apresentou:

| Métrica | Resultado |
|---|---:|
| Acurácia | 80,40% |
| Precisão — negativo | 78,79% |
| Recall — negativo | 82,67% |
| F1 — negativo | 80,69% |
| F1 macro | 68,06% |
| F1 — neutro | 33,72% |
| F1 — positivo | 89,79% |

O F1-score da classe negativa ficou acima da meta de 0,80 estabelecida no projeto. A classe neutra apresentou desempenho inferior às demais classes.

A evidência numérica está em `reports/etapa3/comparacao_teste.json`.

## 8. Otimização da regressão logística

Foram testados nove valores do parâmetro C:

`0,01; 0,03; 0,1; 0,3; 1; 3; 10; 30; 100`.

A comparação utilizou validação cruzada estratificada de cinco folds no conjunto de treino. O critério definido foi maximizar o F1 médio da classe negativa.

O melhor resultado da grade foi obtido com **C = 1**, com F1 negativo médio de aproximadamente **80,34%**.

Como C = 1 já era usado no modelo-base, a otimização confirmou a configuração existente. Os 45 resultados individuais estão em `reports/etapa3/validacao_folds.csv` e o resumo em `reports/etapa3/comparacao_c.csv`.

## 9. Temas recorrentes de insatisfação

Após a exploração NMF, foi feita uma categorização interpretativa reproduzível por regras lexicais em `src/temas_insatisfacao.py`.

A análise utilizou as **8.196 avaliações negativas do conjunto de treino** e permite múltiplos temas por comentário.

| Tema | Menções detectadas | % das negativas de treino |
|---|---:|---:|
| Atraso ou não recebimento | 2.700 | 32,94% |
| Atendimento, troca ou reembolso | 926 | 11,30% |
| Defeito, avaria ou baixa qualidade | 625 | 7,63% |
| Produto diferente do solicitado | 592 | 7,22% |
| Pedido incompleto ou peças faltantes | 520 | 6,34% |

Foram identificadas 4.661 avaliações com pelo menos uma correspondência e 649 com mais de um tema.

Esses resultados são exploratórios. As regras detectam menções textuais e não comprovam, isoladamente, a ocorrência operacional do problema. As evidências estão em `reports/etapa3/cinco_temas.json` e `cinco_temas.csv`.

## 10. Produto gerado

A partir dos resultados foi criado o **Painel de Voz do Cliente da ConectaShop**, disponível em `produto/painel_voz_cliente.html`.

O protótipo reúne:

- acurácia e métricas da classe negativa;
- principal limitação da classe neutra;
- cinco temas exploratórios de insatisfação;
- uma leitura preliminar para apoio à priorização.

O produto demonstra como as saídas analíticas podem ser transformadas em uma visualização de apoio para áreas de Customer Experience, atendimento, qualidade e operações.

## 11. Modelo de negócio

A proposta de valor do produto é reduzir o esforço necessário para transformar grandes volumes de avaliações em informação organizada.

Os usuários principais seriam equipes de:

- Customer Experience;
- atendimento;
- operações e logística;
- qualidade;
- gestão de e-commerce.

No conjunto analisado, atraso ou não recebimento teve a maior presença entre os cinco temas definidos, indicando uma frente relevante para investigação operacional.

## 12. Rastreabilidade e reprodutibilidade

Todos os resultados numéricos utilizados neste relatório estão associados a código e evidências versionadas.

A matriz completa está em `docs/RASTREABILIDADE_RESULTADOS.md`.

A reprodução é documentada em `docs/REPRODUCAO.md`.

A execução registrada em `reports/etapa3/execucao.json` informa versões de Python e bibliotecas, semente aleatória, tamanho dos conjuntos e hashes SHA-256 de `treino.csv` e `teste.csv`.

## 13. Limitações observadas

Os resultados devem ser interpretados considerando:

- o sentimento foi derivado da nota, e não de anotação humana independente do texto;
- a classe neutra apresentou F1 significativamente inferior;
- a categorização temática usa regras lexicais exploratórias;
- 3.535 avaliações negativas não tiveram correspondência com os cinco temas definidos;
- 19 identificadores de pedido aparecem tanto no treino quanto no teste histórico, embora não haja textos idênticos entre os conjuntos;
- o conjunto Olist representa um recorte histórico e público de e-commerce.

Essas limitações fazem parte da interpretação dos resultados efetivamente obtidos.

## 14. Conclusão

O projeto aplicou um fluxo completo de preparação textual, classificação de sentimentos, avaliação, otimização e exploração temática.

O modelo alcançou **80,40% de acurácia** e **80,69% de F1 para a classe negativa**. A exploração das avaliações negativas destacou atraso ou não recebimento como o tema mais frequente entre as cinco categorias definidas.

Além da análise técnica, os resultados foram consolidados em um protótipo de Painel de Voz do Cliente, demonstrando uma aplicação prática para apoio à tomada de decisão.

## 15. Repositório

GitHub: `lucasmendes94/Drop-Table-Projeto-Aplicado-II`

O repositório contém código, documentação, evidências de execução, resultados e o protótipo produzido.

## 16. Referências

- OLIST. Brazilian E-Commerce Public Dataset by Olist. Kaggle.
- SCIKIT-LEARN. Documentação oficial do TF-IDF, Regressão Logística, métricas, validação cruzada e NMF.
