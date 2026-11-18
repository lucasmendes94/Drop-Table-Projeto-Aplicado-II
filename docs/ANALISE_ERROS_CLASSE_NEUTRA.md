# Análise de erros da classe neutra

Este documento analisa o desempenho e os padrões de erro envolvendo a classe neutra no conjunto de teste do classificador oficial de sentimentos (`TF-IDF` e Regressão Logística balanceada), a partir de `data/processed/modelo/metricas_modelo.json`, `data/processed/modelo/previsoes_teste.csv` e `data/processed/teste.csv`.

## 1. Validação da correspondência entre avaliações e previsões

Antes da seleção dos exemplos, foi conferida a correspondência entre `data/processed/teste.csv` e `data/processed/modelo/previsoes_teste.csv` pelo identificador `review_id`. Ambos os arquivos têm 6.980 registros, sem valores nulos nem duplicatas em `review_id`, com cobertura de 100% entre os dois conjuntos (diferença simétrica igual a zero). Após a junção `1:1`, o campo `sentimento` de `teste.csv` coincide com `sentimento_real` de `previsoes_teste.csv` em todas as 6.980 linhas, preservando a mesma ordem gerada por `src/treinamento.py`.

## 2. Métricas da classe neutra e matriz de confusão

Em `data/processed/modelo/metricas_modelo.json`, a classe neutra apresenta os seguintes valores no conjunto de teste:

| Métrica | Valor | Razão exata (previsões / base) |
|---|---:|---|
| Precisão (`precision`) | 27,30% (`0,2730`) | `279 / 1.022` (entre as avaliações previstas como neutras) |
| Recall (`recall`) | 44,08% (`0,4408`) | `279 / 633` (entre as avaliações reais neutras) |
| F1-score (`f1-score`) | 33,72% (`0,3372`) | média harmônica entre precisão e recall |
| Suporte (`support`) | 633 | `633 / 6.980` (`9,07%` do conjunto de teste) |

### Matriz de confusão no conjunto de teste (6.980 avaliações)

| Rótulo real \ Previsto | `negativo` | `neutro` | `positivo` | Total real |
|---|---:|---:|---:|---:|
| `negativo` | 1.694 | 303 | 52 | 2.049 |
| `neutro` | 237 | 279 | 117 | 633 |
| `positivo` | 219 | 440 | 3.639 | 4.298 |
| Total previsto | 2.150 | 1.022 | 3.808 | 6.980 |

## 3. As quatro direções de erro envolvendo a classe neutra

Os 1.097 erros ligados à classe neutra (`15,72%` das 6.980 avaliações de teste) distribuem-se em quatro direções:

| Direção (real → previsto) | Quantidade | % sobre o total da classe real | % sobre o total da classe prevista |
|---|---:|---:|---:|
| `neutro` → `negativo` | 237 | 37,44% (`237 / 633` neutros reais) | 11,02% (`237 / 2.150` previstos negativos) |
| `neutro` → `positivo` | 117 | 18,48% (`117 / 633` neutros reais) | 3,07% (`117 / 3.808` previstos positivos) |
| `negativo` → `neutro` | 303 | 14,79% (`303 / 2.049` negativos reais) | 29,65% (`303 / 1.022` previstos neutros) |
| `positivo` → `neutro` | 440 | 10,24% (`440 / 4.298` positivos reais) | 43,05% (`440 / 1.022` previstos neutros) |

## 4. Origem do rótulo neutro e divergência entre nota e texto

Conforme `MAPA_SENTIMENTO` em `src/preparacao.py`, o rótulo de referência deriva apenas da nota numérica atribuída na avaliação (`review_score`): notas 1 e 2 geram `negativo`, nota 3 gera `neutro` e notas 4 e 5 geram `positivo`. Como o classificador lê somente o texto normalizado (`texto_limpo`), ocorrem três fontes de confusão:

1. **Nota 3 com texto polarizado:** clientes atribuem nota intermediária (3), mas escrevem reclamações explícitas (atraso, extravio, item faltante) ou elogios diretos.
2. **Notas extremas com texto moderado, curto ou misto:** clientes dão nota 1 ou 2 com relatos breves ou contidos, ou dão nota 4 ou 5 com ressalvas ("ainda não testei", "bom, mas demorou"), aproximando o vocabulário do padrão observado na nota 3.
3. **Desbalanceamento e `class_weight="balanced"`:** como a classe neutra representa 9,07% do conjunto, o balanceamento de pesos amplia a sensibilidade para prever `neutro` (1.022 previsões neutras para 633 reais) e reduz a precisão (27,30%).

## 5. Exemplos rastreáveis por direção de erro

> Os exemplos abaixo foram extraídos de `data/processed/teste.csv` e `data/processed/modelo/previsoes_teste.csv`, sem expor dados pessoais, apenas para ilustrar os mecanismos de erro observados. Eles não devem ser usados para estimar a frequência desses padrões na base.

