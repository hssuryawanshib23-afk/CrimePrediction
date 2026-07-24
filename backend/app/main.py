"""FastAPI entrypoint for the Crime Risk Analytics Dashboard."""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .data_service import get_states, get_years_for_state, statistics
from .model_service import load_feature_importance, load_metrics, predict
from .schemas import PredictionRequest, PredictionResponse, StatisticsResponse

app = FastAPI(
    title="Crime Risk Analytics API",
    description="State-wise Indian crime forecasting and explainability API.",
    version="1.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""

    return {"status": "ok"}


@app.get("/states")
def states() -> list[str]:
    """Return available states/UTs."""

    return get_states()


@app.get("/districts")
def districts(state: str | None = None) -> dict[str, list[str]]:
    """Compatibility endpoint; returns state-level units for this MVP."""

    states_list = [state] if state else get_states()
    return {"districts": states_list}


@app.get("/years/{state}")
def years(state: str) -> list[int]:
    """Return years available for a selected state."""

    return get_years_for_state(state)


@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(payload: PredictionRequest) -> dict:
    """Predict next-year crime count for a state."""

    try:
        return predict(payload.state, payload.year)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/statistics", response_model=StatisticsResponse)
def statistics_endpoint() -> dict:
    """Return dashboard overview statistics."""

    return statistics()


@app.get("/feature-importance")
def feature_importance() -> dict:
    """Return global feature importance and model metrics."""

    payload = load_feature_importance()
    payload["metrics"] = load_metrics()
    return payload
