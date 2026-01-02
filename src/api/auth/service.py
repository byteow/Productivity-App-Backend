from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import LoginSchema, SignUpSchema, RefreshSchema
from pydantic import EmailStr
from hashlib import md5
from fastapi import HTTPException
from db import (
    get_user_by_email,
    create_user,
    get_last_send_code,
    Service as CodeService
)
from services import JWTSecurity

class Service:
    def __init__(self):
        self.jwt = JWTSecurity()


    def _generate_token_pair(self, user_id: int):
        payload = { "user_id": user_id }
        return {
            "access_token": self.jwt.create_access_token(payload),
            "refresh_token": self.jwt.create_refresh_token(payload)
        }

    
    async def login(self, schema: LoginSchema, db: AsyncSession):
        user = await get_user_by_email(db, email=schema.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        password_hash = md5(schema.password.encode()).hexdigest()
        if user.password != password_hash:
            raise HTTPException(status_code=404, detail="User not found")

        last_code = await get_last_send_code(db, email=schema.email, service=CodeService.LOGIN)
        if not last_code or last_code.code != schema.code:
            raise HTTPException(status_code=400, detail="Invalid code")

        return {
            **self._generate_token_pair(user.id),
            "user_id": user.id
        }
    

    async def signup(self, schema: SignUpSchema, db: AsyncSession):
        user = await get_user_by_email(db, email=schema.email)
        if user:
            raise HTTPException(status_code=400, detail="User already exists")

        password_hash = md5(schema.password.encode()).hexdigest()

        last_code = await get_last_send_code(db, email=schema.email, service=CodeService.SIGNUP)
        if not last_code or last_code.code != schema.code:
            raise HTTPException(status_code=400, detail="Invalid code")

        user = await create_user(
            db,
            name=schema.name,
            email=schema.email,
            password=password_hash,
            birthday=schema.birthday,
            gender=schema.gender
        )

        return {
            **self._generate_token_pair(user.id),
            "user_id": user.id
        }
    

    async def auth_state(self, user_id: int):
        return { "user_id": user_id }
    

    async def user_exists(self, email: EmailStr, db: AsyncSession):
        user = await get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(404, detail="User not found")
        return { "message": "User exists" }
    

    async def refresh(self, schema: RefreshSchema):
        data = self.jwt.verify_refresh_token(schema.refresh_token)
        if not data:
            raise HTTPException(400, detail="Invalid refresh token")
        return self._generate_token_pair(data["user_id"])