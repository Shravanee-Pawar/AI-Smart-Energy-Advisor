from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import predict_energy

router = APIRouter()


@router.post("/", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    """
    Predict energy usage (Dummy Implementation)
    """
    return predict_energy(data)