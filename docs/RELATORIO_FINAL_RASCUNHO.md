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

Em uma operação de e-commerce com grande volume de pedidos, a leitura manual de avaliações pode dificultar a identificação rápida de padrões de satisfação e insatisfação. Por isso, o projeto busca aplicar técnicas de preparação de dados, processamento de linguagem natural e aprendizado de máquina para transformar comentários textuais em informações estruturadas de apoio à decisão.

## 2. Problema e objetivo

O problema central definido pelo grupo foi:

**Como utilizar avaliações textuais de clientes para identificar automaticamente sentimentos e temas recorrentes de insatisfação em uma operação de e-commerce?**

O objetivo geral é construir uma análise capaz de:

- preparar e documentar avaliações textuais em português;
- analisar a distribuição das avaliações;
- classificar os comentários em sentimentos positivo, neutro e negativo;
- identificar temas recorrentes de insatisfação;
- avaliar o desempenho do método analítico;
- propor uma forma de transformar esses resultados em informação útil para o negócio.

## 3. Fonte dos dados

Foi utilizado o conjunto público da Olist, disponibilizado no Kaggle.

O projeto utiliza principalmente o arquivo de avaliações de pedidos, que contém identificadores do pedido e da avaliação, nota, título e comentário textual.

Os arquivos brutos não são versionados no repositório. O GitHub mantém o código necessário para reproduzir a preparação e as análises.

## 4. Preparação e tratamento da base

O tratamento foi implementado em `src/preparacao.py`.

As principais etapas foram:

1. validação das colunas obrigatórias;
2. conversão e validação da nota;
3. combinação do título e do comentário;
4. normalização textual;
5. remoção de registros sem texto útil;
6. remoção de textos com rótulos conflitantes;
7. remoção de duplicatas textuais;
8. criação do rótulo de sentimento;
9. divisão estratificada em treino e teste.

Os sentimentos foram definidos a partir das notas:

- notas 1 e 2: **negativo**;
- nota 3: **neutro**;
- notas 4 e 5: **positivo**.

Após o tratamento, permaneceram **34.898 avaliações textuais válidas**:

| Sentimento | Quantidade | Percentual |
|---|---:|---:|
| Positivo | 21.488 | 61,57% |
| Negativo | 10.245 | 29,36% |
| Neutro | 3.165 | 9,07% |
| **Total** | **34.898** | **100%** |

A divisão estratificada gerou **27.918 registros de treino** e **6.980 registros de teste**, sem textos idênticos entre os dois conjuntos.

Figura disponível: [Distribuição dos sentimentos](../reports/figures/distribuicao_sentimentos_resumo.svg).

## 5. Análise exploratória

A análise exploratória final foi estruturada para incluir:

- distribuição das notas;
- distribuição das classes de sentimento;
- comprimento dos comentários;
- principais termos por sentimento.

O script `src/eda_final.py` gera automaticamente essas figuras a partir dos conjuntos processados.

A distribuição já conhecida mostra maior presença de avaliações positivas e menor representação da classe neutra. Esse desbalanceamento foi considerado no treinamento do modelo.

> **Pendente de execução local:** gerar as figuras de distribuição das notas, comprimento dos comentários e termos mais frequentes usando `python -m src.eda_final`.

## 6. Método analítico

O método escolhido combina **TF-IDF** e **Regressão Logística**.

O TF-IDF transforma os comentários em vetores numéricos com base na importância relativa dos termos. Foram considerados unigramas e bigramas.

A Regressão Logística realiza a classificação multiclasse entre negativo, neutro e positivo.

A configuração principal utiliza:

- `ngram_range=(1, 2)`;
- `min_df=2`;
- `max_df=0.95`;
- `sublinear_tf=True`;
- `class_weight="balanced"`;
- `max_iter=2000`;
- semente aleatória 42.

Todo o ajuste do TF-IDF ocorre somente no conjunto de treino.

## 7. Avaliação do modelo

No conjunto de teste histórico, o modelo obteve:

| Métrica | Resultado |
|---|---:|
| Acurácia | 80,40% |
| Precisão — negativo | 78,79% |
| Recall — negativo | 82,67% |
| F1 — negativo | 80,69% |
| F1 macro | 68,06% |
| F1 — neutro | 33,72% |
| F1 — positivo | 89,79% |

O F1-score da classe negativa ficou acima da meta de 0,80 estabelecida para o projeto.

A classe neutra apresentou o menor desempenho e representa o principal ponto de melhoria.

Figura disponível: [Desempenho do modelo](../reports/figures/desempenho_modelo.svg).

## 8. Otimização

Foram avaliados nove valores do parâmetro `C`:

`0,01; 0,03; 0,1; 0,3; 1; 3; 10; 30; 100`.

A seleção utilizou validação cruzada estratificada em cinco folds do conjunto de treino. O critério adotado foi o maior F1-score médio da classe negativa.

O melhor valor foi **C = 1**, com F1 negativo médio de aproximadamente **80,34%**.

Como o valor selecionado já era utilizado no baseline, a otimização confirmou a configuração inicial e não produziu ganho adicional no teste histórico.

Figura disponível: [Otimização do parâmetro C](../reports/figures/otimizacao_c.svg).

## 9. Temas recorrentes de insatisfação

