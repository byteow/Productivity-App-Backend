from fastapi import APIRouter, Depends
from .service import Service
from db import get_session
from services import secure_access
from .schemas import CreateTaskSchema, UpdateTaskSchema, DeleteTaskSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/task")
service = Service()

@router.post("/create")
async def create_task(
    schema: CreateTaskSchema,
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.create_task(schema, user_id, db)

@router.get("/list")
async def get_tasks_list(
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.get_tasks_list(user_id, db)

@router.put("/update")
async def update_task(
    schema: UpdateTaskSchema,
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.update_task(schema, user_id, db)

@router.delete("/delete")
async def delete_task(
    schema: DeleteTaskSchema=Depends(),
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.delete_task(schema, user_id, db)