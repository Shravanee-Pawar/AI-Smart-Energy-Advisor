from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def recommendation_home():
    return {"message": "Recommendation API Working"}