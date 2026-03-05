# Telecom X — Parte 2: Previsão de Churn

Este repositório (Parte 2) usa o dataset tratado na **Parte 1** para treinar modelos preditivos e analisar as variáveis mais importantes para churn.

## Pré-requisito
Você precisa ter o dataset processado (Parte 1):

- `data/processed/telecom_transformed.parquet`
- `data/processed/telecom_transformed.csv`

No seu projeto Parte 1, rode:
```bash
python scripts/run_etl.py
```

## Arquivos principais
- `notebooks_03_churn_prediction.ipynb` — notebook completo (pré-processamento, modelos, métricas, importância, export do modelo)
- `scripts/train_models.py` — treino via linha de comando (gera `models/churn_model.joblib` e `relatorio_parte2.md`)
- `scripts/predict_churn.py` — inferência via linha de comando (gera `preds.csv`)

## Modelos avaliados
- Regressão Logística
- KNN
- SVM (linear)
- Random Forest

Métricas:
- ROC-AUC
- PR-AUC
- Precision/Recall/F1
- Matriz de confusão

## Como rodar (local)
1. Instale dependências:
```bash
pip install -r requirements_parte2.txt
```

2. Rode o notebook:
- `notebooks_03_churn_prediction.ipynb`

Ou via script:
```bash
python scripts/train_models.py
```

## Saídas
- `models/churn_model.joblib` (melhor modelo)
- `relatorio_parte2.md` (resumo de performance e top variáveis)
