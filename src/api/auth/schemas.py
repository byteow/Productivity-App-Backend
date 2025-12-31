from pydantic import BaseModel, Field, EmailStr
from db import Gender

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    code: int

class SignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int = Field(ge=14, le=100)
    gender: Gender
    code: int

class UserExistsSchema(BaseModel):
    email: EmailStr