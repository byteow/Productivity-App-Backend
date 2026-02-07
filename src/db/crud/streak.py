from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, cast, Date
from db import Streak
from typing import List
from db.utils import get_month_range

async def create_streak(
    session: AsyncSession,
    *,
    user_id: int,
    day_tip: str
) -> Streak:
    streak = Streak(
        user_id=user_id,
        day_tip=day_tip
    )
    session.add(streak)
    await session.commit()
    await session.refresh(streak)
    return streak

async def get_user_monthly_streaks(
    session: AsyncSession,
    *,
    user_id: int
) -> List[Streak]:
    start_month, end_month = get_month_range()

    query = select(Streak)\
        .where(
            and_(
                Streak.user_id == user_id,
                cast(Streak.created_at, Date).between(start_month, end_month)
            )
        )
    result = await session.execute(query)
    return result.scalars().all()

async def delete_user_streaks(
    session: AsyncSession,
    *,
    user_id: int
) -> None:
    query = delete(Streak).where(Streak.user_id == user_id)
    await session.execute(query)
    await session.commit()