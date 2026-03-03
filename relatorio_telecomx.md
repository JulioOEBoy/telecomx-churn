# Relatório TelecomX Churn

## 1 Introdução
Objetivo: identificar fatores associados à evasão de clientes (churn) e propor ações.

## 2 Fonte de dados
Origem: API/JSON do repositório GitHub.
Arquivos entregues: data/raw/*, data/processed/telecomx_transformed.parquet

## 3 Metodologia ETL
- Extração: URL usada e cópia raw salva.
- Transformação: lista das principais transformações (conversão de datas, imputação, padronização).
- Decisões importantes: como tratei NAs, remoção de duplicatas, criação de features.

## 4 Análise exploratória
- Gráficos principais (incluir imagens): churn por plano; tenure vs churn; gasto médio vs churn; heatmap de correlação.
- Principais observações (bullet points).

## 5 Principais achados
- Resumo dos fatores mais associados ao churn (ex.: clientes com tenure < X meses, queda de uso, alto número de tickets).

## 6 Recomendações
- Ações táticas: monitorar clientes com queda de uso; alertas automáticos para suporte; ofertas de retenção para tenure baixo.
- Ações estratégicas: revisar política de preços; campanhas segmentadas.

## 7 Próximos passos
- Construir modelo preditivo; validar com AUC; implementar pipeline de scoring.

## 8 Apêndice
- Código principal; dicionário de dados; notas sobre imputação.
