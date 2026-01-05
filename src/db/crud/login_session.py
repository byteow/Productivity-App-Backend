from sqlalchemy.ext.asyncio import AsyncSession
from db import LoginSession

async def create_login_session(
    session: AsyncSession,
    *,
    user_id: int,
    ip: str,
    os: str,
    client_app: str,
    is_mobile_device: bool
) -> LoginSession:
    log_session = LoginSession(
        user_id=user_id,
        ip=ip,
        os=os,
        client_app=client_app,
        is_mobile_device=is_mobile_device
    )
    session.add(log_session)
    await session.commit()
    await session.refresh(log_session)
    return log_session