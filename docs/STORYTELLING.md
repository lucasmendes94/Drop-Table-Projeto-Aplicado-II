# Esboço do storytelling

## 1. O problema

Uma operação de e-commerce pode receber milhares de avaliações de clientes. As notas ajudam a enxergar o nível geral de satisfação, mas os comentários possuem informações importantes que não são facilmente consolidadas manualmente.

A pergunta central do projeto é:

**Como transformar avaliações textuais em informações que ajudem uma empresa a identificar insatisfação e priorizar problemas?**

## 2. Os dados

Foi utilizado o conjunto público de dados da Olist, com foco nas avaliações de pedidos.

A base original possui 99.224 registros. Após o tratamento, 34.898 avaliações com conteúdo textual válido foram utilizadas na análise.

## 3. A preparação

Os textos foram normalizados, comentários vazios foram removidos e duplicidades ou rótulos conflitantes foram tratados.

As avaliações foram classificadas em três sentimentos a partir das notas:

- 1 e 2: negativo;
- 3: neutro;
- 4 e 5: positivo.

A base foi dividida em treino e teste de forma estratificada.

## 4. O modelo

Foi utilizado TF-IDF para representar os textos numericamente e regressão logística para classificar o sentimento.

O modelo alcançou **80,40% de acurácia** e **80,69% de F1-score para a classe negativa**.

A otimização do parâmetro C confirmou que o valor 1, já utilizado no baseline, era a melhor escolha dentro da grade testada para o objetivo definido.

## 5. A principal descoberta

A análise das avaliações negativas mostrou que o tema mais frequente entre as regras exploratórias foi **atraso ou não recebimento**, com 32,94% das avaliações negativas de treino apresentando correspondência.

Outros temas relevantes foram atendimento/troca/reembolso, defeitos ou baixa qualidade, produtos divergentes e pedidos incompletos.

## 6. Da análise para a decisão

Os resultados mostram que apenas classificar uma avaliação como negativa não é suficiente.

Para gerar valor de negócio, é necessário também ajudar a responder:

**Por que o cliente está insatisfeito?**

## 7. Produto proposto

A resposta do projeto é o **Painel de Voz do Cliente da ConectaShop**.

O painel combina sentimento e temas de insatisfação para facilitar a priorização de problemas por equipes de Customer Experience, atendimento e operações.

## 8. Valor gerado

O produto pode reduzir o esforço de leitura manual e ajudar a detectar problemas recorrentes mais rapidamente.

No cenário analisado, o destaque dado a atraso e não recebimento sugere que logística e cumprimento de prazo seriam uma frente prioritária de investigação.

## 9. Limitações

Os sentimentos foram derivados das notas e os temas são exploratórios, ainda sem validação humana independente.

A classe neutra também apresentou desempenho inferior, indicando espaço para novos experimentos.

## 10. Encerramento

O projeto demonstra que técnicas relativamente simples de processamento de texto e aprendizado de máquina podem transformar comentários dispersos em informação estruturada para apoiar decisões.

A próxima evolução seria validar os temas com rotulação humana, melhorar o tratamento da classe neutra e integrar o modelo a dados operacionais da empresa.
