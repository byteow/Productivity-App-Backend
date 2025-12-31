from fastapi import FastAPI
from api import auth_router, sms_router
from services import ErrorHandlingMiddleware

app = FastAPI()

app.add_middleware(ErrorHandlingMiddleware)

app.include_router(auth_router)
app.include_router(sms_router)