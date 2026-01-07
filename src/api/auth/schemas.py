from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
from db import Gender

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    code: int

class SignUpSchema(BaseModel):
    name: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=6)
    birthday: Optional[date] = None
    gender: Gender
    code: int

class UserExistsSchema(BaseModel):
    email: EmailStr

class RefreshSchema(BaseModel):
    refresh_token: str