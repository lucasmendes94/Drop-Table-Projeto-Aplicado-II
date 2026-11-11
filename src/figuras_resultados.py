"""Gera figuras a partir das evidências versionadas do projeto.

Este script não treina modelos. Ele apenas transforma arquivos de resultados já
versionados em gráficos para relatório e apresentação.

Execução:
    python -m src.figuras_resultados
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
RESULTADOS = RAIZ / "reports" / "etapa3"
SAIDA = RAIZ / "reports" / "figures"


def grafico_metricas() -> None:
    dados = json.loads((RESULTADOS / "comparacao_teste.json").read_text(encoding="utf-8"))
    metricas = dados["modelos"]["baseline"]["metricas"]

    nomes = ["Acurácia", "F1 negativo", "Recall negativo", "F1 macro", "F1 neutro", "F1 positivo"]
    valores = [
        metricas["accuracy"],
        metricas["negativo"]["f1-score"],
        metricas["negativo"]["recall"],
        metricas["macro avg"]["f1-score"],
        metricas["neutro"]["f1-score"],
        metricas["positivo"]["f1-score"],
    ]

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(nomes[::-1], [100 * v for v in valores[::-1]])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percentual")
    ax.set_title("Desempenho do classificador no conjunto de teste")
    for i, v in enumerate(valores[::-1]):
        ax.text(100 * v + 1, i, f"{100*v:.2f}%".replace(".", ","), va="center")
    fig.tight_layout()
    fig.savefig(SAIDA / "desempenho_modelo.png", dpi=180)
    plt.close(fig)


def grafico_c() -> None:
    dados = pd.read_csv(RESULTADOS / "comparacao_c.csv")

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.semilogx(dados["C"], 100 * dados["f1_negativo_media"], marker="o")
    ax.set_xlabel("Parâmetro C")
    ax.set_ylabel("F1 negativo médio (%)")
    ax.set_title("Validação cruzada do parâmetro C")
    melhor = dados.loc[dados["f1_negativo_media"].idxmax()]
    ax.annotate(
        f"Melhor: C = {melhor['C']:g}",
        (melhor["C"], 100 * melhor["f1_negativo_media"]),
        xytext=(8, 10),
        textcoords="offset points",
    )
    fig.tight_layout()
    fig.savefig(SAIDA / "otimizacao_c.png", dpi=180)
    plt.close(fig)


def grafico_temas() -> None:
    dados = pd.read_csv(RESULTADOS / "cinco_temas.csv").sort_values(
        "percentual_negativos_treino"
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(dados["tema"], dados["percentual_negativos_treino"])
    ax.set_xlabel("% das avaliações negativas de treino")
    ax.set_title("Temas exploratórios de insatisfação")
    for i, v in enumerate(dados["percentual_negativos_treino"]):
        ax.text(v + 0.4, i, f"{v:.2f}%".replace(".", ","), va="center")
    fig.tight_layout()
    fig.savefig(SAIDA / "temas_insatisfacao.png", dpi=180)
    plt.close(fig)


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    grafico_metricas()
    grafico_c()
    grafico_temas()
    print(f"Figuras geradas em {SAIDA}")


if __name__ == "__main__":
    main()
