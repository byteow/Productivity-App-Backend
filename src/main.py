from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api import (
    auth_router, 
    sms_router, 
    profile_router,
    survey_router,
    ws_router
)
from services import ErrorHandlingMiddleware
from config import CORS_ORIGINS

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(ErrorHandlingMiddleware)

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, tags=["Authorization"])
api_router.include_router(sms_router, tags=["Codes"])
api_router.include_router(profile_router, tags=["Profile"])
api_router.include_router(survey_router, tags=["Survey"])
api_router.include_router(ws_router, tags=["WebSocket"])

app.include_router(api_router)