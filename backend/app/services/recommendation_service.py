import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.schemas.chat import ChatResponse

# Load environment variables
load_dotenv()

# Read Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-flash-latest")

def get_recommendation(message: str) -> ChatResponse:
    """
    Send the user's question to Gemini and return the response.
    """

    response = model.generate_content(message)

    return ChatResponse(
        reply=response.text
    )