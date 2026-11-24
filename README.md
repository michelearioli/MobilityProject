# Data-Driven Urban Mobility: Event Detection and Flow Forecasting

BSc thesis in Computer Engineering, University of Modena and Reggio Emilia (UNIMORE), 2025.
Supervisor: Prof. Nicola Bicocchi.

This work was extended into a peer-reviewed journal article:

> N. Bicocchi, **M. Arioli**, M. Mamei, C. Petrovich. *From flows to events: spatiotemporal insights into Bologna's mobility using mobile networks.* Journal of Ambient Intelligence and Humanized Computing, Springer, 2026.
> DOI: [10.1007/s12652-026-05127-x](https://doi.org/10.1007/s12652-026-05127-x)

📄 Full thesis (Italian): [Tesi.pdf](Tesi.pdf)

## Overview

The project analyzes and forecasts human mobility across the Emilia-Romagna region (Italy) using anonymized origin–destination data from **TIM Enterprise**, derived from mobile-network signals. The dataset covers August–September 2019 and records movements between elementary census areas (ACE) with demographic breakdowns: age, gender, nationality and trip purpose.

The pipeline covers four stages:

1. **Data engineering**: cleaning, validation and storage of ~36M raw records in PostgreSQL.
2. **Exploratory analysis and visualization**: temporal, demographic and geographic patterns, with interactive origin–destination flow maps (Folium, GeoPandas).
3. **Event detection**: a Z-score method on hourly net flows that flags anomalies such as trade fairs, sporting events and festivals.
4. **Forecasting and deployment**: Gradient Boosting models that predict daily inbound flows for each ACE, served through a FastAPI + Docker prediction API.

## Repository structure

| Folder | Content |
|---|---|
| `data_analysis_and_cleansing/` | Cleaning scripts and PostgreSQL loading (`data_cleansing1.py`, `data_cleansing2.py`); aggregate analyses by province and ACE; statistical analyses by day, time slot and category. |
| `visualization/` | Interactive Folium map of regional mobility and a single-ACE visualization tool. |
| `flowOD/` | Origin–destination flow analysis and maps (internal city flows, flows toward cities). |
| `EventDetection/` | Z-score anomaly detection at province and single-ACE level, plus presence-based analysis. |
| `experiments_on_single_ACE/` | Inbound/outbound analysis of single ACEs, by demographic category, and the Dozza case study. |
| `regressions/` | Baseline regressors (Random Forest, KNN, Gradient Boosting) at ACE, province and origin/destination level, plus multi-output regression on demographic categories. |
| `GradientBoosting/` | Final Gradient Boosting models: Dozza with local data only, Dozza with the full regional dataset, and generalization to all ACEs. |
| `mobility_api/` | FastAPI service that exposes the trained model (`/predict`, `/health`), with Dockerfile and docker-compose. |

## Methods and results

All forecasting models use a **Gradient Boosting Regressor** with a log-transformed target, Min-Max feature scaling and hyperparameters tuned with `GridSearchCV`. Accuracy is measured with MAE and MAPE.

| Experiment | Setup | Result |
|---|---|---|
| Dozza, local data only | 61 daily samples, features: date, weekday, week, holiday flag, month | MAE 732, MAPE 8.49% |
| Dozza, full regional dataset | 28,548 samples (61 days × 468 ACEs), same features + ACE id | MAE 675, MAPE **8.04%** |
| Generalization to all 468 ACEs | Per-ACE models, 41 training days / 20 test days | Mean MAPE **9.92%** with lag features (vs 12.08% and 12.47% for the calendar-based feature sets) |
| Model behind the API | 70/30 split by day; features: date, ACE id, weekday, week, weekend | MAE 969, MAPE 8.92% |

Main findings:

- Urban and industrial areas (e.g. Bologna, Modena) are the most predictable, thanks to regular commuting patterns.
- Tourist and mountain areas (Romagna coast, Apennines) are harder to forecast, because their flows depend on events, weather and holidays.
- The Z-score detector matches real events, such as Cersaie at the Bologna fair district and motorsport events at the Imola circuit.

## Running the API

The trained model, scaler and encoder are included as `.pkl` files in `mobility_api/`.

**With Docker:**

```bash
cd mobility_api
docker compose up --build
```

**Without Docker** (Python ≥ 3.9):

```bash
cd mobility_api
pip install -r requirements.txt
uvicorn main:app --port 8080
```

Interactive docs: <http://localhost:8080/docs>

**Example request:**

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-06-01", "layerid": "08|037|025|000|000"}'
```

## Data availability

The TIM mobility dataset is not included in this repository, because it is covered by confidentiality agreements with the data provider. The notebooks document the full processing pipeline, but they cannot be re-run without access to the data.

## Tech stack

Python · pandas · scikit-learn · PostgreSQL · Folium · GeoPandas · FastAPI · Uvicorn · Docker
