# Notebooks de análise

Os notebooks percorrem o projeto na ordem em que ele foi feito: conhecer os dados, preparar o texto, escolher e treinar o classificador, avaliar o modelo e investigar os motivos de insatisfação. A regra de preparação e o treino do modelo oficial ficam em `src/`; os notebooks 02 e 03 chamam essas funções, então existe uma única versão de cada regra.

## Mapa dos notebooks

| Notebook | O que faz | Responsável | Lê | Grava |
|---|---|---|---|---|
| [`01_analise_exploratoria.ipynb`](01_analise_exploratoria.ipynb) | Estrutura da base, valores ausentes, notas, tempo de resposta, tamanho dos textos e palavras frequentes | Igor Eduardo Dallan do Couto | `data/raw/olist_order_reviews_dataset.csv` | Nada |
| [`02_preparacao_textual.ipynb`](02_preparacao_textual.ipynb) | Normalização, remoção de textos vazios, conflitantes e duplicados, divisão 80/20 estratificada | Lucas de Lima Mendes | Arquivo bruto | `data/processed/avaliacoes_preparadas.csv`, `treino.csv`, `teste.csv`, `relatorio_preparacao.json` |
| [`03_modelos_classificacao.ipynb`](03_modelos_classificacao.ipynb) | Compara quatro classificadores por validação cruzada no treino, testa valores de `C` para a Regressão Logística e o LinearSVC e treina o modelo oficial | Jaqueline de Oliveira Alves | `treino.csv` e `teste.csv` | `data/processed/modelo/modelo_sentimento.joblib`, `metricas_modelo.json`, `previsoes_teste.csv` |
| [`04_calculo_e_avaliacao_acuracia.ipynb`](04_calculo_e_avaliacao_acuracia.ipynb) | Matriz de confusão, contas de precisão, recall e F1, Meta 1, curvas ROC e precisão-recall, validação cruzada, textos repetidos e sensibilidade ao limiar | Kayo Oliveira Nukui | `teste.csv`, `treino.csv` e o modelo | Nada |
| [`05_analise_topicos_e_insatisfacao.ipynb`](05_analise_topicos_e_insatisfacao.ipynb) | Tópicos de insatisfação com NMF nas avaliações negativas (Meta 2) | Equipe | `avaliacoes_preparadas.csv` | Nada |

## Como rodar

1. Crie o ambiente e instale as dependências: `pip install -r requirements.txt`.
2. Coloque `olist_order_reviews_dataset.csv` em `data/raw/` (veja `data/raw/README.md`).
3. Abra os notebooks na ordem 01 a 05 e use "Restart & Run All" em cada um. O notebook 02 precisa rodar antes do 03, e o 03 antes do 04.

Se preferir o terminal, `python -m src.preparacao` e `python -m src.treinamento` geram os mesmos arquivos dos notebooks 02 e 03.

## Principais resultados

Valores obtidos com a base e a semente atuais. Se o ambiente mudar, rode os notebooks de novo antes de citar os números.

| Etapa | Resultado |
|---|---|
| Preparação | 99.224 linhas brutas; 34.898 avaliações preparadas (21.488 positivas, 10.245 negativas, 3.165 neutras); 27.918 de treino e 6.980 de teste |
| Comparação (validação cruzada no treino) | A Regressão Logística tem o maior F1 macro (0,677); o Naive Bayes tem a maior acurácia (0,839) e o menor F1 macro (0,576) |
| Modelo oficial no teste | Acurácia de 80,40%; na classe negativa, precisão de 78,79%, recall de 82,67% e F1 de 0,8069 |
| Meta 1 (F1 negativo mínimo de 0,80) | Atingida no teste, com margem pequena; na validação cruzada, média de 0,803 e uma das cinco partições abaixo de 0,80 |
| Classe neutra | F1 de 0,337: é o ponto fraco do modelo |
| Curvas (classe negativa) | ROC AUC de 0,948 e precisão média de 0,869 |
| Temas (Meta 2) | Cinco componentes de NMF, mas só dois temas claros: não recebimento ou recebimento incompleto e atraso na entrega. Meta parcialmente demonstrada |

## Limites conhecidos

- O rótulo vem da nota, não da leitura do texto. Avaliações de nota 3 muitas vezes misturam elogio e crítica, o que limita a classe neutra.
- As probabilidades da Regressão Logística ordenam bem os casos, mas não foram calibradas. Qualquer limiar diferente de "classe mais provável" precisa ser escolhido fora do conjunto de teste.
- A checagem de sobreposição entre treino e teste compara textos com acento. Depois da vetorização, 123 avaliações de teste (1,76%) ficam iguais a avaliações de treino; sem elas, o F1 negativo passa de 0,8069 para 0,8061 (notebook 04, seção 10).
- O notebook 03 testa alguns valores de `C` para a Regressão Logística e o LinearSVC (seção 6, só no treino); o melhor `C` da Regressão Logística (0,5) tem F1 macro praticamente igual ao `C=1,0` usado no modelo oficial, então o valor padrão foi mantido.
- O projeto usa só o arquivo de avaliações. Relações entre atraso de entrega e nota exigiriam a tabela de pedidos da Olist.
