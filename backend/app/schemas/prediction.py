from pydantic import BaseModel


class PredictionRequest(BaseModel):
    Year: int
    Month: int
    lag_1: float
    lag_2: float
    rolling_mean_3: float


class PredictionResponse(BaseModel):
    predicted_units: float
    predicted_bill: float
    status: str