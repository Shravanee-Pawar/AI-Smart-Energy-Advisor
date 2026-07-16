from fastapi import APIRouter, HTTPException, Depends

from app.core.security import verify_firebase_token

from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdateRequest,
)
from app.services.profile_service import (
    get_profile,
    update_profile,
)

router = APIRouter()


@router.get("/", response_model=ProfileResponse)
def read_profile(
    current_user: dict = Depends(verify_firebase_token),
):
    uid = current_user["uid"]
    profile = get_profile(uid)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return profile


@router.put("/{uid}", response_model=ProfileResponse)
def edit_profile(uid: str, profile: ProfileUpdateRequest):
    existing = get_profile(uid)

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    updated_profile = update_profile(
        uid,
        profile.model_dump()
    )

    return updated_profile