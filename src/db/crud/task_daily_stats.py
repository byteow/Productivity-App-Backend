from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, cast, Date, func
from db import TaskDailyStat
from db.utils import get_week_range
from datetime import datetime, date

async def create_task_daily_stat(
    session: AsyncSession,
    *,
    user_id: int,
    count: int,
    points: int
) -> TaskDailyStat:
    stat = TaskDailyStat(
        user_id=user_id,
        count=count,
        points=points
    )
    session.add(stat)
    await session.commit()
    await session.refresh(stat)

    return stat

async def update_task_count_stat(
    session: AsyncSession,
    is_increment: bool,
    *,
    user_id: int,
    points: int,
    _datetime: datetime
) -> int:
    _date = _datetime.date()
    query = update(TaskDailyStat)\
        .where(
            and_(
                TaskDailyStat.user_id == user_id,
                cast(TaskDailyStat.created_at, Date) == _date
            )
        )\
        .values(
            count=((TaskDailyStat.count + 1) if is_increment else (TaskDailyStat.count - 1)),
            points=((TaskDailyStat.points + points) if is_increment else (TaskDailyStat.points - points))
        )
    result = await session.execute(query)
    await session.commit()

    return result.rowcount

async def get_weekly_stats(
    session: AsyncSession,
    *,
    user_id: int
) -> list[dict]:
    start_of_week, end_of_week = get_week_range()

    query = select(TaskDailyStat.points, TaskDailyStat.created_at)\
        .where(
            and_(
                TaskDailyStat.user_id == user_id,
                cast(TaskDailyStat.created_at, Date).between(start_of_week, end_of_week)
            )
        )
    result = await session.execute(query)
    return [row._asdict() for row in result]

async def get_tasks_total_stats(
    session: AsyncSession,
    *,
    user_id: int
) -> dict[str, int]:
    today = date.today()
    start_of_week, end_of_week = get_week_range()

    query = select(
            func.sum(TaskDailyStat.count).label("total"),
            func.sum(TaskDailyStat.count)\
                .filter(
                    cast(TaskDailyStat.created_at, Date) == today
                ).label("daily"),
            func.sum(TaskDailyStat.count)\
                .filter(
                    cast(TaskDailyStat.created_at, Date).between(start_of_week, end_of_week)
                ).label("weekly")
        )\
        .where(TaskDailyStat.user_id == user_id)
    
    result = await session.execute(query)
    stats = result.mappings().one()
    
    return {
        "total": stats["total"] or 0,
        "daily": stats["daily"] or 0,
        "weekly": stats["weekly"] or 0
    }