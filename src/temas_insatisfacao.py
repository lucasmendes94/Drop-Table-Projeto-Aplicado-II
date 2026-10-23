"""Codificação exploratória multirrótulo das avaliações negativas de treino."""
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd


# Categorias interpretadas a partir dos termos e exemplos da NMF. Uma avaliação
# pode mencionar vários problemas. Correspondência lexical não é rótulo humano.
PADROES = {
    "Atraso ou não recebimento": r"\b(atras\w*|demor\w*|nao recebi|nao chegou|nao entreg\w*|nao foi entregue|ainda aguard\w*|prazo venc\w*)\b",
    "Defeito, avaria ou baixa qualidade": r"\b(defeit\w*|quebrad\w*|danificad\w*|avariad\w*|estragad\w*|rachad\w*|nao funciona\w*|pessima qualidade|baixa qualidade|qualidade ruim)\b",
    "Produto diferente do solicitado": r"\b(errad\w*|diferente do|diferente da|veio outro|veio outra|nao corresponde|nao condiz|divergent\w*)\b",
    "Pedido incompleto ou peças faltantes": r"\b(faltando|incomplet\w*|falta de pecas|faltam pecas|so veio um|so veio uma|so recebi um|so recebi uma|apenas um|apenas uma)\b",
    "Atendimento, troca ou reembolso": r"\b(atendimento|nao respond\w*|sem resposta|sem retorno|nao tive retorno|reembols\w*|estorn\w*|devolu\w*|devolver|troca\w*)\b",
}


def classificar(text):
    plain = unicodedata.normalize("NFKD", str(text).lower())
    plain = "".join(c for c in plain if not unicodedata.combining(c))
    return {name: bool(re.search(pattern, plain)) for name, pattern in PADROES.items()}


def main():
    dados = pd.read_csv("data/processed/treino.csv")
    dados = dados.loc[dados.sentimento.eq("negativo")].reset_index(drop=True)
    flags = pd.DataFrame(dados.texto_limpo.map(classificar).tolist())
    saida = Path("reports/etapa3")
    local = Path("data/processed/etapa3")
    saida.mkdir(parents=True, exist_ok=True)
    local.mkdir(parents=True, exist_ok=True)
    rows, samples = [], []
    for name in PADROES:
        subset = dados.loc[flags[name]]
        rows.append({"tema": name, "mencoes_detectadas": len(subset),
                     "percentual_negativos_treino": round(100 * len(subset) / len(dados), 2)})
        samples.append({"tema": name, "exemplos": subset.sample(min(15, len(subset)), random_state=42).texto_limpo.tolist()})
    pd.DataFrame(rows).to_csv(saida / "cinco_temas.csv", index=False)
    report = {"denominador": len(dados), "escopo": "negativos do treino",
              "metodo": "regras lexicais exploratórias multirrótulo; não validado como classificador",
              "com_algum_tema": int(flags.any(axis=1).sum()),
              "sem_tema_detectado": int((~flags.any(axis=1)).sum()),
              "multiplos_temas": int((flags.sum(axis=1) > 1).sum()), "temas": rows,
              "padroes": PADROES}
    (saida / "cinco_temas.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (local / "amostra_temas.json").write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.concat([dados[["review_id", "texto_limpo"]], flags], axis=1).to_csv(local / "temas_por_avaliacao.csv", index=False)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
