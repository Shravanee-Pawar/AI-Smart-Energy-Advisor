import os

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

from app.schemas.chat import ChatResponse

# -----------------------------------------
# Load Environment Variables
# -----------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not found in .env file.")

# -----------------------------------------
# Configure Gemini
# -----------------------------------------

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


# -----------------------------------------
# Generate Recommendation
# -----------------------------------------

def get_recommendation(message: str) -> ChatResponse:
    """
    Send the user's question to Gemini
    and return the AI response.
    """

    try:

        response = model.generate_content(message)

        reply = response.text.strip()

        if not reply:
            reply = "The AI assistant did not return a response."

        return ChatResponse(
            reply=reply
        )

    except ResourceExhausted:

        return ChatResponse(
            reply=(
                "The AI assistant is temporarily unavailable because the "
                "Gemini API rate limit has been reached. "
                "Please wait about a minute and try again."
            )
        )

    except Exception as e:

        print("Gemini Error:", e)

        return ChatResponse(
            reply=(
                "Sorry, I am unable to connect with the AI service right now. "
                "Please try again later."
            )
        )