from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def energy_home():
    return {"message": "Energy API Working"}