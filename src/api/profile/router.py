from fastapi import APIRouter, Depends
from .service import Service
from db import get_session
from services import secure_access
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/profile")
service = Service()

@router.get("/me")
async def me(user_id: int=Depends(secure_access), db: AsyncSession=Depends(get_session)):
    return await service.me(user_id, db)