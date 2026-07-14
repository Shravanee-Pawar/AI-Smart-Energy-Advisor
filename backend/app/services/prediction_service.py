from app.schemas.prediction import PredictionRequest, PredictionResponse


def predict_energy(data: PredictionRequest) -> PredictionResponse:
    """
    Dummy prediction service.
    Later, this function will use the trained ML model.
    """

    return PredictionResponse(
        predicted_units=338,
        predicted_bill=1640,
        status="Demo Prediction"
    )