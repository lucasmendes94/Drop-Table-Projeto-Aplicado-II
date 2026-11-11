# Rastreabilidade dos resultados

Este documento liga cada resultado apresentado no relatório ao código que o produz e à evidência versionada no repositório.

## Regra adotada

Um número só deve aparecer no relatório final quando existir:

1. código reproduzível no repositório;
2. evidência de execução versionada ou documentação técnica correspondente;
3. comando de reprodução definido.

## Matriz de rastreabilidade

| Resultado apresentado | Código responsável | Evidência versionada | Reprodução |
|---|---|---|---|
| 99.224 linhas originais; 34.898 avaliações textuais válidas | `src/preparacao.py` | `docs/TRATAMENTO_BASE_DADOS.md` | `python -m src.preparacao` |
| 27.918 registros de treino e 6.980 de teste | `src/preparacao.py` | `reports/etapa3/execucao.json` | `python -m src.preparacao` |
| Classes: 21.488 positivas, 10.245 negativas e 3.165 neutras | `src/preparacao.py` | `docs/TRATAMENTO_BASE_DADOS.md` | `python -m src.preparacao` |
| Acurácia de 80,40% | `src/treinamento.py` / `src/etapa3.py` | `reports/etapa3/comparacao_teste.json` | `python -m src.treinamento` e `python -m src.etapa3` |
| Precisão negativa de 78,79% | `src/treinamento.py` / `src/etapa3.py` | `reports/etapa3/comparacao_teste.json` | mesmos comandos |
| Recall negativo de 82,67% | `src/treinamento.py` / `src/etapa3.py` | `reports/etapa3/comparacao_teste.json` | mesmos comandos |
| F1 negativo de 80,69% | `src/treinamento.py` / `src/etapa3.py` | `reports/etapa3/comparacao_teste.json` | mesmos comandos |
| F1 macro de 68,06% | `src/etapa3.py` | `reports/etapa3/comparacao_teste.json` | `python -m src.etapa3` |
| F1 neutro de 33,72% | `src/etapa3.py` | `reports/etapa3/comparacao_teste.json` | `python -m src.etapa3` |
| F1 positivo de 89,79% | `src/etapa3.py` | `reports/etapa3/comparacao_teste.json` | `python -m src.etapa3` |
| Comparação de 9 valores de C em 5 folds | `src/etapa3.py` | `reports/etapa3/comparacao_c.csv` e `validacao_folds.csv` | `python -m src.etapa3` |
| Melhor C = 1; F1 negativo médio ≈ 80,34% | `src/etapa3.py` | `reports/etapa3/comparacao_c.csv` | `python -m src.etapa3` |
| 8.196 avaliações negativas analisadas na etapa temática | `src/etapa3.py` / `src/temas_insatisfacao.py` | `reports/etapa3/topicos_nmf.json` e `cinco_temas.json` | `python -m src.etapa3` e `python -m src.temas_insatisfacao` |
| Atraso ou não recebimento: 2.700 menções / 32,94% | `src/temas_insatisfacao.py` | `reports/etapa3/cinco_temas.json` | `python -m src.temas_insatisfacao` |
| Atendimento/troca/reembolso: 926 / 11,30% | `src/temas_insatisfacao.py` | `reports/etapa3/cinco_temas.json` | mesmo comando |
| Defeito/avaria/baixa qualidade: 625 / 7,63% | `src/temas_insatisfacao.py` | `reports/etapa3/cinco_temas.json` | mesmo comando |
| Produto diferente: 592 / 7,22% | `src/temas_insatisfacao.py` | `reports/etapa3/cinco_temas.json` | mesmo comando |
| Pedido incompleto: 520 / 6,34% | `src/temas_insatisfacao.py` | `reports/etapa3/cinco_temas.json` | mesmo comando |
| 4.661 avaliações com ao menos um tema; 649 multirrótulo | `src/temas_insatisfacao.py` | `reports/etapa3/cinco_temas.json` | mesmo comando |
| 19 pedidos compartilhados entre treino e teste | `src/etapa3.py` | `reports/etapa3/execucao.json` | `python -m src.etapa3` |

## Integridade dos conjuntos usados nos experimentos

A execução versionada registra os hashes SHA-256 dos conjuntos processados:

- `treino.csv`: `95b5878d846571ba7cd6bd2204b8c6fd1efbf11733fb723cf7be38468db89f2b`
- `teste.csv`: `9f8ff8c1671018ac59795e7a87ec6550b7ffea447031bce3fad973a2e5f59d4e`

Esses hashes constam em `reports/etapa3/execucao.json` e permitem confirmar que uma reprodução está utilizando os mesmos conjuntos dos experimentos documentados.

## Resultados que não entram na entrega final

Código ou análise que não possua evidência de execução não deve ser apresentado como fase concluída nem como resultado no relatório final.
