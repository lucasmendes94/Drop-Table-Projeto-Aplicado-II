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

**Milhares de avaliações, mas quais problemas realmente aparecem nos comentários?**

- notas resumem satisfação;
- comentários explicam a experiência;
- leitura manual dificulta consolidar grandes volumes;
- a ConectaShop precisa transformar texto em informação estruturada.

Pergunta do projeto:

**Como identificar automaticamente sentimentos e temas recorrentes de insatisfação?**

---

## Slide 3 — Da base bruta à base analisável

**Olist — avaliações de pedidos**

- 99.224 registros originais;
- 34.898 avaliações textuais válidas após o tratamento;
- 27.918 registros de treino;
- 6.980 registros de teste.

Classes:

- 61,57% positivas;
- 29,36% negativas;
- 9,07% neutras.

---

## Slide 4 — O método aplicado

**Pipeline reproduzível**

Avaliação → normalização → rótulo → TF-IDF → Regressão Logística

Rótulos:

- notas 1–2: negativo;
- nota 3: neutro;
- notas 4–5: positivo.

O TF-IDF é ajustado somente no conjunto de treino e o classificador usa balanceamento de classes.

---

## Slide 5 — Resultado do classificador

**Desempenho no teste**

- Acurácia: **80,40%**
- Precisão negativa: **78,79%**
- Recall negativo: **82,67%**
- F1 negativo: **80,69%**
- F1 positivo: **89,79%**
- F1 neutro: **33,72%**

Mensagem:

**O modelo apresentou bom desempenho nas classes positiva e negativa; a classe neutra foi a principal dificuldade observada.**

---

## Slide 6 — Otimização

**Qual regularização funcionou melhor?**

- 9 valores de C testados;
- 5 folds de validação cruzada;
- 45 ajustes executados;
- critério: F1 da classe negativa;
- melhor resultado: **C = 1**.

Conclusão:

**A otimização confirmou o parâmetro já utilizado no baseline.**

---

## Slide 7 — O que aparece nas avaliações negativas?

Foram analisadas 8.196 avaliações negativas do treino.

Principais temas exploratórios:

1. atraso ou não recebimento — **32,94%**;
2. atendimento, troca ou reembolso — **11,30%**;
3. defeito, avaria ou baixa qualidade — **7,63%**;
4. produto diferente do solicitado — **7,22%**;
5. pedido incompleto — **6,34%**.

Mensagem:

**Classificar o sentimento mostra quem está insatisfeito; analisar os temas ajuda a entender o motivo.**

---

## Slide 8 — Produto gerado

**Painel Operacional de CX — ConectaShop**

O produto integra o modelo treinado a uma API local e permite classificar novas avaliações em tempo real.

Fluxo:

**Avaliação → Painel → POST /triagem → normalização → modelo → sentimento → decisão de revisão**

O painel apresenta:

- indicadores históricos do modelo;
- cinco temas exploratórios de insatisfação;
- triagem manual de novas avaliações;
- fila de atendimento da sessão;
- contadores de itens triados, encaminhados e pendentes;
- ação para marcar uma avaliação como tratada.

Usuários:
Customer Experience, atendimento, qualidade e operações.

---

## Slide 9 — Limitações e aprendizado com os erros

- o classificador alcançou 80,40% de acurácia;
- a meta de F1 negativo acima de 0,80 foi atingida;
- a classe neutra teve F1 de **33,72%**;
- **303 avaliações negativas reais foram previstas como neutras**;
- previsões neutras não geram alerta automático no MVP;
- pequenas variações de escrita, como abreviações, podem alterar a classificação;
- os temas identificados são exploratórios e não equivalem a taxas oficiais de falha operacional.

Mensagem:

**O painel apoia a triagem, mas não substitui revisão humana em casos ambíguos.**

Todos os resultados apresentados possuem código e evidência correspondente no GitHub.

---

## Slide 10 — Encerramento

**De comentários dispersos para informação estruturada**

O projeto entregou:

- base tratada;
- método analítico aplicado;
- métricas de desempenho;
- otimização reproduzível;
- análise temática;
- Painel Operacional de CX integrado à API de triagem;
- análise de erros da classe neutra;
- testes de integração;
- documentação de reprodução e rastreabilidade.

**GitHub:** lucasmendes94/Drop-Table-Projeto-Aplicado-II
