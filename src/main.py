from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import (
    auth_router, 
    sms_router, 
    profile_router,
    survey_router
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

app.include_router(auth_router, tags=["Authorization"])
app.include_router(sms_router, tags=["Codes"])
app.include_router(profile_router, tags=["Profile"])
app.include_router(survey_router, tags=["Survey"])