from pydantic import BaseModel, EmailStr
from db import Service

class SendCodeSchema(BaseModel):
    email: EmailStr
    service: Service

class CheckCodeSchema(BaseModel):
    email: EmailStr
    service: Service
    code: int