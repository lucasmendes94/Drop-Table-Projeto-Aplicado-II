"""Preparação reproduzível das avaliações textuais da Olist."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


COLUNAS_OBRIGATORIAS = {
    "review_id",
    "order_id",
    "review_score",
    "review_comment_title",
    "review_comment_message",
}
MAPA_SENTIMENTO = {
    1: "negativo",
    2: "negativo",
    3: "neutro",
    4: "positivo",
    5: "positivo",
}


def normalizar_texto(valor: object) -> str:
    """Normaliza o texto sem remover acentos nem palavras de negação."""
    if pd.isna(valor):
        return ""
    texto = unicodedata.normalize("NFKC", str(valor)).lower()
    texto = re.sub(r"https?://\S+|www\.\S+", " url ", texto)
    texto = re.sub(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b", " email ", texto)
    texto = re.sub(r"\d+", " numero ", texto)
    texto = re.sub(r"[^\w\sáàâãéèêíïóôõöúçñ]", " ", texto, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", texto).strip()


def carregar_avaliacoes(caminho: str | Path) -> pd.DataFrame:
    """Carrega o CSV e valida o esquema mínimo necessário."""
    dados = pd.read_csv(caminho, low_memory=False)
    ausentes = sorted(COLUNAS_OBRIGATORIAS.difference(dados.columns))
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(ausentes)}")
    return dados


def preparar_avaliacoes(dados: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    """Limpa avaliações, cria o rótulo e remove duplicidade/vazamento textual."""
    total_inicial = len(dados)
    trabalho = dados.loc[:, sorted(COLUNAS_OBRIGATORIAS)].copy()
    trabalho["review_score"] = pd.to_numeric(trabalho["review_score"], errors="coerce")
    trabalho = trabalho[trabalho["review_score"].isin(MAPA_SENTIMENTO)].copy()

    trabalho["titulo"] = trabalho["review_comment_title"].fillna("").astype(str)
    trabalho["comentario"] = trabalho["review_comment_message"].fillna("").astype(str)
    trabalho["texto_original"] = (
        trabalho["titulo"].str.strip() + " " + trabalho["comentario"].str.strip()
    ).str.strip()
    trabalho["texto_limpo"] = trabalho["texto_original"].map(normalizar_texto)
    trabalho["sentimento"] = trabalho["review_score"].astype(int).map(MAPA_SENTIMENTO)

    sem_texto = int(trabalho["texto_limpo"].eq("").sum())
    trabalho = trabalho[trabalho["texto_limpo"].ne("")].copy()

    # Textos iguais com rótulos diferentes geram supervisão ambígua e são excluídos.
    rotulos_por_texto = trabalho.groupby("texto_limpo")["sentimento"].nunique()
    textos_ambiguos = set(rotulos_por_texto[rotulos_por_texto > 1].index)
    linhas_ambiguas = int(trabalho["texto_limpo"].isin(textos_ambiguos).sum())
    trabalho = trabalho[~trabalho["texto_limpo"].isin(textos_ambiguos)].copy()

    antes_duplicatas = len(trabalho)
    trabalho = trabalho.drop_duplicates(subset=["texto_limpo", "sentimento"], keep="first")
    duplicatas = antes_duplicatas - len(trabalho)
    trabalho = trabalho.sort_values(["sentimento", "review_id"]).reset_index(drop=True)

    resumo = {
        "linhas_originais": total_inicial,
        "linhas_sem_texto": sem_texto,
        "linhas_com_texto_ambiguo": linhas_ambiguas,
        "duplicatas_textuais_removidas": duplicatas,
        "linhas_preparadas": len(trabalho),
        "distribuicao_sentimentos": trabalho["sentimento"].value_counts().to_dict(),
    }
    colunas_saida = [
        "review_id",
        "order_id",
        "review_score",
        "sentimento",
        "texto_original",
        "texto_limpo",
    ]
    return trabalho[colunas_saida], resumo


def dividir_base(
    dados: pd.DataFrame,
    proporcao_teste: float = 0.20,
    semente: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cria conjuntos estratificados e determinísticos de treino e teste."""
    treino, teste = train_test_split(
        dados,
        test_size=proporcao_teste,
        random_state=semente,
        stratify=dados["sentimento"],
    )
    return treino.reset_index(drop=True), teste.reset_index(drop=True)


def executar_preparacao(
    entrada: str | Path,
    diretorio_saida: str | Path,
    proporcao_teste: float = 0.20,
    semente: int = 42,
) -> dict[str, object]:
    """Executa a preparação e grava bases e relatório de qualidade."""
    saida = Path(diretorio_saida)
    saida.mkdir(parents=True, exist_ok=True)
    preparados, resumo = preparar_avaliacoes(carregar_avaliacoes(entrada))
    treino, teste = dividir_base(preparados, proporcao_teste, semente)

    preparados.to_csv(saida / "avaliacoes_preparadas.csv", index=False, encoding="utf-8")
    treino.to_csv(saida / "treino.csv", index=False, encoding="utf-8")
    teste.to_csv(saida / "teste.csv", index=False, encoding="utf-8")
    resumo.update(
        {
            "linhas_treino": len(treino),
            "linhas_teste": len(teste),
            "proporcao_teste": proporcao_teste,
            "semente_aleatoria": semente,
            "sobreposicao_textual_treino_teste": len(
                set(treino["texto_limpo"]).intersection(teste["texto_limpo"])
            ),
        }
    )
    (saida / "relatorio_preparacao.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return resumo


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepara as avaliações da Olist.")
    parser.add_argument(
        "--entrada",
        default="data/raw/olist_order_reviews_dataset.csv",
        help="Caminho do CSV bruto.",
    )
    parser.add_argument(
        "--saida", default="data/processed", help="Diretório dos dados preparados."
    )
    parser.add_argument("--teste", type=float, default=0.20, help="Proporção de teste.")
    parser.add_argument("--semente", type=int, default=42, help="Semente aleatória.")
    argumentos = parser.parse_args()
    resumo = executar_preparacao(
        argumentos.entrada, argumentos.saida, argumentos.teste, argumentos.semente
    )
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

