"""Application configuration for the Crime Risk Analytics API."""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"

DATASET_PATH = DATA_DIR / "state_crime_2001_2023.csv"
MODEL_BUNDLE_PATH = MODELS_DIR / "crime_model.joblib"
METRICS_PATH = MODELS_DIR / "model_metrics.json"
FEATURE_IMPORTANCE_PATH = MODELS_DIR / "feature_importance.json"

RISK_QUANTILES = (0.33, 0.66)
DEFAULT_FORECAST_YEAR = 2024

