from fastapi import APIRouter

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
)
from app.services.auth_service import (
    create_user,
    verify_user,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest):
    return create_user(
        name=request.name,
        email=request.email,
        password=request.password,
        phone=request.phone
    )


@router.post("/login")
def login(request: LoginRequest):
    user = verify_user(request.id_token)

    return {
        "message": "Login successful",
        "user": user
    }