from pydantic import BaseModel


# Request Schema
class PredictionRequest(BaseModel):
    month: str
    previous_units: float
    temperature: float
    occupants: int


# Response Schema
class PredictionResponse(BaseModel):
    predicted_units: float
    predicted_bill: float
    status: str