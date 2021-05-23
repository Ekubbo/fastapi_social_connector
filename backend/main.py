from api.routers import router as api_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(api_router, prefix="/api")
