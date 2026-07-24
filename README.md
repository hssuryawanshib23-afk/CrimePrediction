# Crime Risk Analytics Dashboard

Interactive dashboard for forecasting Indian state-wise crime risk using historical NCRB-style crime data, demographic context, model comparison, and SHAP feature importance.

This is a portfolio-focused full-stack ML project. It is intentionally local-first: CSV files, FastAPI, React, and no database.

## Project Scope

- Predict next-year state-wise crime count.
- Compare Linear Regression, Random Forest, and XGBoost.
- Automatically select the best model by holdout RMSE.
- Explain predictions using SHAP global feature importance.
- Visualize state-wise risk on an India map using React Leaflet.

The current MVP uses state-wise data from 2001-2023 because official district-level joins are harder to keep clean across boundary and naming changes.

## Architecture

```text
crime-risk-dashboard/
├── data/
│   ├── raw/                  # Official source files go here
│   └── processed/            # Clean model-ready CSV
├── ml/
│   ├── generate_sample_data.py
│   └── train_models.py
├── models/
│   ├── crime_model.joblib
│   ├── model_metrics.json
│   └── feature_importance.json
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── data_service.py
│       └── model_service.py
└── frontend/
    ├── package.json
    └── src/
```

## Dataset

Recommended official sources:

- NCRB Crime in India annual data from data.gov.in and NCRB annual reports.
- Census of India 2001 and 2011 Primary Census Abstract.
- MoHFW / National Commission on Population projections for 2011-2036.
- Census literacy and urban population percentage tables.

Expected processed CSV schema:

```csv
state,year,crime_count,population,literacy_rate,urban_population_pct,latitude,longitude
```

The repository includes `ml/generate_sample_data.py` to create a deterministic local dataset with the same schema. Replace `data/processed/state_crime_2001_2023.csv` with cleaned official data when available.

## Model Features

- Previous year's crime count
- Crime growth rate
- Population
- Literacy rate
- Urban population percentage
- Three-year rolling crime average

Target:

- Current year `crime_count`, trained from lagged features. The prediction endpoint uses the latest available history to forecast a selected future year.

## Model Comparison

Training writes model metrics to `models/model_metrics.json`.

Models compared:

- Linear Regression
- Random Forest
- XGBoost

Selection criterion:

- Lowest RMSE on the 2020-2023 holdout window.

## Installation

### Backend

```bash
cd crime-risk-dashboard
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
python ml/generate_sample_data.py
python ml/train_models.py
uvicorn backend.app.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### Frontend

```bash
cd crime-risk-dashboard/frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

For SHAP installation, Python 3.10-3.12 is recommended. On Python 3.13, the training script still runs and falls back to model feature importance if SHAP wheels are unavailable.

## API Endpoints

- `GET /states`
- `GET /districts`
- `POST /predict`
- `GET /statistics`
- `GET /feature-importance`

Example prediction:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"state":"Maharashtra","year":2024}'
```

## Screenshots

Add screenshots after running locally:

- `docs/screenshots/overview.png`
- `docs/screenshots/map.png`
- `docs/screenshots/prediction.png`
- `docs/screenshots/explainability.png`

## Notes

NCRB data is police-recorded crime data. Raw crime counts should not be interpreted as a complete measure of safety or governance performance. Population-normalized rates and reporting behavior matter for responsible interpretation.