A exploração das avaliações negativas utilizou NMF como apoio inicial à descoberta de padrões. Como vários componentes encontrados se concentravam em variações do mesmo problema de entrega, foi criada posteriormente uma categorização interpretativa com regras lexicais explícitas e possibilidade de múltiplos temas por avaliação.

Foram analisadas **8.196 avaliações negativas do conjunto de treino**.

| Tema | Menções detectadas | % das negativas de treino |
|---|---:|---:|
| Atraso ou não recebimento | 2.700 | 32,94% |
| Atendimento, troca ou reembolso | 926 | 11,30% |
| Defeito, avaria ou baixa qualidade | 625 | 7,63% |
| Produto diferente do solicitado | 592 | 7,22% |
| Pedido incompleto ou peças faltantes | 520 | 6,34% |

Ao todo, 4.661 avaliações tiveram pelo menos uma correspondência e 649 apresentaram mais de um tema.

As categorias são exploratórias e multirrótulo. Os percentuais não representam taxas oficiais de falhas operacionais.

Figura disponível: [Temas de insatisfação](../reports/figures/temas_insatisfacao.svg).

## 10. Validação adicional por pedido

A auditoria da divisão original identificou **19 `order_id` presentes tanto no treino quanto no teste**, embora não existam textos idênticos entre os conjuntos.

Para avaliar o possível efeito dessa dependência, foi implementado `src/etapa3_validacao.py`, que realiza:

- auditoria dos pedidos compartilhados;
- reavaliação do teste sem pedidos compartilhados;
- nova divisão agrupada por `order_id`;
- validação cruzada agrupada por pedido;
- bootstrap por pedido;
- estudo de calibração;
- avaliação de limiares para a classe negativa.

> **Pendente de execução local:** incorporar aqui as métricas produzidas por `reports/etapa3/validacao_operacional/validacao_operacional.json`.

A ausência dessas métricas não invalida os resultados históricos, mas a análise agrupada é importante para avaliar melhor a generalização para pedidos novos.

## 11. Produto analítico proposto

Como produto do projeto, foi proposto o **Painel de Voz do Cliente da ConectaShop**.

O painel reúne:

- indicadores de desempenho do classificador;
- distribuição de sentimentos;
- destaque de avaliações negativas;
- principais temas de insatisfação;
- informações para apoiar a priorização de problemas.

Um protótipo simples está disponível em `produto/painel_voz_cliente.html`.

O objetivo não é substituir a análise humana, mas reduzir o esforço necessário para ler grandes volumes de comentários e criar uma primeira triagem.

## 12. Modelo de negócio

Os principais usuários do produto seriam áreas de:

- Customer Experience;
- atendimento;
- operações e logística;
- qualidade;
- gestão de e-commerce.

A proposta de valor está em transformar comentários dispersos em indicadores organizados.

No cenário estudado, **atraso ou não recebimento** foi o tema com maior presença entre as regras exploratórias aplicadas às avaliações negativas, sugerindo que logística e cumprimento de prazos seriam uma frente relevante de investigação.

Uma evolução empresarial poderia incluir processamento periódico de novas avaliações, alertas automáticos e integração com informações de pedido, vendedor, categoria e logística.

## 13. Storytelling do projeto

A narrativa final foi estruturada da seguinte forma:

**Problema → Dados → Preparação → Modelo → Avaliação → Descoberta → Produto → Valor para o negócio → Limitações → Próximos passos.**

A ideia central é mostrar que o projeto parte de comentários textuais dispersos e chega a informação estruturada que pode apoiar decisões.

## 14. Limitações

As principais limitações registradas são:

- os rótulos de sentimento foram derivados das notas e não de anotação humana independente;
- a classe neutra possui baixo desempenho;
- as regras de temas são exploratórias e não foram validadas como classificador;
- os resultados de temas representam a amostra textual tratada;
- o teste histórico já foi utilizado em etapas anteriores;
- a divisão inicial possui 19 pedidos compartilhados entre treino e teste;
- os dados públicos não representam necessariamente a operação atual de uma empresa.

## 15. Próximos passos

Como evolução do projeto, recomenda-se:

- executar e documentar a validação agrupada por pedido;
- criar uma amostra rotulada manualmente para validar os temas;
- estudar alternativas para melhorar a classe neutra;
- testar outros modelos de classificação;
- integrar novas variáveis do conjunto Olist;
- transformar o protótipo em um dashboard interativo.

## 16. Conclusão

O projeto demonstrou que técnicas de processamento de texto e aprendizado de máquina podem transformar avaliações de clientes em indicadores úteis.

O modelo obteve 80,40% de acurácia e F1 de 80,69% para a classe negativa. Além da classificação, a análise exploratória permitiu identificar temas recorrentes de insatisfação, com destaque para atraso ou não recebimento.

Os resultados indicam potencial para uso como ferramenta de apoio à experiência do cliente, desde que suas limitações sejam consideradas e que as análises exploratórias sejam complementadas por validação operacional.

## 17. Repositório

GitHub: `lucasmendes94/Drop-Table-Projeto-Aplicado-II`

O repositório contém o código de preparação, treinamento, validação, documentação, resultados reproduzíveis e protótipo do produto.

## 18. Referências

- OLIST. Brazilian E-Commerce Public Dataset by Olist. Kaggle.
- SCIKIT-LEARN. Documentação oficial — TF-IDF, Regressão Logística e métricas de classificação.
- SCIKIT-LEARN. Documentação oficial — validação cruzada e modelagem NMF.
