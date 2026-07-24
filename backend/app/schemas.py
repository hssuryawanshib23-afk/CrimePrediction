"""Pydantic request and response models."""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Input payload for state-year crime prediction."""

    state: str = Field(..., examples=["Maharashtra"])
    year: int = Field(..., ge=2002, le=2035, examples=[2024])


class PredictionResponse(BaseModel):
    """Prediction API response."""

    state: str
    year: int
    predicted_crime_count: float
    risk_level: str
    confidence: float
    features: dict[str, float]
    explanation: list[dict[str, float | str]]


class StatisticsResponse(BaseModel):
    """Overview statistics for the dashboard."""

    total_states: int
    average_crime: float
    highest_crime_state: str
    lowest_crime_state: str
    latest_year: int
    statewise_crime: list[dict[str, float | str]]
    crime_trend: list[dict[str, float | int]]
    map_points: list[dict[str, float | str]]
