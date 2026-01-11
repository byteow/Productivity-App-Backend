from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db import Streak

async def create_streak(
    session: AsyncSession,
    *,
    user_id: int,
    streak_days: int,
    is_active: bool,
    penalty_days: int,
) -> Streak:
    streak = Streak(
        user_id=user_id,
        streak_days=streak_days,
        is_active=is_active,
        penalty_days=penalty_days
    )
    session.add(streak)
    await session.commit()
    await session.refresh(streak)
    return streak

async def get_user_streak(
    session: AsyncSession,
    *,
    user_id: int
) -> Streak | None:
    query = select(Streak).where(Streak.user_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def update_user_streak(
    session: AsyncSession,
    *,
    user_id: int,
    **kwargs
) -> None:
    query = update(Streak)\
        .where(Streak.user_id == user_id)\
        .values(**kwargs)
    await session.execute(query)
    await session.commit()

async def delete_user_streak(
    session: AsyncSession,
    *,
    user_id: int
) -> None:
    query = delete(Streak).where(Streak.user_id == user_id)
    await session.execute(query)
    await session.commit()