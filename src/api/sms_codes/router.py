from fastapi import APIRouter, Depends
from .service import Service
from db import get_session
from .schemas import SendCodeSchema, CheckCodeSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/codes")
service = Service()

@router.post("/send")
async def send_code(schema: SendCodeSchema, db: AsyncSession=Depends(get_session)):
    return await service.send(schema, db)

@router.get("/check_code")
async def check_code(schema: CheckCodeSchema=Depends(), db: AsyncSession=Depends(get_session)):
    return await service.check_code(schema, db)