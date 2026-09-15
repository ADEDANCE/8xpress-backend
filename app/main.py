from fastapi import FastAPI
from app.routes.menu import router as menu_router
from app.routes.auth import router as auth_router
from app.routes.order import router as order_router


app = FastAPI()


app.include_router(
    menu_router,
    prefix="/menu",
    tags=["Menu"]
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


app.include_router(
    order_router,
    prefix="/orders",
    tags=["Orders"]
)



@app.get("/")
def home():
    return {"message": "8Xpress API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "8Xpress API"
    }