from fastapi import APIRouter
from typing import List

from app.schemas.dashboard import DashboardResponse, ChartData
from app.services.dashboard_service import (
    get_dashboard_data,
    get_chart_data,
)

router = APIRouter()


@router.get("/", response_model=DashboardResponse)
def get_dashboard():
    return get_dashboard_data()

@router.get("/chart", response_model=List[ChartData])
def dashboard_chart():
    return get_chart_data()