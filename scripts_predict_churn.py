#!/usr/bin/env python3
"""Telecom X — Parte 2: Inferência (CLI)

Carrega models/churn_model.joblib e gera previsões para um CSV de entrada.

Uso:
  python scripts/predict_churn.py --input data/processed/telecom_transformed.csv --output preds.csv

"""

import argparse
import joblib
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV com as features (mesmas colunas do treino, sem a coluna churn)")
    ap.add_argument("--output", default="preds.csv", help="Arquivo de saída com probabilidades e classe")
    ap.add_argument("--threshold", type=float, default=0.5, help="Limiar para classificar churn")
    args = ap.parse_args()

    model = joblib.load("models/churn_model.joblib")
    X = pd.read_csv(args.input)

    # tenta remover coluna churn se vier por acidente
    for c in ["churn", "Churn", "evasao", "Evasao"]:
        if c in X.columns:
            X = X.drop(columns=[c])

    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= args.threshold).astype(int)

    out = X.copy()
    out["proba_churn"] = proba
    out["pred_churn"] = pred
    out.to_csv(args.output, index=False)
    print("✅ Salvo:", args.output)

if __name__ == "__main__":
    main()
