from fastapi import APIRouter, Depends
from .service import Service
from db import get_session
from services import secure_access
from .schemas import LoginSchema, SignUpSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth")
service = Service()

@router.post("/login")
async def login(schema: LoginSchema, db: AsyncSession=Depends(get_session)):
    return await service.login(schema, db)

@router.post("/signup")
async def signup(schema: SignUpSchema, db: AsyncSession=Depends(get_session)):
    return await service.signup(schema, db)

@router.get("/auth_state")
async def auth_state(user_id = Depends(secure_access)):
    return await service.auth_state(user_id)