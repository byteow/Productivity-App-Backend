from sqlalchemy.ext.asyncio import AsyncSession
from db import (
    update_user,
    get_user_by_id,
    Service as CodeService
)
from .schemas import UpdateEmailSchema, UpdateMetaInfoSchema, UpdatePasswordSchema
from fastapi import HTTPException
from services import get_otp_manager, hash_password

class Service:
    def __init__(self):
        self.otp_manager = get_otp_manager()

    
    async def me(self, user_id: int, db: AsyncSession):
        user = await get_user_by_id(db, id=user_id)
        if not user:
            raise HTTPException(404, detail="User not found")
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "gender": user.gender,
            "birthday": user.birthday
        }
    

    async def update_meta_info(self, schema: UpdateMetaInfoSchema, user_id: int, db: AsyncSession):
        data_for_update = {}
        if schema.name:
            data_for_update["name"] = schema.name
        if schema.gender:
            data_for_update["gender"] = schema.gender
        if schema.birthday:
            data_for_update["birthday"] = schema.birthday

        await update_user(db, id=user_id, **data_for_update)

        return { "message": "Profile successfully updated" }
    

    async def update_email(self, schema: UpdateEmailSchema, user_id: int, db: AsyncSession):
        is_valid_code = await self.otp_manager.verify_otp(schema.email, schema.code, CodeService.UPDATE)
        if not is_valid_code:
            raise HTTPException(400, detail="Invalid code")
        
        await update_user(db, id=user_id, email=schema.email)
        return { "message": "Email successfully updated" }

    
    async def update_password(self, schema: UpdatePasswordSchema, user_id: int, db: AsyncSession):
        user = await get_user_by_id(db, id=user_id)
        if not user:
            raise HTTPException(404, detail="User not found")
        
        old_pass_hash = hash_password(schema.old_password)
        if user.password != old_pass_hash:
            raise HTTPException(400, detail="Incorrect password")
        
        new_pass_hash = hash_password(schema.new_password)
        await update_user(db, id=user_id, password=new_pass_hash)

        return { "message": "Password successfully updated" }