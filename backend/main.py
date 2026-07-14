from fastapi import FastAPI

from app.api import auth, energy, prediction, chat, dashboard

app = FastAPI(
    title="AI Smart Energy Advisor API",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api")
app.include_router(energy.router, prefix="/api/energy", tags=["Energy"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "AI Smart Energy Advisor"
    }