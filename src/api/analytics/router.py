from fastapi import APIRouter, Depends
from .service import Service
from db import get_session
from services import secure_access, get_client_ip_address
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/analytics")
service = Service()

@router.get("/productivity")
async def productivity(
    db: AsyncSession=Depends(get_session),
    user_id: int=Depends(secure_access)
):
    return await service.productivity(user_id, db)

@router.get("/analytics_stats")
async def analytics_stats(
    db: AsyncSession=Depends(get_session),
    user_id: int=Depends(secure_access)
):
    return await service.analytics_stats(user_id, db)

@router.put("/pomodoro")
async def increment_pomodoro(
    user_id: int=Depends(secure_access),
    _=Depends(RateLimiter(times=1, minutes=30, identifier=get_client_ip_address)),
    db: AsyncSession=Depends(get_session)
):
    return await service.increment_pomodoro(user_id, db)