### 5.1 `neutro` → `negativo` (237 casos)

| `review_id` | Nota | Real → Previsto | Texto original | Interpretação |
|---|---|---|---|---|
| `58b4413cd843fed2be9fe01ca1dd7aef` | 3 | `neutro` → `negativo` | "Carga roubada. O site dos correios diz que a carga foi roubada. Esperando resolução." | Nota intermediária acompanhada de relato grave de extravio ou roubo, captado como problema pelo vocabulário negativo. |
| `608e890852fc78c3854d83a0cfab8557` | 3 | `neutro` → `negativo` | "Até agora não recebi nada, a colcha estava prevista para anteontem(18/12) e até agora nada" | Reclamação explícita de atraso e não recebimento, com tom incompatível com uma avaliação neutra. |
| `a8e3a7512fa5b1c3ba9fa2f7757766da` | 3 | `neutro` → `negativo` | "Comprei 2 unidades e recebi apenas 1 unidade!!" | Relato objetivo de pedido incompleto; o modelo associa "recebi apenas" ao padrão de insatisfação. |

### 5.2 `neutro` → `positivo` (117 casos)

| `review_id` | Nota | Real → Previsto | Texto original | Interpretação |
|---|---|---|---|---|
| `56fa8f6d3b3418e1e00dd4c59e8fa3f9` | 3 | `neutro` → `positivo` | "10 otimo foi entrege antes do prazo" | Elogio explícito ("otimo", "antes do prazo") divergente da nota 3 atribuída na plataforma. |
| `9d14b1424ca737608bc50f9d3c1a78bb` | 3 | `neutro` → `positivo` | "Produto de boa qualidade, exatamente conforme anunciado, e o preço baixo é uma atrativo a mais." | Texto inteiramente elogioso sem ressalvas, levando o classificador a prever `positivo`. |
| `cb15044c65145013e85587dafb8c9884` | 3 | `neutro` → `positivo` | "Amei, muito linda e bem feita. Atendeu minhas expectativas." | Expressão forte de satisfação ("Amei", "muito linda"), típica de notas 4 e 5. |

### 5.3 `negativo` → `neutro` (303 casos)

| `review_id` | Nota | Real → Previsto | Texto original | Interpretação |
|---|---|---|---|---|
| `f29bbead1034936360ff92f70abbe8f6` | 2 | `negativo` → `neutro` | "Produto demorou muito para chegar" | Reclamação curta sobre atraso sem termos de rejeição forte ("péssimo", "não recomendo"), deslocada para `neutro`. |
| `65002ef06d60405421812c7ee7d2e39a` | 1 | `negativo` → `neutro` | "Ainda estamos aguardando a chegada do produto" | Relato de não recebimento formulado em tom informativo ("aguardando"), que o modelo confunde com neutralidade. |
| `b7e7824518fc3524656a2ceffa220fa3` | 2 | `negativo` → `neutro` | "Loja boa mas tem muito problema com prazos... e acaba deixando a desejar" | Comentário misto combinando elogio inicial ("Loja boa") e crítica ("problema com prazos"), padrão frequente na classe neutra. |

### 5.4 `positivo` → `neutro` (440 casos)

| `review_id` | Nota | Real → Previsto | Texto original | Interpretação |
|---|---|---|---|---|
| `6433bd861bad9b6077d6cb47a5577594` | 4 | `positivo` → `neutro` | "Panela de boa qualidade, só faltou um puxador na panela que vai o pudim" | Elogio combinado com ressalva de peça faltante ("só faltou"), criando sinal misto entre positivo e negativo. |
| `062a50ab4cadfa7d5bc3c9d126413ebd` | 5 | `positivo` → `neutro` | "Ainda não testei" | Comentário curto e não avaliativo, muito próximo de relatos neutros de quem ainda aguarda uso ou entrega. |
| `e0d45295ba3e8bf652fecec118af4fde` | 4 | `positivo` → `neutro` | "O produto funciona bem, é um pouco duro os botões , demorou a entrega por ser final de ano, mas já comprei outros produtos e a entrega é qualidade são bons." | Avaliação balanceada com elogios e críticas pontuais ("demorou a entrega", "um pouco duro"), gerando previsão `neutro`. |

## 6. Implicação para o Painel de Voz do Cliente

Na regra do MVP implementada em `POST /triagem` (`src/api_triagem.py`), o campo `encaminhar_para_revisao` só recebe `true` quando a previsão é `negativo`. Isso significa que uma previsão `neutro` pode deixar uma reclamação real sem alerta automático.

No conjunto de teste, 303 avaliações negativas reais (`14,79%` das 2.049 negativas) foram classificadas como neutras, além de haver avaliações de nota 3 com relatos claros de falha operacional que também não recebem alerta quando previstas como neutras. Na demonstração local do painel, uma previsão neutra não garante ausência de problema no pedido e deve ser lida considerando essa limitação do modelo.
