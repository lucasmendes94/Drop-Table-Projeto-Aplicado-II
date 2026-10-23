"""Etapa 3: validação operacional, calibração e limiares da classe negativa.

Execução a partir da raiz do projeto:
    python -m src.etapa3_validacao
"""
from __future__ import annotations

import argparse
import json
import unicodedata
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss
from sklearn.model_selection import StratifiedGroupKFold
from threadpoolctl import threadpool_limits

from .treinamento import carregar_conjunto, criar_pipeline

SEMENTE = 42
GRADE_LIMIARES = np.round(np.arange(0.05, 0.951, 0.01), 2)
RECALL_MINIMO = 0.85
PRECISAO_MINIMA = 0.80
N_BOOTSTRAP = 1000
N_FAIXAS = 10

def salvar_json(caminho, valor):
    Path(caminho).write_text(
        json.dumps(valor, ensure_ascii=False, indent=2, default=float), encoding="utf-8"
    )


def sem_acentos(texto: str) -> str:
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def metricas_binarias(y, previsto, pesos=None) -> dict[str, float]:
    w = np.ones(len(y)) if pesos is None else pesos
    vp = float((w * (y & previsto)).sum())
    fp = float((w * (~y & previsto)).sum())
    fn = float((w * (y & ~previsto)).sum())
    precisao = vp / (vp + fp) if vp + fp else 0.0
    recall = vp / (vp + fn) if vp + fn else 0.0
    f1 = 2 * precisao * recall / (precisao + recall) if precisao + recall else 0.0
    return {"precisao": precisao, "recall": recall, "f1": f1,
            "vp": vp, "fp": fp, "fn": fn}


def ece(y, p, n_faixas: int = N_FAIXAS) -> float:
    faixas = pd.qcut(pd.Series(p).rank(method="first"), n_faixas, labels=False)
    total = 0.0
    for k in range(n_faixas):
        m = (faixas == k).to_numpy()
        if m.any():
            total += m.mean() * abs(y[m].mean() - p[m].mean())
    return float(total)


def tabela_confiabilidade(y, p, n_faixas: int = N_FAIXAS) -> pd.DataFrame:
    faixas = pd.qcut(pd.Series(p).rank(method="first"), n_faixas, labels=False)
    linhas = []
    for k in range(n_faixas):
        m = (faixas == k).to_numpy()
        linhas.append({"faixa": k + 1, "n": int(m.sum()),
                       "prob_media_prevista": float(p[m].mean()),
                       "frequencia_observada": float(y[m].mean())})
    return pd.DataFrame(linhas)


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


class CalibradorSigmoide:

    def fit(self, p, y):
        self.m = LogisticRegression(C=1e6, max_iter=1000).fit(logit(p).reshape(-1, 1), y)
        return self

    def predict(self, p):
        return self.m.predict_proba(logit(p).reshape(-1, 1))[:, 1]


class CalibradorIsotonico:
    def fit(self, p, y):
        self.m = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(p, y)
        return self

    def predict(self, p):
        return self.m.predict(p)


def brier_validacao_cruzada(classe_calibrador, p, y, pedidos) -> float:
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    previsto = np.zeros(len(p))
    for ti, vi in cv.split(p, y, pedidos):
        previsto[vi] = classe_calibrador().fit(p[ti], y[ti]).predict(p[vi])
    return float(brier_score_loss(y, previsto))


def resumo_calibracao(y, p) -> dict[str, float]:
    p_seguro = np.clip(p, 1e-6, 1 - 1e-6)
    return {"brier": float(brier_score_loss(y, p)), "ece": ece(y, p),
            "log_loss": float(log_loss(y, p_seguro)), "prob_media": float(p.mean()),
            "frequencia_real": float(y.mean())}


# ----------------------------------------------------------------- divisões
def dividir_por_pedido(base: pd.DataFrame):
    y, g = base["sentimento"], base["order_id"]
    externo = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    resto_idx, teste_idx = next(externo.split(base, y, g))
    resto = base.iloc[resto_idx]
    interno = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=SEMENTE)
    aj, va = next(interno.split(resto, resto["sentimento"], resto["order_id"]))
    return resto.iloc[aj].reset_index(drop=True), resto.iloc[va].reset_index(drop=True), \
        base.iloc[teste_idx].reset_index(drop=True)


