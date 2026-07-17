from pydantic import BaseModel


class EnergyRequest(BaseModel):
    uid: str
    month: str
    units: float
    bill: float

    rate: float
    family_members: int
    house_type: str

    ac_hours: float
    fan_hours: float
    tv_hours: float

    refrigerator: bool
    washing_machine: bool
    cooler: bool
    other_appliances: bool


class EnergyResponse(BaseModel):
    record_id: str
    uid: str
    month: str
    units: float
    bill: float