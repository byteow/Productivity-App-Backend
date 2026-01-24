from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, cast, Date, func
from db import PomodoroSessionDailyStat, get_week_range
from datetime import date

async def create_pomodoro_daily_stat(
    session: AsyncSession,
    *,
    user_id: int,
    count: int
) -> PomodoroSessionDailyStat:
    stat = PomodoroSessionDailyStat(
        user_id=user_id,
        count=count
    )
    session.add(stat)
    await session.commit()
    await session.refresh(stat)

    return stat

async def update_pomodoro_count_stat(
    session: AsyncSession,
    *,
    user_id: int
) -> int:
    today = date.today()
    query = update(PomodoroSessionDailyStat)\
        .where(
            and_(
                PomodoroSessionDailyStat.user_id == user_id,
                cast(PomodoroSessionDailyStat.created_at, Date) == today
            )
        )\
        .values(count=PomodoroSessionDailyStat.count + 1)
    result = await session.execute(query)
    await session.commit()

    return result.rowcount

async def get_pomodoro_total_stats(
    session: AsyncSession,
    *,
    user_id: int
) -> dict[str, int]:
    today = date.today()
    start_of_week, end_of_week = get_week_range()

    query = select(
            func.sum(PomodoroSessionDailyStat.count).label("total"),
            func.sum(PomodoroSessionDailyStat.count)\
                .filter(
                    cast(PomodoroSessionDailyStat.created_at, Date) == today
                ).label("daily"),
            func.sum(PomodoroSessionDailyStat.count)\
                .filter(
                    cast(PomodoroSessionDailyStat.created_at, Date).between(start_of_week, end_of_week)
                ).label("weekly")
        )\
        .where(PomodoroSessionDailyStat.user_id == user_id)
    
    result = await session.execute(query)
    stats = result.mappings().one()
    
    return {
        "total": stats["total"] or 0,
        "daily": stats["daily"] or 0,
        "weekly": stats["weekly"] or 0
    }