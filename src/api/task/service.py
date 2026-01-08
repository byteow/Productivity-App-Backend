from sqlalchemy.ext.asyncio import AsyncSession
from db import (
    get_user_tasks_count,
    create_task as new_task,
    get_user_tasks,
    delete_user_task,
    update_user_task,
    TaskStatus
)
from fastapi import HTTPException
from .constants import MAX_PINNED_TASKS_COUNT, MAX_TASKS_COUNT
from .schemas import CreateTaskSchema, UpdateTaskSchema, DeleteTaskSchema

class Service:
    def __init__(self):
        ...

    
    async def create_task(self, schema: CreateTaskSchema, user_id: int, db: AsyncSession):
        count_stats = await get_user_tasks_count(db, user_id=user_id)

        if count_stats["total"] >= MAX_TASKS_COUNT:
            raise HTTPException(400, detail="Too many tasks")
        
        if count_stats["pinned"] >= MAX_PINNED_TASKS_COUNT and schema.is_pinned:
            raise HTTPException(400, detail="Too many pinned tasks")
        
        task = await new_task(
            db,
            user_id=user_id,
            category=schema.category,
            description=schema.description,
            status=TaskStatus.IN_PROGRESS,
            priority=schema.priority,
            is_pinned=schema.is_pinned
        )

        return {"task_id": task.id}
    

    async def get_tasks_list(self, user_id: int, db: AsyncSession):
        tasks = await get_user_tasks(db, user_id=user_id)
        return {
            "tasks": [
                {
                    "id": task.id,
                    "category": task.category,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "is_pinned": task.is_pinned
                } for task in tasks
            ]
        }
    

    async def update_task(self, schema: UpdateTaskSchema, user_id: int, db: AsyncSession):
        data = schema.model_dump(exclude_none=True, exclude={"task_id"})
        rowcount = await update_user_task(
            db,
            user_id=user_id,
            task_id=schema.task_id,
            **data
        )
        if rowcount == 0:
            raise HTTPException(404, detail="Task not found")
        return {"message": "Task successfully updated"}
    

    async def delete_task(self, schema: DeleteTaskSchema, user_id: int, db: AsyncSession):
        rowcount = await delete_user_task(
            db,
            user_id=user_id,
            task_id=schema.task_id
        )
        if rowcount == 0:
            raise HTTPException(404, detail="Task not found")
        return {"message": "Task successfully deleted"}