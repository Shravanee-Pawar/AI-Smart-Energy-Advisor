from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME = "AI Smart Energy Advisor"
    VERSION = "1.0.0"

    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()