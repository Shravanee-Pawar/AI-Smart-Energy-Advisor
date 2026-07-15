from pydantic import BaseModel


class ProfileResponse(BaseModel):
    uid: str
    name: str
    email: str
    phone: str
    address: str
    household_size: int
    tariff: str


class ProfileUpdateRequest(BaseModel):
    name: str
    phone: str
    address: str
    household_size: int
    tariff: str