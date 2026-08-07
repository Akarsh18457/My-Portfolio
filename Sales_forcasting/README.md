# 📈 End-to-End Sales Forecasting & Demand Intelligence System

An end-to-end data science pipeline built on 4 years of Superstore sales data — covering time series forecasting, anomaly detection, product demand segmentation, and an interactive deployed dashboard.

## Overview

Retail businesses live or die by one question: *how much of each product will we sell next month, and will we have enough stock to meet that demand?* This project builds a working system to answer that, from raw transactional data to a stakeholder-facing dashboard and business report.

**What's inside:**
- Time series decomposition & stationarity testing on 4 years of monthly sales
- Three forecasting models built and benchmarked head-to-head: **SARIMA**, **Facebook Prophet**, and **XGBoost** (lag-feature based)
- Category & region-level forecasting
- Anomaly detection using two independent methods (Isolation Forest + rolling Z-score)
- Product demand segmentation via K-Means clustering (PCA-visualized)
- A 4-page interactive **Streamlit** dashboard
- A 2-page executive business report for non-technical stakeholders

## Key Results

| Model | MAE | RMSE | MAPE |
|---|---|---|---|
| **XGBoost** ✅ | 18,878 | 22,570 | **18.8%** |
| Prophet | 20,296 | 22,487 | 21.9% |
| SARIMA | 21,060 | 22,020 | 22.4% |

XGBoost (trained on lag features + cyclically-encoded calendar features, forecasted recursively) outperformed both classical time series approaches on a 3-month holdout and was carried forward for segment-level forecasting.

- Identified a consistent, repeatable seasonal pattern (Sep/Nov/Dec peaks, Jan/Feb troughs) confirmed across all 4 years via decomposition, EDA, and anomaly detection.
- Flagged anomalous sales weeks using two independent detectors; the two methods largely disagreed, revealing the difference between *globally* extreme weeks (Isolation Forest) and *locally* unusual weeks relative to recent trend (Z-score).
- Segmented 17 product sub-categories into 4 actionable demand clusters (e.g. *High Volume Stable*, *Low Volume High-Value Volatile*, *Growing Demand*) with a distinct stocking strategy recommended per cluster.

## Tech Stack

`Python` · `Pandas` / `NumPy` · `Statsmodels` · `pmdarima` · `Prophet` · `XGBoost` · `Scikit-learn` · `Matplotlib` / `Seaborn` · `Streamlit` · `Plotly`

## Project Structure

```
SalesForecasting_Akarsh/
├── analysis.ipynb          # Full analysis — all tasks, fully executed
├── app.py                  # Streamlit dashboard (4 pages)
├── requirements.txt
├── summary.docx            # 2-page executive business report
├── train.csv                # Superstore sales dataset
├── vgsales.csv              # Supplementary dataset (merge exercise)
├── charts/                  # All exported chart images
└── dashboard_data/          # Precomputed data the dashboard reads
```

## Dashboard

4 pages, built with Streamlit + Plotly:
1. **Sales Overview** — yearly/monthly trends, region × category breakdown with filters
2. **Forecast Explorer** — pick a category or region, view its forecast + model accuracy
3. **Anomaly Report** — flagged anomalous weeks from both detection methods
4. **Product Demand Segments** — cluster visualization + sub-category stocking guide

**Live app:** _add your deployed Streamlit Community Cloud link here_

## Running Locally

```bash
git clone <this-repo-url>
cd SalesForecasting_Akarsh
pip install -r requirements.txt
jupyter notebook analysis.ipynb   # to explore the full analysis
streamlit run app.py              # to launch the dashboard
```

## Dataset

- [Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) — 4 years of daily transactional sales data
- [Video Game Sales Dataset](https://www.kaggle.com/datasets/gregorut/videogamesales) — supplementary dataset used to practice multi-source merging

## Notes & Limitations

Model validation was done on a 3-month holdout, which is a small test set — the ranking between models should be re-checked periodically as more data becomes available rather than treated as permanent. Forecast confidence decreases further beyond the 3-month horizon.
