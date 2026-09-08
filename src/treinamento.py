"""Treinamento do modelo-base de classificação de sentimentos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline


CLASSES = ["negativo", "neutro", "positivo"]


def carregar_conjunto(caminho: str | Path) -> pd.DataFrame:
    """Carrega e valida um conjunto preparado."""
    dados = pd.read_csv(caminho)
    obrigatorias = {"texto_limpo", "sentimento"}
    ausentes = sorted(obrigatorias.difference(dados.columns))
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(ausentes)}")
    if dados[list(obrigatorias)].isna().any().any():
        raise ValueError("O conjunto preparado contém texto ou sentimento nulo.")
    return dados


def criar_pipeline() -> Pipeline:
    """Cria o baseline TF-IDF + regressão logística balanceada."""
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.95,
                    sublinear_tf=True,
                    strip_accents="unicode",
                ),
            ),
            (
                "classificador",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def treinar_e_avaliar(
    caminho_treino: str | Path,
    caminho_teste: str | Path,
    diretorio_saida: str | Path,
) -> dict[str, object]:
    """Treina o modelo, avalia somente no teste e salva resultados reproduzíveis."""
    treino = carregar_conjunto(caminho_treino)
    teste = carregar_conjunto(caminho_teste)
    sobreposicao = set(treino["texto_limpo"]).intersection(teste["texto_limpo"])
    if sobreposicao:
        raise ValueError("Há textos repetidos entre treino e teste; possível vazamento.")

    modelo = criar_pipeline()
    modelo.fit(treino["texto_limpo"], treino["sentimento"])
    previsoes = modelo.predict(teste["texto_limpo"])

    relatorio = classification_report(
        teste["sentimento"],
        previsoes,
        labels=CLASSES,
        output_dict=True,
        zero_division=0,
    )
    metricas = {
        "acuracia": accuracy_score(teste["sentimento"], previsoes),
        "f1_negativo": relatorio["negativo"]["f1-score"],
        "relatorio_classificacao": relatorio,
        "matriz_confusao": confusion_matrix(
            teste["sentimento"], previsoes, labels=CLASSES
        ).tolist(),
        "ordem_classes_matriz": CLASSES,
        "linhas_treino": len(treino),
        "linhas_teste": len(teste),
    }

    saida = Path(diretorio_saida)
    saida.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, saida / "modelo_sentimento.joblib")
    (saida / "metricas_modelo.json").write_text(
        json.dumps(metricas, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    pd.DataFrame(
        {
            "review_id": teste.get("review_id", pd.Series(index=teste.index, dtype=str)),
            "sentimento_real": teste["sentimento"],
            "sentimento_previsto": previsoes,
        }
    ).to_csv(saida / "previsoes_teste.csv", index=False, encoding="utf-8")
    return metricas


def main() -> None:
    parser = argparse.ArgumentParser(description="Treina o classificador de sentimentos.")
    parser.add_argument("--treino", default="data/processed/treino.csv")
    parser.add_argument("--teste", default="data/processed/teste.csv")
    parser.add_argument("--saida", default="data/processed/modelo")
    argumentos = parser.parse_args()
    metricas = treinar_e_avaliar(argumentos.treino, argumentos.teste, argumentos.saida)
    print(json.dumps(metricas, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

