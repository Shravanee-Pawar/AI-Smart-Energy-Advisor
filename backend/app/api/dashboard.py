from fastapi import APIRouter
from typing import List

from app.schemas.dashboard import (
    DashboardResponse,
    ChartData
)

from app.services.dashboard_service import (
    get_dashboard_data,
    get_chart_data
)


router = APIRouter()



@router.get("/")
def get_dashboard(uid:str):

    return get_dashboard_data(uid)



@router.get("/chart")
def dashboard_chart():

    return get_chart_data()