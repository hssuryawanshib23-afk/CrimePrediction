"""Train and compare crime forecasting models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

try:
    import shap
except ImportError:  # pragma: no cover
    shap = None

try:
    from xgboost import XGBRegressor
except ImportError:  # pragma: no cover
    XGBRegressor = None


BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "data" / "processed" / "state_crime_2001_2023.csv"
MODELS_DIR = BASE_DIR / "models"

FEATURE_NAMES = [
    "previous_crime_count",
    "crime_growth_rate",
    "population",
    "literacy_rate",
    "urban_population_pct",
    "rolling_mean_3yr",
]


def load_training_frame() -> pd.DataFrame:
    """Load source CSV and create lagged supervised-learning features."""

    df = pd.read_csv(DATASET_PATH).sort_values(["state", "year"]).reset_index(drop=True)
    df["previous_crime_count"] = df.groupby("state")["crime_count"].shift(1)
    df["previous_previous_crime_count"] = df.groupby("state")["crime_count"].shift(2)
    df["crime_growth_rate"] = (
        (df["previous_crime_count"] - df["previous_previous_crime_count"])
        / df["previous_previous_crime_count"].replace(0, np.nan)
    )
    df["rolling_mean_3yr"] = (
        df.groupby("state")["crime_count"]
        .shift(1)
        .rolling(window=3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )
    frame = df.dropna(subset=FEATURE_NAMES + ["crime_count"]).copy()
    frame["crime_growth_rate"] = frame["crime_growth_rate"].replace([np.inf, -np.inf], 0).fillna(0)
    return frame


def candidate_models() -> dict[str, Any]:
    """Return candidate regressors."""

    models: dict[str, Any] = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=250,
            max_depth=8,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        ),
    }
    if XGBRegressor is not None:
        models["XGBoost"] = XGBRegressor(
            n_estimators=300,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="reg:squarederror",
            random_state=42,
        )
    return models


def evaluate_model(name: str, model: Any, x_train: pd.DataFrame, y_train: pd.Series, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, Any]:
    """Fit and score one model."""

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    return {
        "name": name,
        "model": model,
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
        "r2": float(r2_score(y_test, predictions)),
    }


def compute_feature_importance(
    model: Any, x_train: pd.DataFrame, y_train: pd.Series
) -> tuple[str, list[dict[str, float | str]]]:
    """Compute SHAP mean absolute feature importance when available."""

    source = "SHAP mean absolute value"
    if shap is not None:
        try:
            explainer = shap.Explainer(model, x_train)
            shap_values = explainer(x_train)
            values = np.abs(shap_values.values).mean(axis=0)
        except Exception:
            source = "model feature importance fallback"
            values = fallback_importance(model, x_train, y_train)
    else:
        source = "model feature importance fallback"
        values = fallback_importance(model, x_train, y_train)

    total = float(values.sum()) or 1.0
    rows = [
        {"feature": feature, "importance": round(float(value / total), 4)}
        for feature, value in zip(FEATURE_NAMES, values)
    ]
    return source, sorted(rows, key=lambda row: float(row["importance"]), reverse=True)


def fallback_importance(model: Any, x_train: pd.DataFrame, y_train: pd.Series) -> np.ndarray:
    """Compute model-agnostic permutation importance as a fallback."""

    result = permutation_importance(
        model,
        x_train,
        y_train,
        n_repeats=12,
        random_state=42,
        scoring="neg_root_mean_squared_error",
        n_jobs=1,
    )
    values = np.maximum(result.importances_mean, 0)
    if float(values.sum()) == 0:
        values = np.asarray(getattr(model, "feature_importances_", np.ones(len(FEATURE_NAMES))), dtype=float)
    return values


def main() -> None:
    """Train models and persist the best performer."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset missing: {DATASET_PATH}")

    frame = load_training_frame()
    train = frame[frame["year"] <= 2019]
    test = frame[frame["year"] > 2019]
    x_train, y_train = train[FEATURE_NAMES], train["crime_count"]
    x_test, y_test = test[FEATURE_NAMES], test["crime_count"]

    results = [
        evaluate_model(name, model, x_train, y_train, x_test, y_test)
        for name, model in candidate_models().items()
    ]
    best = min(results, key=lambda item: item["rmse"])
    importance_source, feature_importance = compute_feature_importance(best["model"], x_train, y_train)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": best["model"],
            "model_name": best["name"],
            "feature_names": FEATURE_NAMES,
            "feature_importance": feature_importance,
        },
        MODELS_DIR / "crime_model.joblib",
    )

    metrics = [
        {
            "model": row["name"],
            "mae": round(row["mae"], 2),
            "rmse": round(row["rmse"], 2),
            "r2": round(row["r2"], 4),
            "selected": row["name"] == best["name"],
        }
        for row in results
    ]
    (MODELS_DIR / "model_metrics.json").write_text(json.dumps(metrics, indent=2))
    (MODELS_DIR / "feature_importance.json").write_text(
        json.dumps(
            {
                "selected_model": best["name"],
                "features": feature_importance,
                "importance_source": importance_source,
            },
            indent=2,
        )
    )
    print(f"Selected model: {best['name']}")


if __name__ == "__main__":
    main()
