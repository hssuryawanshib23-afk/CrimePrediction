"""Model loading, feature assembly, and explainability helpers."""

import json
from functools import lru_cache
from typing import Any

import joblib
import pandas as pd

from .config import FEATURE_IMPORTANCE_PATH, METRICS_PATH, MODEL_BUNDLE_PATH
from .data_service import compute_risk_level, load_dataset


@lru_cache(maxsize=1)
def load_model_bundle() -> dict[str, Any]:
    """Load the selected trained model and preprocessing metadata."""

    if not MODEL_BUNDLE_PATH.exists():
        raise FileNotFoundError(
            f"Model bundle not found at {MODEL_BUNDLE_PATH}. Run `python ml/train_models.py`."
        )
    return joblib.load(MODEL_BUNDLE_PATH)


def load_metrics() -> list[dict[str, float | str]]:
    """Load model comparison metrics."""

    if not METRICS_PATH.exists():
        return []
    return json.loads(METRICS_PATH.read_text())


def load_feature_importance() -> dict[str, Any]:
    """Load global feature importance data."""

    if not FEATURE_IMPORTANCE_PATH.exists():
        return {"features": []}
    return json.loads(FEATURE_IMPORTANCE_PATH.read_text())


def build_features(
    state: str,
    year: int,
    model: Any | None = None,
    feature_names: list[str] | None = None,
) -> dict[str, float]:
    """Build model features, recursively forecasting missing future years."""

    df = load_dataset()
    state_rows = df[df["state"].str.lower() == state.lower()].sort_values("year")
    if state_rows.empty:
        raise ValueError(f"Unknown state: {state}")

    history = state_rows[state_rows["year"] < year]
    if history.empty:
        history = state_rows

    counts = [float(value) for value in history["crime_count"].tolist()]
    population = float(history.iloc[-1]["population"])
    literacy_rate = float(history.iloc[-1]["literacy_rate"])
    urban_pct = float(history.iloc[-1]["urban_population_pct"])
    current_year = int(history.iloc[-1]["year"])

    if year > current_year + 1:
        if model is None or feature_names is None:
            raise ValueError("Future multi-year forecasts require a trained model.")
        population_growth, literacy_step, urban_step = _demographic_trends(history)
        while current_year < year - 1:
            features = _features_from_history(counts, population, literacy_rate, urban_pct)
            frame = pd.DataFrame([{name: features[name] for name in feature_names}])
            predicted_count = max(float(model.predict(frame)[0]), 0.0)
            counts.append(predicted_count)
            current_year += 1
            population *= 1 + population_growth
            literacy_rate = min(literacy_rate + literacy_step, 100.0)
            urban_pct = min(urban_pct + urban_step, 100.0)

    return _features_from_history(counts, population, literacy_rate, urban_pct)


def predict(state: str, year: int) -> dict[str, Any]:
    """Predict crime count and return local explanation values."""

    bundle = load_model_bundle()
    feature_names: list[str] = bundle["feature_names"]
    model = bundle["model"]
    features = build_features(state, year, model, feature_names)
    frame = pd.DataFrame([{name: features[name] for name in feature_names}])
    prediction = max(float(model.predict(frame)[0]), 0.0)

    df = load_dataset()
    risk_level = compute_risk_level(prediction, df["crime_count"])
    confidence = _estimate_confidence(prediction, df["crime_count"])
    explanation = _local_explanation(features, bundle.get("feature_importance", []))

    return {
        "state": state,
        "year": year,
        "predicted_crime_count": round(prediction, 2),
        "risk_level": risk_level,
        "confidence": confidence,
        "features": {key: round(value, 4) for key, value in features.items()},
        "explanation": explanation,
    }


def _features_from_history(
    counts: list[float], population: float, literacy_rate: float, urban_pct: float
) -> dict[str, float]:
    """Create model inputs from observed or simulated state history."""

    previous_count = counts[-1]
    older_count = counts[-2] if len(counts) >= 2 else previous_count
    growth_rate = 0.0 if older_count == 0 else (previous_count - older_count) / older_count
    rolling_mean_3yr = sum(counts[-3:]) / min(len(counts), 3)

    return {
        "previous_crime_count": previous_count,
        "crime_growth_rate": growth_rate,
        "population": population,
        "literacy_rate": literacy_rate,
        "urban_population_pct": urban_pct,
        "rolling_mean_3yr": rolling_mean_3yr,
    }


def _demographic_trends(history: pd.DataFrame) -> tuple[float, float, float]:
    """Estimate annual demographic changes from the latest observed rows."""

    if len(history) < 2:
        return 0.0, 0.0, 0.0

    recent = history.tail(min(len(history), 5))
    years = max(int(recent.iloc[-1]["year"] - recent.iloc[0]["year"]), 1)
    start_population = max(float(recent.iloc[0]["population"]), 1.0)
    end_population = max(float(recent.iloc[-1]["population"]), 1.0)
    population_growth = (end_population / start_population) ** (1 / years) - 1
    literacy_step = (float(recent.iloc[-1]["literacy_rate"]) - float(recent.iloc[0]["literacy_rate"])) / years
    urban_step = (
        float(recent.iloc[-1]["urban_population_pct"]) - float(recent.iloc[0]["urban_population_pct"])
    ) / years
    return population_growth, max(literacy_step, 0.0), max(urban_step, 0.0)


def _estimate_confidence(prediction: float, reference: pd.Series) -> float:
    """Return a simple portfolio-friendly confidence proxy from prediction spread."""

    std = max(float(reference.std()), 1.0)
    z_score = abs(prediction - float(reference.mean())) / std
    confidence = max(0.55, min(0.94, 0.9 - (z_score * 0.05)))
    return round(confidence, 2)


def _local_explanation(
    features: dict[str, float], global_importance: list[dict[str, float | str]]
) -> list[dict[str, float | str]]:
    """Approximate a local explanation using normalized feature values and global weights."""

    if not global_importance:
        return []

    max_values = {
        "previous_crime_count": 350000.0,
        "crime_growth_rate": 0.35,
        "population": 250000000.0,
        "literacy_rate": 100.0,
        "urban_population_pct": 100.0,
        "rolling_mean_3yr": 350000.0,
    }
    rows = []
    for item in global_importance:
        feature = str(item["feature"])
        value = abs(features.get(feature, 0.0)) / max_values.get(feature, 1.0)
        impact = float(item["importance"]) * value
        rows.append(
            {
                "feature": feature,
                "impact": round(impact, 4),
                "direction": "increases risk" if impact >= 0 else "reduces risk",
            }
        )
    return sorted(rows, key=lambda row: abs(float(row["impact"])), reverse=True)[:5]
