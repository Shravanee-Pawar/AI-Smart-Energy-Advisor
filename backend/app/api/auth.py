from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def auth_home():
    return {"message": "Authentication API Working"}