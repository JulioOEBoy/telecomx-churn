# telecomx-churn

Entrega do desafio TelecomX — ETL + EDA.

## Estrutura
- `notebooks/01_etl.ipynb` — ETL interativo
- `notebooks/02_eda.ipynb` — EDA interativo
- `scripts/run_etl.py` — script para gerar `data/processed/telecom_transformed.parquet`
- `scripts/generate_figs.py` — gera figuras em `figs/`
- `data/raw/` — raw JSON (não versionar)
- `data/processed/` — dataset tratado (não versionar)
- `figs/` — figuras salvas
- `relatorio_telecomx.md` — relatório final

## Como rodar (local)
1. Instale dependências: `pip install -r requirements.txt`  
2. Rode ETL: `python scripts/run_etl.py`  
3. Gere figuras: `python scripts/generate_figs.py`  
4. Abra notebooks para análise interativa.

