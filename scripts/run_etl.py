#!/usr/bin/env python3
"""
Run ETL: baixa JSON, salva raw e gera data/processed/telecom_transformed.parquet
Uso: python scripts/run_etl.py
"""
import requests, json, os, datetime
import pandas as pd

URL = "https://raw.githubusercontent.com/alura-cursos/challenge2-data-science/refs/heads/main/TelecomX_Data.json"

def run_etl(url=URL):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    raw = resp.json()

    os.makedirs("data/raw", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"data/raw/telecom_raw_{ts}.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)
    print("Raw salvo em:", raw_path)

    df = pd.json_normalize(raw)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    date_cols = [c for c in df.columns if "date" in c or "signup" in c or "last" in c]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors='coerce')

    os.makedirs("data/processed", exist_ok=True)
    parquet_path = "data/processed/telecom_transformed.parquet"
    csv_path = "data/processed/telecom_transformed.csv"
    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False)
    print("Processed salvo em:", parquet_path, "e", csv_path)
    return parquet_path

if __name__ == "__main__":
    run_etl()