def probabilidade_negativo(modelo, textos) -> np.ndarray:
    classes = list(modelo.named_steps["classificador"].classes_)
    return modelo.predict_proba(textos)[:, classes.index("negativo")]


# -------------------------------------------------------------------- etapas
def auditar(treino, teste) -> dict:
    compartilhados = sorted(set(treino["order_id"]) & set(teste["order_id"]))
    chave_t = set(treino["texto_limpo"].map(sem_acentos))
    colisoes = teste["texto_limpo"].map(sem_acentos).isin(chave_t)
    return {
        "pedidos_compartilhados": len(compartilhados),
        "avaliacoes_teste_em_pedidos_compartilhados": int(teste["order_id"].isin(compartilhados).sum()),
        "avaliacoes_treino_em_pedidos_compartilhados": int(treino["order_id"].isin(compartilhados).sum()),
        "teste_com_texto_igual_ao_treino_sem_acentos": int(colisoes.sum()),
        "pedidos_com_mais_de_uma_avaliacao_na_base": int(
            pd.concat([treino, teste])["order_id"].value_counts().gt(1).sum()),
        "_lista": compartilhados,
    }


def reavaliar_etapa2_sem_compartilhados(treino, teste, compartilhados) -> dict:
    modelo = criar_pipeline().fit(treino["texto_limpo"], treino["sentimento"])
    saida = {}
    for rotulo, sub in (("teste_completo", teste),
                        ("teste_sem_pedidos_compartilhados",
                         teste[~teste["order_id"].isin(compartilhados)])):
        prev = modelo.predict(sub["texto_limpo"])
        y = (sub["sentimento"] == "negativo").to_numpy()
        m = metricas_binarias(y, np.asarray(prev == "negativo"))
        saida[rotulo] = {"n": len(sub), "f1_negativo": m["f1"], "precisao": m["precisao"],
                         "recall": m["recall"], "acuracia": float((prev == sub["sentimento"]).mean())}
    return saida


def cv_agrupada(base) -> dict:
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    f1s = []
    for ti, vi in cv.split(base, base["sentimento"], base["order_id"]):
        m = criar_pipeline().fit(base.iloc[ti]["texto_limpo"], base.iloc[ti]["sentimento"])
        prev = m.predict(base.iloc[vi]["texto_limpo"])
        y = (base.iloc[vi]["sentimento"] == "negativo").to_numpy()
        f1s.append(metricas_binarias(y, np.asarray(prev == "negativo"))["f1"])
    return {"f1_negativo_por_particao": f1s, "media": float(np.mean(f1s)),
            "desvio_amostral": float(np.std(f1s, ddof=1)), "minimo": float(np.min(f1s)),
            "particoes_abaixo_de_0_80": int(sum(f < 0.80 for f in f1s))}


def escolher_limiares(y_val, p_val) -> pd.DataFrame:
    linhas = []
    for t in GRADE_LIMIARES:
        m = metricas_binarias(y_val, p_val >= t)
        linhas.append({"limiar": float(t), **{k: m[k] for k in ("precisao", "recall", "f1")}})
    grade = pd.DataFrame(linhas)
    escolhas = {}
    escolhas["f1_maximo"] = grade.sort_values(["f1", "limiar"], ascending=[False, True]).iloc[0].limiar
    ok = grade[grade.recall >= RECALL_MINIMO]
    escolhas[f"recall_minimo_{RECALL_MINIMO:.2f}"] = (
        ok.sort_values(["precisao", "limiar"], ascending=[False, False]).iloc[0].limiar if len(ok) else np.nan)
    ok = grade[grade.precisao >= PRECISAO_MINIMA]
    escolhas[f"precisao_minima_{PRECISAO_MINIMA:.2f}"] = (
        ok.sort_values(["recall", "limiar"], ascending=[False, True]).iloc[0].limiar if len(ok) else np.nan)
    grade.attrs["escolhas"] = {k: (None if np.isnan(v) else float(v)) for k, v in escolhas.items()}
    return grade


