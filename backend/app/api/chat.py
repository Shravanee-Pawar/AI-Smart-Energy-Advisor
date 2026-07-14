from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.recommendation_service import get_recommendation

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat with Gemini AI
    """
    return get_recommendation(request.message)