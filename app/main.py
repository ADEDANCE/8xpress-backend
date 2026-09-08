from fastapi import FastAPI
from app.routes.menu import router as menu_router

app = FastAPI()

app.include_router(menu_router, prefix="/menu", tags=["Menu"])


@app.get("/")
def home():
    return {"message": "8Xpress API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "8Xpress API"
    }