# Resultados preliminares e produto analítico

## Resultado do classificador

O modelo final avaliado no conjunto de teste apresentou:

- **Acurácia:** 80,40%;
- **Precisão da classe negativa:** 78,79%;
- **Recall da classe negativa:** 82,67%;
- **F1-score da classe negativa:** 80,69%;
- **F1-score macro:** 68,06%;
- **F1-score da classe neutra:** 33,72%.

O F1-score da classe negativa ficou acima da meta de 0,80 definida para o projeto. O principal ponto de atenção é a classe neutra, que apresentou desempenho consideravelmente inferior às classes negativa e positiva.

A busca de hiperparâmetro manteve **C = 1**, portanto não houve ganho em relação ao baseline com a alteração desse parâmetro.

## Temas recorrentes de insatisfação

A análise exploratória das 8.196 avaliações negativas do conjunto de treino identificou cinco temas recorrentes por regras lexicais orientadas pelos tópicos obtidos com NMF:

1. **Atraso ou não recebimento:** 2.700 menções (32,94%);
2. **Atendimento, troca ou reembolso:** 926 menções (11,30%);
3. **Defeito, avaria ou baixa qualidade:** 625 menções (7,63%);
4. **Produto diferente do solicitado:** 592 menções (7,22%);
5. **Pedido incompleto ou peças faltantes:** 520 menções (6,34%).

As categorias são multirrótulo e podem se sobrepor. Esses percentuais representam correspondências exploratórias na amostra de avaliações negativas de treino e não devem ser interpretados como taxas oficiais de falhas da operação.

## Produto gerado

Como produto analítico do projeto é proposto o **Painel de Voz do Cliente da ConectaShop**.

A proposta é transformar avaliações textuais em informações de apoio à decisão, reunindo:

- classificação automática do sentimento;
- distribuição de avaliações positivas, neutras e negativas;
- destaque das avaliações negativas;
- acompanhamento dos principais temas de insatisfação;
- indicadores para priorização de problemas recorrentes.

O produto pode ser apresentado inicialmente como um protótipo analítico, sem necessidade de implantação de um sistema transacional completo.

## Uso do produto

O painel seria utilizado principalmente por áreas de:

- Customer Experience;
- atendimento ao cliente;
- operações;
- qualidade;
- gestão.

Um gestor poderia, por exemplo, acompanhar o crescimento das avaliações negativas e identificar se as reclamações estão relacionadas principalmente a atraso, qualidade do produto, itens faltantes ou atendimento.

## Resultado preliminar de negócio

A principal descoberta da análise é que **atraso ou não recebimento aparece com grande destaque entre os temas identificados nas avaliações negativas**.

Isso indica uma oportunidade de priorizar investigações sobre logística e cumprimento de prazos. Ao mesmo tempo, atendimento/troca/reembolso e problemas de qualidade também aparecem como frentes relevantes.

A proposta não é substituir a análise humana, mas reduzir o volume de leitura manual e oferecer uma primeira triagem das avaliações.

## Limitações dos resultados

O modelo utiliza notas como aproximação do sentimento e a análise temática é exploratória. Os temas ainda não foram validados por uma amostra independente rotulada manualmente.

Assim, os resultados devem ser apresentados como apoio à decisão e geração de hipóteses, e não como diagnóstico definitivo da operação real da Olist.


## Protótipo disponível

O protótipo está disponível em [Painel de Voz do Cliente](../produto/painel_voz_cliente.html).

Ele consolida as principais métricas do classificador e os cinco temas exploratórios de insatisfação em uma visualização simples, servindo como evidência do produto gerado nesta etapa.
