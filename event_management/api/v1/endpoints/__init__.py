from fastapi import APIRouter
from .routes import event_management_router

api_router = APIRouter()
api_router.include_router(event_management_router, prefix="/v1", tags=["event_management"])
