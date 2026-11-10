"""Executa as análises finais antes da produção do relatório.

Pré-requisito:
    data/processed/treino.csv
    data/processed/teste.csv

Execução:
    python -m src.finalizar_analise
"""
from __future__ import annotations

import subprocess
import sys


def executar(modulo: str) -> None:
    print(f"\n=== Executando {modulo} ===", flush=True)
    subprocess.run([sys.executable, "-m", modulo], check=True)


def main() -> None:
    executar("src.eda_final")
    executar("src.etapa3_validacao")
    print("\nAnálises finais concluídas. Verifique reports/figures e reports/etapa3/validacao_operacional.")


if __name__ == "__main__":
    main()
