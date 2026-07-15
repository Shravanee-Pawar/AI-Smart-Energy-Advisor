from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_records: int
    total_units: float
    average_daily: float
    estimated_bill: float
    latest_consumption: float
    latest_bill: float
    
class ChartData(BaseModel):
    month: str
    units: float