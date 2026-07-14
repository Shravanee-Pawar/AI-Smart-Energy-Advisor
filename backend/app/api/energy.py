from typing import List

from fastapi import APIRouter

from app.schemas.energy import EnergyRequest, EnergyResponse
from app.services.energy_service import (
    save_energy,
    get_all_energy,
    get_energy_by_user
)

router = APIRouter()


@router.post("/", response_model=EnergyResponse)
def create_energy(request: EnergyRequest):
    """
    Save a new energy usage record.
    """
    return save_energy(request)


@router.get("/", response_model=List[EnergyResponse])
def read_all_energy():
    """
    Get all energy records.
    """
    return get_all_energy()


@router.get("/{uid}", response_model=List[EnergyResponse])
def read_user_energy(uid: str):
    """
    Get all energy records for a specific user.
    """
    return get_energy_by_user(uid)