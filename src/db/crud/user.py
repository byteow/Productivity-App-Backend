from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from typing import Optional
from db import User, Gender

async def create_user(
    session: AsyncSession,
    *,
    name: str,
    email: str,
    password: str,
    birthday: Optional[date],
    gender: Gender
) -> User:
    user = User(
        name=name,
        email=email,
        password=password,
        birthday=birthday,
        gender=gender
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_email(
    session: AsyncSession,
    *,
    email: str
) -> User | None:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_id(
    session: AsyncSession,
    *,
    id: int
) -> User | None:
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    return result.scalar_one_or_none()