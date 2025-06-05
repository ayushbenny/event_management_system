from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from event_management.api.v1.endpoints import api_router as event_management_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_management_router, prefix="/event", tags=["event_management"])
