from fastapi import APIRouter, HTTPException

from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdateRequest,
)
from app.services.profile_service import (
    get_profile,
    update_profile,
)

router = APIRouter()


@router.get("/{uid}", response_model=ProfileResponse)
def read_profile(uid: str):
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