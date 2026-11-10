"""Análise exploratória final e figuras para relatório/apresentação.

Usa somente os conjuntos processados já preparados pelo projeto.
Execução:
    python -m src.eda_final
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .treinamento import carregar_conjunto

STOPWORDS = {
    "a","ao","aos","as","o","os","de","da","das","do","dos","e","em","um","uma",
    "uns","umas","para","por","com","que","se","eu","meu","minha","meus","minhas",
    "foi","ser","estar","esta","esse","essa","isso","ele","ela","eles","elas","muito",
    "mais","mas","como","na","nas","no","nos","ja","numero","url","email"
}


def salvar_json(caminho: Path, valor: dict) -> None:
    caminho.write_text(json.dumps(valor, ensure_ascii=False, indent=2), encoding="utf-8")


def juntar_bases(treino: pd.DataFrame, teste: pd.DataFrame) -> pd.DataFrame:
    base = pd.concat([treino, teste], ignore_index=True)
    if base["texto_limpo"].duplicated().any():
        raise ValueError("A base combinada contém texto duplicado.")
    return base


def top_termos(textos: pd.Series, n: int = 15) -> list[tuple[str, int]]:
    contagem = Counter()
    for texto in textos.astype(str):
        tokens = [
            token for token in texto.split()
            if len(token) > 2 and token not in STOPWORDS
        ]
        contagem.update(tokens)
    return contagem.most_common(n)


def gerar_figuras(base: pd.DataFrame, saida: Path) -> dict:
    saida.mkdir(parents=True, exist_ok=True)

    resumo = {
        "n_total": int(len(base)),
        "distribuicao_sentimento": {
            str(k): int(v) for k, v in base["sentimento"].value_counts().to_dict().items()
        },
        "distribuicao_notas": {
            str(int(k)): int(v)
            for k, v in base["review_score"].value_counts().sort_index().to_dict().items()
        },
    }

    # 1. Distribuição das notas
    notas = base["review_score"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([str(int(x)) for x in notas.index], notas.values)
    ax.set_title("Distribuição das notas das avaliações")
    ax.set_xlabel("Nota")
    ax.set_ylabel("Quantidade de avaliações")
    fig.tight_layout()
    fig.savefig(saida / "distribuicao_notas.png", dpi=180)
    plt.close(fig)

    # 2. Distribuição dos sentimentos
    ordem = ["negativo", "neutro", "positivo"]
    sentimentos = base["sentimento"].value_counts().reindex(ordem, fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(sentimentos.index, sentimentos.values)
    ax.set_title("Distribuição das classes de sentimento")
    ax.set_xlabel("Sentimento")
    ax.set_ylabel("Quantidade de avaliações")
    fig.tight_layout()
    fig.savefig(saida / "distribuicao_sentimentos.png", dpi=180)
    plt.close(fig)

    # 3. Comprimento dos comentários por sentimento
    aux = base[["sentimento", "texto_limpo"]].copy()
    aux["n_palavras"] = aux["texto_limpo"].astype(str).str.split().str.len()
    limite = float(aux["n_palavras"].quantile(0.99))
    dados_box = [
        aux.loc[(aux.sentimento == classe) & (aux.n_palavras <= limite), "n_palavras"].to_numpy()
        for classe in ordem
    ]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.boxplot(dados_box, tick_labels=ordem, showfliers=False)
    ax.set_title("Comprimento dos comentários por sentimento")
    ax.set_xlabel("Sentimento")
    ax.set_ylabel("Quantidade de palavras")
    fig.tight_layout()
    fig.savefig(saida / "comprimento_comentarios.png", dpi=180)
    plt.close(fig)

    resumo["comprimento_palavras"] = {
        classe: {
            "mediana": float(aux.loc[aux.sentimento == classe, "n_palavras"].median()),
            "media": float(aux.loc[aux.sentimento == classe, "n_palavras"].mean()),
        }
        for classe in ordem
    }

    # 4-6. Termos mais frequentes por sentimento
    resumo["top_termos"] = {}
    for classe in ordem:
        termos = top_termos(base.loc[base.sentimento == classe, "texto_limpo"])
        resumo["top_termos"][classe] = [{"termo": t, "frequencia": int(f)} for t, f in termos]
        if termos:
            nomes = [t for t, _ in termos][::-1]
            valores = [f for _, f in termos][::-1]
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(nomes, valores)
            ax.set_title(f"Termos mais frequentes — {classe}")
            ax.set_xlabel("Frequência")
            fig.tight_layout()
            fig.savefig(saida / f"top_termos_{classe}.png", dpi=180)
            plt.close(fig)

    salvar_json(saida / "eda_resumo.json", resumo)
    return resumo


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--treino", default="data/processed/treino.csv")
    parser.add_argument("--teste", default="data/processed/teste.csv")
    parser.add_argument("--saida", default="reports/figures")
    args = parser.parse_args()

    treino = carregar_conjunto(args.treino)
    teste = carregar_conjunto(args.teste)
    base = juntar_bases(treino, teste)
    resumo = gerar_figuras(base, Path(args.saida))
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
