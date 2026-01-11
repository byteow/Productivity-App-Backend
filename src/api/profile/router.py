from fastapi import APIRouter, Depends
from .service import Service
from .schemas import (
    UpdateEmailSchema, 
    UpdateMetaInfoSchema, 
    UpdatePasswordSchema,
    GetMyProfileSchema
)
from db import get_session
from services import secure_access
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/profile")
service = Service()

@router.get("/me")
async def me(
    schema: GetMyProfileSchema=Depends(),
    user_id: int=Depends(secure_access), 
    db: AsyncSession=Depends(get_session)
):
    return await service.me(schema, user_id, db)

@router.put("/meta_info")
async def update_meta_info(
    schema: UpdateMetaInfoSchema, 
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.update_meta_info(schema, user_id, db)

@router.put("/email")
async def update_email(
    schema: UpdateEmailSchema, 
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.update_email(schema, user_id, db)

@router.put("/password")
async def update_password(
    schema: UpdatePasswordSchema, 
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.update_password(schema, user_id, db)