from fastapi import FastAPI

from app.database import Base, engine
from app.routers import router

# Create all tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Webhook Retry Service",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Webhook Retry Service is running"
    }