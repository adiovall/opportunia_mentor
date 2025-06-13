from fastapi import FastAPI
from backend.routes import auth_router

app = FastAPI(debug=True, title="Opportunia Mentor API")

@app.get("/")
async def root():
    return {"message": "Opportunia Mentor API - v1", "time": "01:15 AM WAT, June 13, 2025"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])