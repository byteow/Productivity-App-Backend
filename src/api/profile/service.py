from sqlalchemy.ext.asyncio import AsyncSession
from db import (
    update_user,
    get_user_by_id,
    get_user_streak,
    update_user_streak,
    create_streak,
    Service as CodeService
)
from .schemas import UpdateEmailSchema, UpdateMetaInfoSchema, UpdatePasswordSchema
from fastapi import HTTPException
from services import get_otp_manager, hash_password
from datetime import date, timedelta

class Service:
    def __init__(self):
        self.otp_manager = get_otp_manager()

    
    async def me(self, user_id: int, db: AsyncSession):
        user = await get_user_by_id(db, id=user_id)
        if not user:
            raise HTTPException(404, detail="User not found")
        
        if not user.streak:
            user.streak = await create_streak(
                db,
                user_id=user_id,
                streak_days=1,
                is_active=True,
                penalty_days=0
            )
        today = date.today()
        
        if user.streak and user.streak.updated_at.date() != today:
            kwargs = {}
            yesterday = today - timedelta(days=1)
            update_date = user.streak.updated_at.date()

            if user.streak.is_active and update_date == yesterday:
                kwargs = { "streak_days": user.streak.streak_days + 1 }
            elif user.streak.is_active and update_date < yesterday:
                kwargs = { "is_active": False, "streak_days": 0 }
            elif not user.streak.is_active and update_date == yesterday:
                penalty_days = user.streak.penalty_days + 1
                kwargs = { "is_active": True, "penalty_days": 0 , "streak_days": 1} if penalty_days >= 3 else { "penalty_days": penalty_days }
            elif not user.streak.is_active and update_date < yesterday:
                kwargs = { "penalty_days": 0 }
            if kwargs:
                await update_user_streak(db, user_id=user_id, **kwargs)
                for key, value in kwargs.items():
                    setattr(user.streak, key, value)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "gender": user.gender,
            "birthday": user.birthday,
            "streak": {
                "is_active": user.streak.is_active,
                "streak_days": user.streak.streak_days,
                "penalty_days": user.streak.penalty_days
            }
        }
    

    async def update_meta_info(self, schema: UpdateMetaInfoSchema, user_id: int, db: AsyncSession):
        data_for_update = {}
        data_for_update["birthday"] = schema.birthday

        if schema.name:
            data_for_update["name"] = schema.name
        if schema.gender:
            data_for_update["gender"] = schema.gender
            
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