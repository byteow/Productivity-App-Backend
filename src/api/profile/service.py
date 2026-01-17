from sqlalchemy.ext.asyncio import AsyncSession
from db import (
    update_user,
    get_user_by_id,
    update_user_streak,
    create_streak,
    get_user_by_email,
    Service as CodeService
)
from .schemas import (
    UpdateEmailSchema, 
    UpdateMetaInfoSchema, 
    UpdatePasswordSchema,
    GetMyProfileSchema
)
from fastapi import HTTPException
from services import get_otp_manager, hash_password
from datetime import date, timedelta
from .enums import Language
import os
import json
import random

class Service:
    def __init__(self):
        self.otp_manager = get_otp_manager()
        self.tips = {
            Language.RU: json.loads(open(os.path.join('tips', 'ru_tips.json')).read()),
            Language.EN: json.loads(open(os.path.join('tips', 'en_tips.json')).read())
        }

    
    def _random_tip(self, lang: Language):
        return random.choice(self.tips[lang])
    

    async def me(self, schema: GetMyProfileSchema, user_id: int, db: AsyncSession):
        user = await get_user_by_id(db, id=user_id)
        if not user:
            raise HTTPException(404, detail="User not found")
        
        rt = lambda: self._random_tip(schema.lang)

        if not user.streak:
            user.streak = await create_streak(
                db,
                user_id=user_id,
                streak_days=1,
                is_active=True,
                penalty_days=0,
                day_tip=rt()
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
                kwargs = { "is_active": True, "penalty_days": 0 , "streak_days": 1 } if penalty_days >= 3 else { "penalty_days": penalty_days }
            elif not user.streak.is_active and update_date < yesterday:
                kwargs = { "penalty_days": 0 }
            if kwargs:
                kwargs["day_tip"] = rt()
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
                "penalty_days": user.streak.penalty_days,
                "day_tip": user.streak.day_tip
            }
        }
    

    async def update_meta_info(self, schema: UpdateMetaInfoSchema, user_id: int, db: AsyncSession):
        data = schema.model_dump(exclude_none=True, include={'birthday', 'name', 'gender'})
        data["birthday"] = schema.birthday
        await update_user(db, id=user_id, **data)
        return { "message": "Profile successfully updated" }
    

    async def update_email(self, schema: UpdateEmailSchema, user_id: int, db: AsyncSession):
        user = await get_user_by_email(db, email=schema.email)
        if user:
            raise HTTPException(400, detail="User with such email already exists")

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