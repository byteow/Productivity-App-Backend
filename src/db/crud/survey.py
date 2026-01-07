from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func, Date, cast
from db import SurveyStatus, Survey, SurveyAnswers
from datetime import timedelta, datetime
from typing import Optional

async def create_survey(
    session: AsyncSession,
    *,
    user_id: int,
    status: SurveyStatus,
    schema: Optional[str] = None
) -> Survey:
    survey = Survey(
        user_id=user_id,
        status=status,
        schema=schema
    )
    answers = SurveyAnswers(schema=None)
    survey.answers = answers

    session.add(survey)

    await session.commit()
    await session.refresh(survey)

    return survey

async def get_today_survey(
    session: AsyncSession,
    *,
    user_id: int
) -> Survey | None:
    query = select(Survey)\
        .where(
            and_(
                Survey.user_id == user_id,
                Survey.created_at > (func.now() - timedelta(hours=12)),
                cast(Survey.created_at, Date) == datetime.now().date()
            )
        )
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def update_survey(
    session: AsyncSession,
    *,
    survey_id: int,
    **kwargs
) -> None:
    query = update(Survey)\
        .where(Survey.id == survey_id)\
        .values(**kwargs)
    
    await session.execute(query)
    await session.commit()

async def update_today_survey(
    session: AsyncSession,
    *,
    user_id: int,
    **kwargs
) -> None:
    query = update(Survey)\
        .where(
            and_(
                Survey.user_id == user_id,
                Survey.created_at > (func.now() - timedelta(hours=12)),
                cast(Survey.created_at, Date) == datetime.now().date()
            )
        )\
        .values(**kwargs)
    
    await session.execute(query)
    await session.commit()

async def update_today_survey_answers(
    session: AsyncSession,
    *,
    user_id: int,
    **kwargs
) -> int:
    query = update(SurveyAnswers)\
        .where(
            and_(
                SurveyAnswers.survey_id == Survey.id,
                Survey.user_id == user_id,
                Survey.created_at > (func.now() - timedelta(hours=12)),
                cast(Survey.created_at, Date) == datetime.now().date(),
                Survey.status == SurveyStatus.PENDING
            )
        )\
        .values(**kwargs)
    
    result = await session.execute(query)
    await session.commit()

    return result.rowcount