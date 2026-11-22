# Painel Operacional de CX — ConectaShop

## Objetivo

O Painel de Voz do Cliente transforma o classificador de sentimentos do projeto em um MVP operacional de triagem para equipes de Customer Experience.

Ele combina duas partes:

1. **referência histórica do modelo**, com métricas e temas de insatisfação já medidos no projeto;
2. **triagem de novas avaliações em tempo real**, utilizando a API local e o modelo treinado versionado no repositório.

## Arquitetura

O fluxo implementado é:

**Usuário → Painel HTML → POST /triagem → normalização do texto → modelo TF-IDF + Regressão Logística → sentimento previsto → decisão de revisão → fila da sessão**

Arquivos principais:

- `produto/painel_voz_cliente.html`: interface operacional;
- `src/api_triagem.py`: servidor HTTP e endpoint de classificação;
- `src/preparacao.py`: função de normalização textual;
- `data/processed/modelo/modelo_sentimento.joblib`: pipeline treinado;
- `tests/test_api_triagem.py`: testes de integração.

## Funcionamento da API

Ao iniciar:

```text
python -m src.api_triagem
```

o serviço carrega o modelo apenas uma vez e disponibiliza:

- `GET /`: painel HTML;
- `GET /health`: verificação simples de status;
- `POST /triagem`: classificação de uma nova avaliação.

Formato esperado:

```json
{
  "texto": "Produto chegou atrasado e com defeito."
}
```

Exemplo de resposta:

```json
{
  "sentimento": "negativo",
  "encaminhar_para_revisao": true
}
```

O campo `encaminhar_para_revisao` recebe `true` apenas quando o sentimento previsto é `negativo`.

## Recursos do painel

O painel implementa:

- campo para entrada manual de novas avaliações;
- exemplos rápidos para demonstração;
- classificação em positivo, neutro ou negativo;
- indicação de encaminhamento para revisão;
- contadores de avaliações triadas, encaminhadas e pendentes;
- fila de atendimento da sessão;
- filtro para exibir somente itens enviados para revisão;
- ação para marcar uma avaliação como tratada e reabri-la;
- indicadores históricos de acurácia, F1 e recall;
- visualização dos cinco temas exploratórios de insatisfação.

A fila existe apenas na memória do navegador enquanto a página está aberta. Não há persistência em banco de dados.

## Evidências e testes

A suíte `tests/test_api_triagem.py` cobre:

- carregamento do painel;
- presença do formulário e dos indicadores;
- classificação de exemplo negativo;
- classificação de exemplo positivo;
- várias classificações sucessivas;
- rejeição de texto vazio ou inválido;
- rejeição de JSON malformado.

Execução:

```text
python -m pytest -v tests/test_api_triagem.py
```

## Limitações observadas

### Classe neutra

A análise de erros mostrou F1 de 33,72% para a classe neutra.

No conjunto de teste, **303 avaliações negativas reais foram classificadas como neutras**, correspondendo a 14,79% das avaliações negativas reais. Como o MVP só gera alerta automático quando a previsão é negativa, algumas reclamações podem não ser encaminhadas.

Detalhes: `docs/ANALISE_ERROS_CLASSE_NEUTRA.md`.

### Variações de escrita

Durante os testes do grupo foi observado que pequenas variações linguísticas, como usar **"pra"** em vez de **"para"**, podem alterar a classificação de uma frase.

Isso é compatível com o funcionamento de um modelo baseado em TF-IDF: formas diferentes podem ocupar posições diferentes no vocabulário e ter pesos distintos.

Uma evolução possível é acrescentar uma etapa de normalização de abreviações, gírias e variantes comuns do português antes da vetorização. Essa melhoria não foi implementada nesta versão e, portanto, é registrada apenas como limitação/evolução possível.

## Escopo do MVP

O painel demonstra a aplicação do método analítico em uma operação de CX.

Ele não:

- armazena histórico de forma permanente;
- monitora automaticamente novas avaliações da Olist;
- substitui análise humana;
- corrige automaticamente previsões neutras;
- executa integração com sistemas externos.

Seu objetivo é comprovar, de forma reproduzível, como o modelo treinado pode ser utilizado para triagem contínua de novas avaliações.
