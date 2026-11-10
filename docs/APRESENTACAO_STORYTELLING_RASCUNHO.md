# Apresentação final — Storytelling

## Slide 1 — Capa

**Drop Table — Projeto Aplicado II**

Análise de sentimentos em avaliações de e-commerce

Equipe:
Igor Eduardo Dallan do Couto  
Jaqueline de Oliveira Alves  
Kayo Oliveira Nukui  
Lucas de Lima Mendes

---

## Slide 2 — O problema

**Milhares de avaliações, mas quais problemas realmente importam?**

- notas mostram satisfação geral;
- comentários explicam o motivo;
- leitura manual não escala;
- a ConectaShop precisa transformar texto em informação.

Mensagem principal:

> Como identificar automaticamente clientes insatisfeitos e entender os principais motivos?

---

## Slide 3 — Os dados

**Base pública da Olist**

- 99.224 registros originais no arquivo de avaliações;
- 34.898 avaliações textuais válidas após tratamento;
- 61,57% positivas;
- 29,36% negativas;
- 9,07% neutras.

Visual sugerido:
`reports/figures/distribuicao_sentimentos_resumo.svg`

---

## Slide 4 — Preparação e método

**Do comentário ao modelo**

Fluxo:

Avaliação → limpeza → rótulo de sentimento → TF-IDF → Regressão Logística

- notas 1–2: negativo;
- nota 3: neutro;
- notas 4–5: positivo;
- 27.918 registros de treino;
- 6.980 registros de teste.

---

## Slide 5 — O modelo funciona?

**Resultado no conjunto de teste**

- acurácia: **80,40%**;
- F1 negativo: **80,69%**;
- recall negativo: **82,67%**;
- F1 positivo: **89,79%**;
- F1 neutro: **33,72%**.

Mensagem:

> O modelo identifica bem avaliações positivas e negativas, mas ainda encontra dificuldade com avaliações neutras.

Visual:
`reports/figures/desempenho_modelo.svg`

---

## Slide 6 — Otimização

**Testamos diferentes níveis de regularização**

- 9 valores de C;
- validação cruzada em 5 folds;
- critério: F1 da classe negativa;
- melhor configuração: **C = 1**.

Mensagem:

> A busca confirmou que o baseline já estava bem ajustado nesse parâmetro.

Visual:
`reports/figures/otimizacao_c.svg`

---

## Slide 7 — Por que os clientes estão insatisfeitos?

**Temas exploratórios nas avaliações negativas**

1. atraso ou não recebimento — **32,94%**;
2. atendimento, troca ou reembolso — **11,30%**;
3. defeito, avaria ou baixa qualidade — **7,63%**;
4. produto diferente do solicitado — **7,22%**;
5. pedido incompleto — **6,34%**.

Mensagem:

> Identificar o sentimento é útil, mas entender o motivo da insatisfação gera mais valor.

Visual:
`reports/figures/temas_insatisfacao.svg`

---

## Slide 8 — Produto proposto

**Painel de Voz do Cliente — ConectaShop**

O painel reúne:

- sentimento das avaliações;
- indicadores do classificador;
- principais temas negativos;
- informação para priorização de problemas.

Usuários:
Customer Experience, atendimento, operações e qualidade.

Visual:
captura do `produto/painel_voz_cliente.html`.

---

## Slide 9 — Impacto e limitações

**O que o projeto permite fazer**

- reduzir leitura manual;
- detectar padrões;
- priorizar investigações;
- transformar texto em informação.

**O que ainda precisamos considerar**

- sentimento aproximado pela nota;
- classe neutra com desempenho inferior;
- temas exploratórios;
- validação agrupada por pedido.

> Inserir aqui o resultado final da validação por `order_id` após execução local.

---

## Slide 10 — Conclusão

**De comentários dispersos para informação acionável**

- modelo com 80,40% de acurácia;
- F1 negativo acima de 80%;
- descoberta de temas recorrentes;
- proposta de produto aplicável ao negócio.

Próximos passos:

- validação humana dos temas;
- melhoria da classe neutra;
- integração com dados operacionais;
- dashboard interativo.

Final:

**GitHub:** lucasmendes94/Drop-Table-Projeto-Aplicado-II
