"""Dataset loading and dashboard statistics."""

from functools import lru_cache

import pandas as pd

from .config import DATASET_PATH


@lru_cache(maxsize=1)
def load_dataset() -> pd.DataFrame:
    """Load the processed state-wise crime dataset."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found at {DATASET_PATH}. "
            "Run `python ml/generate_sample_data.py` and `python ml/train_models.py`."
        )
    return pd.read_csv(DATASET_PATH)


def get_states() -> list[str]:
    """Return sorted state names."""

    df = load_dataset()
    return sorted(df["state"].unique().tolist())


def get_years_for_state(state: str) -> list[int]:
    """Return available years for a state."""

    df = load_dataset()
    years = df.loc[df["state"] == state, "year"].sort_values().unique()
    return [int(year) for year in years]


def compute_risk_level(value: float, reference: pd.Series) -> str:
    """Classify a predicted value into Low, Medium, or High risk."""

    low_cutoff = reference.quantile(0.33)
    high_cutoff = reference.quantile(0.66)
    if value <= low_cutoff:
        return "Low"
    if value <= high_cutoff:
        return "Medium"
    return "High"


def statistics() -> dict:
    """Compute overview, chart, and map data for the dashboard."""

    df = load_dataset()
    latest_year = int(df["year"].max())
    latest = df[df["year"] == latest_year].copy()
    latest = latest.sort_values("crime_count", ascending=False)

    statewise = [
        {"state": row.state, "crime_count": float(row.crime_count)}
        for row in latest.itertuples(index=False)
    ]

    trend = (
        df.groupby("year", as_index=False)["crime_count"]
        .sum()
        .sort_values("year")
        .to_dict(orient="records")
    )

    map_points = []
    for row in latest.itertuples(index=False):
        risk = compute_risk_level(float(row.crime_count), latest["crime_count"])
        map_points.append(
            {
                "state": row.state,
                "crime_count": float(row.crime_count),
                "risk_level": risk,
                "latitude": float(row.latitude),
                "longitude": float(row.longitude),
            }
        )

    return {
        "total_states": int(latest["state"].nunique()),
        "average_crime": float(latest["crime_count"].mean()),
        "highest_crime_state": str(latest.iloc[0]["state"]),
        "lowest_crime_state": str(latest.iloc[-1]["state"]),
        "latest_year": latest_year,
        "statewise_crime": statewise,
        "crime_trend": trend,
        "map_points": map_points,
    }

