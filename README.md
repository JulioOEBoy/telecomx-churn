# telecomx-churn

Entrega do desafio TelecomX — **ETL + EDA** (Parte 1).

## Estrutura
- `notebooks_01_etl.ipynb` — ETL interativo (gera dataset processado)
- `notebooks_02_eda.ipynb` — EDA interativo (gera gráficos e relatório)
- `scripts/run_etl.py` — baixa o JSON e gera `data/processed/telecom_transformed.parquet`
- `scripts/generate_figs.py` — (opcional) gera figuras em `figs/`
- `data/raw/` — raw JSON (não versionar)
- `data/processed/` — dataset tratado (não versionar)
- `figs/` — figuras salvas (pode versionar)
- `relatorio_telecomx.md` — relatório final (gerado pelo EDA)

## Como rodar (local)
1. Instale dependências: `pip install -r requirements.txt`
2. Rode ETL: `python scripts/run_etl.py`
3. Rode EDA (recomendado): abra `notebooks_02_eda.ipynb` e execute tudo
4. (Opcional) Gere figuras via script: `python scripts/generate_figs.py`

> Dica: o notebook de EDA também gera `figs/` e escreve `relatorio_telecomx.md` automaticamente.
