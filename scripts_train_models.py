#!/usr/bin/env python3
"""Telecom X — Parte 2: Treino de modelos (CLI)

Este script treina modelos de churn usando o dataset processado na Parte 1:
- data/processed/telecom_transformed.parquet (preferido) ou .csv

Saídas:
- models/churn_model.joblib
- relatorio_parte2.md

Uso:
  python scripts/train_models.py
"""

import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.inspection import permutation_importance


PARQUET = "data/processed/telecom_transformed.parquet"
CSV = "data/processed/telecom_transformed.csv"

USAR_SMOTE = False  # opcional


def carregar():
    if os.path.exists(PARQUET):
        return pd.read_parquet(PARQUET)
    if os.path.exists(CSV):
        return pd.read_csv(CSV)
    raise FileNotFoundError("Não achei dataset processado. Rode antes: python scripts/run_etl.py")


def binarizar_y(y_raw: pd.Series) -> pd.Series:
    if y_raw.dtype == "object":
        mapa = {"yes":1,"no":0,"sim":1,"não":0,"nao":0,"true":1,"false":0,"1":1,"0":0}
        y = y_raw.astype(str).str.strip().str.lower().map(mapa)
        if y.isna().any():
            uniq = list(pd.unique(y_raw.astype(str)))
            if len(uniq) == 2:
                y = y_raw.astype(str).map({uniq[0]:0, uniq[1]:1})
            else:
                raise ValueError(f"Não consegui converter churn para binário. Valores únicos: {uniq[:10]}")
        return y.astype(int)
    return y_raw.astype(int)


def main():
    df = carregar()
    alvo = "churn" if "churn" in df.columns else next((c for c in df.columns if "churn" in c.lower() or "evas" in c.lower()), None)
    if alvo is None:
        raise KeyError("Não encontrei coluna de churn.")

    # remove IDs (heurística)
    cols_drop = []
    for c in df.columns:
        if c == alvo:
            continue
        nome = c.lower()
        if nome in ["customerid","customer_id","id","cliente_id"] or nome.endswith("id"):
            cols_drop.append(c)
            continue
        nunique = df[c].nunique(dropna=True)
        if nunique / max(len(df),1) > 0.95:
            cols_drop.append(c)

    df_model = df.drop(columns=sorted(set(cols_drop)), errors="ignore")

    X = df_model.drop(columns=[alvo])
    y = binarizar_y(df_model[alvo])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    cat_cols = [c for c in X_train.columns if X_train[c].dtype == "object"]
    num_cols = [c for c in X_train.columns if c not in cat_cols]

    preprocess_scale = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("scaler", StandardScaler())]), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )
    preprocess_tree = ColumnTransformer(
        transformers=[
            ("num", "passthrough", num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    if USAR_SMOTE:
        from imblearn.over_sampling import SMOTE
        from imblearn.pipeline import Pipeline as ImbPipeline
        smote = SMOTE(random_state=42)
    else:
        smote = None
        ImbPipeline = None

    modelos = {
        "LogReg": LogisticRegression(max_iter=2500, class_weight="balanced"),
        "KNN": KNeighborsClassifier(n_neighbors=15),
        "SVM": SVC(kernel="linear", class_weight="balanced", probability=True),
        "RandomForest": RandomForestClassifier(n_estimators=400, random_state=42, n_jobs=-1, class_weight="balanced_subsample"),
    }

    resultados = {}
    treinados = {}

    for nome, clf in modelos.items():
        prep = preprocess_tree if nome == "RandomForest" else preprocess_scale
        if USAR_SMOTE and smote is not None and nome != "RandomForest":
            pipe = ImbPipeline([("prep", prep), ("smote", smote), ("clf", clf)])
        else:
            pipe = Pipeline([("prep", prep), ("clf", clf)])

        pipe.fit(X_train, y_train)

        if hasattr(pipe, "predict_proba"):
            y_score = pipe.predict_proba(X_test)[:, 1]
        else:
            y_score = pipe.decision_function(X_test)

        resultados[nome] = {
            "roc_auc": float(roc_auc_score(y_test, y_score)),
            "pr_auc": float(average_precision_score(y_test, y_score)),
        }
        treinados[nome] = pipe

    melhor_nome = max(resultados, key=lambda k: resultados[k]["roc_auc"])
    melhor_pipe = treinados[melhor_nome]

    # importância por permutação
    r = permutation_importance(melhor_pipe, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1)

    prep = melhor_pipe.named_steps["prep"]
    feat_names = []
    feat_names.extend(num_cols)
    if len(cat_cols) > 0:
        ohe = prep.named_transformers_["cat"]
        feat_names.extend(list(ohe.get_feature_names_out(cat_cols)))

    importancias = pd.Series(r.importances_mean, index=feat_names).sort_values(ascending=False)

    os.makedirs("models", exist_ok=True)
    joblib.dump(melhor_pipe, "models/churn_model.joblib")

    linhas = []
    linhas.append("# Relatório — Telecom X (Parte 2: Previsão de Churn)")
    linhas.append("")
    linhas.append("## Resultados")
    linhas.append("")
    for nome, m in sorted(resultados.items(), key=lambda kv: kv[1]["roc_auc"], reverse=True):
        linhas.append(f"- **{nome}** — ROC-AUC: `{m['roc_auc']:.4f}` | PR-AUC: `{m['pr_auc']:.4f}`")
    linhas.append("")
    linhas.append("## Melhor modelo")
    linhas.append("")
    linhas.append(f"- **{melhor_nome}**")
    linhas.append("")
    linhas.append("## Top variáveis (permutation importance)")
    linhas.append("")
    for k, v in importancias.head(12).items():
        linhas.append(f"- `{k}`: `{v:.6f}`")
    linhas.append("")

    with open("relatorio_parte2.md", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

    print("✅ Modelo salvo em: models/churn_model.joblib")
    print("✅ Relatório salvo em: relatorio_parte2.md")


if __name__ == "__main__":
    main()
