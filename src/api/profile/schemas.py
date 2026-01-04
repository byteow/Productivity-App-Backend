from pydantic import EmailStr, BaseModel, Field
from typing import Optional
from db import Gender
from datetime import date

class UpdateMetaInfoSchema(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=32)
    gender: Optional[Gender] = None
    birthday: Optional[date] = None    

class UpdateEmailSchema(BaseModel):
    email: EmailStr
    code: int

class UpdatePasswordSchema(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)