from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
    LoginSchema, 
    SignUpSchema, 
    RefreshSchema, 
    RecoveryPasswordSchema
)
from pydantic import EmailStr
from fastapi import HTTPException
from db import (
    get_user_by_email,
    create_user,
    update_user,
    create_login_session,
    Service as CodeService
)
from services import JWTSecurity, get_otp_manager, hash_password

class Service:
    def __init__(self):
        self.jwt = JWTSecurity()
        self.otp_manager = get_otp_manager()


    def _generate_token_pair(self, user_id: int):
        payload = { "user_id": user_id }
        return {
            "access_token": self.jwt.create_access_token(payload),
            "refresh_token": self.jwt.create_refresh_token(payload)
        }


    async def _save_login_session(self, db: AsyncSession, user_id: int, dev_info: dict):
        await create_login_session(
            db,
            user_id=user_id,
            ip=dev_info.get("ip"),
            os=dev_info.get("os"),
            client_app=dev_info.get("client_app"),
            is_mobile_device=dev_info.get("is_mobile_device")
        )

    
    async def login(self, schema: LoginSchema, db: AsyncSession, dev_info: dict):
        user = await get_user_by_email(db, email=schema.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        password_hash = hash_password(schema.password)
        if user.password != password_hash:
            raise HTTPException(status_code=404, detail="User not found")

        is_valid_code = await self.otp_manager.verify_otp(schema.email, schema.code, CodeService.LOGIN)
        if not is_valid_code:
            raise HTTPException(status_code=400, detail="Invalid code")

        await self._save_login_session(db, user.id, dev_info)

        return {
            **self._generate_token_pair(user.id),
            "user_id": user.id
        }
    

    async def signup(self, schema: SignUpSchema, db: AsyncSession, dev_info: dict):
        user = await get_user_by_email(db, email=schema.email)
        if user:
            raise HTTPException(status_code=400, detail="User already exists")

        password_hash = hash_password(schema.password)

        is_valid_code = await self.otp_manager.verify_otp(schema.email, schema.code, CodeService.SIGNUP)
        if not is_valid_code:
            raise HTTPException(status_code=400, detail="Invalid code")

        user = await create_user(
            db,
            name=schema.name,
            email=schema.email,
            password=password_hash,
            birthday=schema.birthday,
            gender=schema.gender
        )

        await self._save_login_session(db, user.id, dev_info)

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
    

    async def recovery_passwowrd(self, schema: RecoveryPasswordSchema, db: AsyncSession):
        user = await get_user_by_email(db, email=schema.email)
        if not user:
            raise HTTPException(404, detail="User not found")
        
        is_valid_code = await self.otp_manager.verify_otp(schema.email, schema.code, CodeService.RECOVERY)
        if not is_valid_code:
            raise HTTPException(status_code=400, detail="Invalid code")

        new_password = hash_password(schema.new_password)
        await update_user(db, id=user.id, password=new_password)

        return { "message": "Password successfully recovered" }