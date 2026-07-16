import joblib
import pandas as pd
from pathlib import Path

from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)

# Folder containing this file
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_energy(data: PredictionRequest):

    df = pd.DataFrame([{
        "Year": data.Year,
        "Month": data.Month,
        "lag_1": data.lag_1,
        "lag_2": data.lag_2,
        "rolling_mean_3": data.rolling_mean_3
    }])

    scaled = scaler.transform(df)

    prediction = model.predict(scaled)[0]

    predicted_bill = prediction * 6

    return PredictionResponse(
        predicted_units=round(float(prediction), 2),
        predicted_bill=round(float(predicted_bill), 2),
        status="Prediction Successful"
    )