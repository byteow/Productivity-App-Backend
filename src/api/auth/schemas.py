from pydantic import BaseModel, Field
from db import Gender

class LoginSchema(BaseModel):
    email: str
    password: str
    code: int

class SignUpSchema(BaseModel):
    name: str
    email: str
    password: str
    age: int = Field(ge=14, le=100)
    gender: Gender
    code: int