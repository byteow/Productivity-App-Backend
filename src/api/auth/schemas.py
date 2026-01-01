from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
from db import Gender

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    code: int

class SignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    birthday: Optional[date]
    gender: Gender
    code: int

class UserExistsSchema(BaseModel):
    email: EmailStr