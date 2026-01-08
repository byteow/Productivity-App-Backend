from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func, delete, or_
from db import TaskPriority, Task, TaskStatus
from datetime import timedelta
from typing import List

async def create_task(
    session: AsyncSession,
    *,
    user_id: int,
    category: str,
    description: str,
    status: TaskStatus,
    priority: TaskPriority,
    is_pinned: bool
) -> Task:
    task = Task(
        user_id=user_id,
        category=category,
        description=description,
        status=status,
        priority=priority,
        is_pinned=is_pinned
    )
    session.add(task)

    await session.commit()
    await session.refresh(task)

    return task

async def get_user_tasks(
    session: AsyncSession,
    *,
    user_id: int
) -> List[Task]:
    threshold = func.now() - timedelta(hours=24)
    query = select(Task)\
        .where(
            and_(
                Task.user_id == user_id,
                or_(
                    Task.is_pinned, 
                    Task.created_at > threshold
                )
            )
        )
    result = await session.execute(query)
    return result.scalars().all()

async def update_user_task(
    session: AsyncSession,
    *,
    user_id: int,
    task_id: int,
    **kwargs
) -> int:
    query = update(Task)\
        .where(and_(Task.id == task_id, Task.user_id == user_id))\
        .values(**kwargs)
    result = await session.execute(query)
    await session.commit()
    return result.rowcount

async def delete_user_task(
    session: AsyncSession,
    *,
    user_id: int,
    task_id: int
) -> int:
    query = delete(Task)\
        .where(and_(Task.id == task_id, Task.user_id == user_id))
    result = await session.execute(query)
    await session.commit()
    return result.rowcount

async def delete_task(
    session: AsyncSession,
    *,
    task_id: int
) -> int:
    query = delete(Task)\
        .where(Task.id == task_id)
    result = await session.execute(query)
    await session.commit()
    return result.rowcount

async def get_user_tasks_count(
    session: AsyncSession,
    *,
    user_id: int
) -> dict[str, int]:
    threshold = func.now() - timedelta(hours=24)
    query = select(
        func.count(Task.id).label("total"),
        func.count(Task.id).filter(Task.is_pinned == True).label("pinned")
    ).where(
        and_(
            Task.user_id == user_id,
            Task.created_at > threshold
        )
    )
    
    result = await session.execute(query)
    stats = result.mappings().one()
    
    return {
        "total": stats["total"],
        "pinned": stats["pinned"]
    }