def bootstrap_por_pedido(y, previsto, pedidos, n=N_BOOTSTRAP) -> dict:
    codigos, _ = pd.factorize(pedidos)
    n_ped = codigos.max() + 1
    rng = np.random.default_rng(SEMENTE)
    f1, pr, rc = [], [], []
    for _ in range(n):
        pesos = np.bincount(rng.integers(0, n_ped, n_ped), minlength=n_ped)[codigos].astype(float)
        m = metricas_binarias(y, previsto, pesos)
        f1.append(m["f1"]); pr.append(m["precisao"]); rc.append(m["recall"])
    def ic(v):
        return {"p2_5": float(np.percentile(v, 2.5)), "mediana": float(np.percentile(v, 50)),
                "p97_5": float(np.percentile(v, 97.5))}
    f1 = np.array(f1)
    return {"f1": ic(f1), "precisao": ic(pr), "recall": ic(rc),
            "proporcao_f1_abaixo_de_0_80": float((f1 < 0.80).mean())}


def figuras(saida, y_te, probas_te, grade_val, escolhas):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="calibração perfeita")
    for nome, p in probas_te.items():
        t = tabela_confiabilidade(y_te, p)
        ax.plot(t.prob_media_prevista, t.frequencia_observada, "o-", ms=4, label=nome)
    ax.set_xlabel("Probabilidade média prevista de negativo")
    ax.set_ylabel("Frequência observada de negativo")
    ax.set_title("Curva de confiabilidade (teste)")
    ax.legend(); fig.tight_layout()
    fig.savefig(saida / "confiabilidade_teste.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    for col, nome in (("precisao", "Precisão"), ("recall", "Recall"), ("f1", "F1")):
        ax.plot(grade_val.limiar, grade_val[col], label=nome)
    for nome, t in escolhas.items():
        if t is not None:
            ax.axvline(t, ls=":", lw=1, color="gray")
    ax.set_xlabel("Limiar de probabilidade calibrada"); ax.set_ylabel("Métrica (validação)")
    ax.set_title("Limiares na validação (linhas: critérios)")
    ax.legend(); fig.tight_layout()
    fig.savefig(saida / "limiares_validacao.png", dpi=150); plt.close(fig)


def executar(args):
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    treino, teste = carregar_conjunto(args.treino), carregar_conjunto(args.teste)
    for col in ("order_id",):
        if col not in treino or col not in teste:
            raise ValueError(f"Coluna obrigatória ausente: {col}")
    resultados: dict = {"semente": SEMENTE}

    # 1-2. auditoria e reavaliação da Etapa 2
    auditoria = auditar(treino, teste)
    compartilhados = auditoria.pop("_lista")
    resultados["auditoria"] = auditoria
    resultados["etapa2_sem_pedidos_compartilhados"] = reavaliar_etapa2_sem_compartilhados(
        treino, teste, compartilhados)

    # 3. divisão agrupada por pedido
    base = pd.concat([treino, teste], ignore_index=True)
    aj, va, te = dividir_por_pedido(base)
    for a, b, n in ((aj, va, "ajuste/validação"), (aj, te, "ajuste/teste"), (va, te, "validação/teste")):
        if set(a["order_id"]) & set(b["order_id"]):
            raise ValueError(f"Pedido repetido entre {n}.")
    resultados["divisao_por_pedido"] = {
        c: {"n": len(d), **d["sentimento"].value_counts().to_dict()}
        for c, d in (("ajuste", aj), ("validacao", va), ("teste", te))}

    modelo = criar_pipeline().fit(aj["texto_limpo"], aj["sentimento"])
    y_va = (va["sentimento"] == "negativo").to_numpy()
    y_te = (te["sentimento"] == "negativo").to_numpy()
    p_va, p_te = probabilidade_negativo(modelo, va["texto_limpo"]), probabilidade_negativo(modelo, te["texto_limpo"])
    prev_te = modelo.predict(te["texto_limpo"])
    prev_neg_te = np.asarray(prev_te == "negativo")
    resultados["modelo_atual_teste_agrupado"] = {
        **metricas_binarias(y_te, prev_neg_te),
        "acuracia": float((prev_te == te["sentimento"]).mean()),
        "bootstrap_por_pedido": bootstrap_por_pedido(y_te, prev_neg_te, te["order_id"].to_numpy())}

    # 4. validação cruzada agrupada
    resultados["cv_agrupada_por_pedido"] = cv_agrupada(base)

    # 5. calibração (ajustada só na validação)
    calibradores = {"sigmoide": CalibradorSigmoide().fit(p_va, y_va),
                    "isotonica": CalibradorIsotonico().fit(p_va, y_va)}
    probas_va = {"bruta": p_va, **{k: c.predict(p_va) for k, c in calibradores.items()}}
    probas_te = {"bruta": p_te, **{k: c.predict(p_te) for k, c in calibradores.items()}}
    resultados["calibracao"] = {
        "validacao_(ajuste_dos_calibradores)": {k: resumo_calibracao(y_va, p) for k, p in probas_va.items()},
        "teste": {k: resumo_calibracao(y_te, p) for k, p in probas_te.items()}}

    brier_cv = {k: brier_validacao_cruzada(c.__class__, p_va, y_va, va["order_id"].to_numpy())
                for k, c in calibradores.items()}
    resultados["calibracao"]["brier_validacao_ajuste_cruzado"] = brier_cv
    escolhido = "sigmoide" if brier_cv["sigmoide"] <= brier_cv["isotonica"] * 1.02 else "isotonica"
    resultados["calibrador_escolhido"] = escolhido
    for k, p in probas_te.items():
        tabela_confiabilidade(y_te, p).to_csv(saida / f"confiabilidade_teste_{k}.csv", index=False)

    # 6. limiares: escolha na validação, aplicação ao teste
    p_val_cal, p_te_cal = probas_va[escolhido], probas_te[escolhido]
    grade = escolher_limiares(y_va, p_val_cal)
    grade.to_csv(saida / "limiares_validacao.csv", index=False)
    escolhas = grade.attrs["escolhas"]
    linhas, pedidos_te = [], te["order_id"].to_numpy()
    for criterio, t in escolhas.items():
        if t is None:
            linhas.append({"criterio": criterio, "limiar": None}); continue
        previsto = p_te_cal >= t
        m = metricas_binarias(y_te, previsto)
        bs = bootstrap_por_pedido(y_te, previsto, pedidos_te)
        linhas.append({"criterio": criterio, "limiar": t, "precisao_teste": m["precisao"],
                       "recall_teste": m["recall"], "f1_teste": m["f1"],
                       "alertas_por_1000": 1000 * float(previsto.mean()),
                       "queixas_encontradas_por_1000": 1000 * m["vp"] / len(y_te),
                       "alertas_falsos_por_1000": 1000 * m["fp"] / len(y_te),
                       "f1_ic95_inf": bs["f1"]["p2_5"], "f1_ic95_sup": bs["f1"]["p97_5"],
                       "prop_bootstrap_f1_abaixo_0_80": bs["proporcao_f1_abaixo_de_0_80"]})
    pd.DataFrame(linhas).to_csv(saida / "limiares_teste.csv", index=False)
    resultados["limiares"] = {"calibrador": escolhido, "criterios": escolhas, "teste": linhas}

    salvar_json(saida / "validacao_operacional.json", resultados)
    if not args.sem_figuras:
        figuras(saida, y_te, {"bruta": p_te, "sigmoide": probas_te["sigmoide"],
                              "isotônica": probas_te["isotonica"]}, grade, escolhas)
    print(json.dumps(resultados, ensure_ascii=False, indent=2, default=float))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--treino", default="data/processed/treino.csv")
    parser.add_argument("--teste", default="data/processed/teste.csv")
    parser.add_argument("--saida", default="reports/etapa3/validacao_operacional")
    parser.add_argument("--sem-figuras", action="store_true")
    args = parser.parse_args()
    warnings.filterwarnings("error", category=ConvergenceWarning)
    with threadpool_limits(limits=2):
        executar(args)


if __name__ == "__main__":
    main()
