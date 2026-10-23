"""Experimentos da Etapa 3: temas exploratórios e seleção de C somente no treino."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.decomposition import NMF
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import StratifiedKFold
from threadpoolctl import threadpool_limits

from .treinamento import carregar_conjunto, criar_pipeline


def salvar_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def temas(treino, saida, local):
    """NMF exploratória; exemplos permanecem locais para revisão qualitativa."""
    negativos = treino.loc[treino.sentimento.eq("negativo")].reset_index(drop=True)
    stop = "a ao aos as o os de da das do dos em um uma uns umas para por com que e se eu meu minha meus minhas foi ser estar esta esse essa isso ele ela eles elas muito mais mas como na nas no nos ja numero url email".split()
    vector = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=.90,
                            max_features=10000, strip_accents="unicode", stop_words=stop)
    x = vector.fit_transform(negativos.texto_limpo)
    model = NMF(n_components=5, init="nndsvda", random_state=42, max_iter=1000)
    weights = model.fit_transform(x)
    active = weights.sum(axis=1) > 0
    dominant = np.where(active, weights.argmax(axis=1), -1)
    words = vector.get_feature_names_out()
    summaries, examples = [], []
    for k in range(5):
        top = words[model.components_[k].argsort()[-20:][::-1]].tolist()
        summaries.append({"topico": k + 1, "termos": top,
                          "avaliacoes_dominantes": int((dominant == k).sum())})
        candidates = np.flatnonzero(dominant == k)
        indices = candidates[np.argsort(weights[candidates, k])[-12:][::-1]]
        examples.append({"topico": k + 1, "termos": top,
                         "exemplos": negativos.iloc[indices].texto_limpo.tolist()})
    salvar_json(saida / "topicos_nmf.json", {"escopo": "somente negativos do treino",
                "n": len(negativos), "sem_topico": int((~active).sum()), "topicos": summaries})
    salvar_json(local / "exemplos_topicos_revisao.json", examples)


def executar(args):
    saida, local = Path(args.saida), Path(args.local)
    saida.mkdir(parents=True, exist_ok=True)
    local.mkdir(parents=True, exist_ok=True)
    treino, teste = carregar_conjunto(args.treino), carregar_conjunto(args.teste)
    if set(treino.texto_limpo) & set(teste.texto_limpo):
        raise ValueError("Sobreposição textual entre treino e teste.")
    if treino.texto_limpo.duplicated().any():
        raise ValueError("Textos duplicados no treino.")
    if set(treino.sentimento) != {"negativo", "neutro", "positivo"}:
        raise ValueError("Classes inesperadas.")
    manifest = {"python": platform.python_version(), "sklearn": sklearn.__version__,
                "numpy": np.__version__, "pandas": pd.__version__, "seed": 42,
                "n_treino": len(treino), "n_teste": len(teste),
                "pedidos_compartilhados_treino_teste": len(set(treino["order_id"]) & set(teste["order_id"])) if "order_id" in treino and "order_id" in teste else None,
                "sha256": {Path(p).name: hashlib.sha256(Path(p).read_bytes()).hexdigest()
                           for p in (args.treino, args.teste)}}
    salvar_json(saida / "execucao.json", manifest)
    temas(treino, saida, local)
    if args.somente_temas:
        return
    cs = [.01, .03, .1, .3, 1., 3., 10., 30., 100.]
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    base = criar_pipeline()
    rows = []
    # Cada fold aprende seu próprio vocabulário. Reuso da mesma matriz entre Cs
    # equivale ao pipeline em busca em grade, sem refazer vetorização idêntica.
    for fold, (it, iv) in enumerate(folds.split(treino.texto_limpo, treino.sentimento), 1):
        vector = clone(base.named_steps["tfidf"])
        x = vector.fit_transform(treino.iloc[it].texto_limpo)
        xv = vector.transform(treino.iloc[iv].texto_limpo)
        for c in cs:
            model = clone(base.named_steps["classificador"]).set_params(C=c)
            model.fit(x, treino.iloc[it].sentimento)
            pred = model.predict(xv)
            y = treino.iloc[iv].sentimento
            rows.append({"fold": fold, "C": c,
                         "f1_negativo": f1_score(y, pred, labels=["negativo"], average="macro"),
                         "f1_macro": f1_score(y, pred, average="macro")})
            print(json.dumps(rows[-1]), flush=True)
        pd.DataFrame(rows).to_csv(saida / "validacao_folds.csv", index=False)
    summary = pd.DataFrame(rows).groupby("C").agg(
        f1_negativo_media=("f1_negativo", "mean"),
        f1_negativo_desvio=("f1_negativo", "std"),
        f1_macro_media=("f1_macro", "mean")).reset_index()
    summary.to_csv(saida / "comparacao_c.csv", index=False)
    # Critério pré-definido: maior F1 negativo médio; empate favorece menor C.
    best = float(summary.sort_values(["f1_negativo_media", "C"], ascending=[False, True]).iloc[0].C)
    results = {"criterio": "maior F1 negativo médio nos 5 folds de treino",
               "melhor_C": best, "teste_ja_utilizado_na_etapa2": True, "modelos": {}}
    for label, c in (("baseline", 1.), ("otimizado", best)):
        model = criar_pipeline().set_params(classificador__C=c)
        model.fit(treino.texto_limpo, treino.sentimento)
        pred = model.predict(teste.texto_limpo)
        results["modelos"][label] = {"C": c, "metricas": classification_report(
            teste.sentimento, pred, output_dict=True, zero_division=0)}
        if label == "otimizado":
            joblib.dump(model, local / "modelo_c_otimizado.joblib")
    salvar_json(saida / "comparacao_teste.json", results)
    print(json.dumps(results, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--treino", default="data/processed/treino.csv")
    parser.add_argument("--teste", default="data/processed/teste.csv")
    parser.add_argument("--saida", default="reports/etapa3")
    parser.add_argument("--local", default="data/processed/etapa3")
    parser.add_argument("--somente-temas", action="store_true")
    args = parser.parse_args()
    warnings.filterwarnings("error", category=ConvergenceWarning)
    with threadpool_limits(limits=2):
        executar(args)


if __name__ == "__main__":
    main()
