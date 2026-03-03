#!/usr/bin/env python3
"""
Gera figuras principais a partir do parquet processado e salva em figs/
Uso: python scripts/generate_figs.py
"""
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os.makedirs("figs", exist_ok=True)
processed = "data/processed/telecom_transformed.parquet"
if not os.path.exists(processed):
    raise FileNotFoundError("Arquivo processado não encontrado. Rode scripts/run_etl.py primeiro.")

df = pd.read_parquet(processed)

# 1 - Churn por tipo de contrato
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='contract_type', hue='churn')
plt.title("Churn por tipo de contrato")
plt.tight_layout()
plt.savefig("figs/churn_por_contrato.png", dpi=150)
plt.close()

# 2 - Boxplot monthlycharges por churn
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='churn', y='monthlycharges')
plt.title("Monthly Charges por churn")
plt.tight_layout()
plt.savefig("figs/monthlycharges_boxplot.png", dpi=150)
plt.close()

# 3 - Heatmap correlação numérica
num_df = df.select_dtypes(include='number')
plt.figure(figsize=(10,8))
sns.heatmap(num_df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Matriz de correlação")
plt.tight_layout()
plt.savefig("figs/correlation_heatmap.png", dpi=150)
plt.close()

# 4 - Tenure vs churn (histograma/violin)
if 'customer_tenure' in df.columns:
    plt.figure(figsize=(8,5))
    sns.violinplot(data=df, x='churn', y='customer_tenure')
    plt.title("Tenure por churn")
    plt.tight_layout()
    plt.savefig("figs/tenure_violin.png", dpi=150)
    plt.close()

print("Figuras geradas em /figs")
