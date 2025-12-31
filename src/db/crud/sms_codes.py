from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from db import SmsCodes, Service
from datetime import datetime, timedelta, timezone
from typing import List

def _get_code_exp_delta():
    return datetime.now(timezone.utc) - timedelta(minutes=15)

async def create_sms_code(
    session: AsyncSession,
    *,
    email: str,
    service: Service,
    code: int
) -> SmsCodes:
    sms_code = SmsCodes(email=email, service=service, code=code)
    session.add(sms_code)
    await session.commit()
    await session.refresh(sms_code)
    return sms_code


async def get_recent_send_codes(
    session: AsyncSession,
    *,
    email: str,
    service: Service
) -> List[SmsCodes] | None:
    delta = _get_code_exp_delta()

    query = select(SmsCodes)\
        .where(
            and_(
                SmsCodes.email == email, 
                and_(
                    SmsCodes.service == service.value,
                    SmsCodes.created_at >= delta
                )
            )
        ).limit(3)
    result = await session.execute(query)
    return result.scalars().all()


async def get_send_code_by_code(
    session: AsyncSession,
    *,
    code: int
) -> SmsCodes | None:
    query = select(SmsCodes).where(SmsCodes.code == code)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_last_send_code(
    session: AsyncSession,
    *,
    email: str,
    service: Service
) -> SmsCodes | None:
    detla = _get_code_exp_delta()
    query = select(SmsCodes)\
        .where(
            and_(
                SmsCodes.email == email, 
                and_(
                    SmsCodes.service == service.value,
                    SmsCodes.created_at >= detla
                )
            )
        )\
        .order_by(SmsCodes.id.desc()).limit(1)
    result = await session.execute(query)
    return result.scalar_one_or_none()