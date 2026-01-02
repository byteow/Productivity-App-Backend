from sqlalchemy.ext.asyncio import AsyncSession
from db import get_user_by_id
from fastapi import HTTPException

class Service:
    def __init__(self):
        ...

    
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