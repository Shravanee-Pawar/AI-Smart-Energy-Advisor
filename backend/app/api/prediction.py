from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def prediction_home():
    return {"message": "Prediction API Working"}