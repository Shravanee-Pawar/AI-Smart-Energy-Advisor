from fastapi import FastAPI

from app.api import auth, energy, prediction, chat, dashboard, profile

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Smart Energy Advisor API",
    version="1.0.0"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(energy.router, prefix="/api/energy", tags=["Energy"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "AI Smart Energy Advisor"
    }