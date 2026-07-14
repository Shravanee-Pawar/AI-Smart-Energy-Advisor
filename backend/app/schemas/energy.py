from pydantic import BaseModel


class EnergyRequest(BaseModel):
    uid: str
    month: str
    units: float
    bill: float


class EnergyResponse(BaseModel):
    record_id: str
    uid: str
    month: str
    units: float
    bill: float