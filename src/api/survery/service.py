from sqlalchemy.ext.asyncio import AsyncSession
from db import (
    SurveyStatus,
    create_survey,
    get_today_survey,
    update_today_survey_answers,
    update_today_survey
)
from fastapi import HTTPException
from .schemas import UpdateAnswersSchema
from worker import generate_survey

class Service:
    def __init__(self):
        ...


    async def generate_survey(self, user_id: int, db: AsyncSession):
        today_survey = await get_today_survey(db, user_id=user_id)
        if today_survey:
            return {
                "survey_id": today_survey.id,
                "status": today_survey.status,
                "schema": today_survey.schema
            }
    
        survey = await create_survey(
            db,
            user_id=user_id,
            status=SurveyStatus.GENERATING,
            schema=None
        )

        generate_survey.delay(user_id, survey.id)

        return {
            "survey_id": survey.id,
            "status": survey.status,
            "schema": survey.schema
        }
    

    async def update_answers(
        self, 
        schema: UpdateAnswersSchema,
        user_id: int,
        db: AsyncSession
    ):
        rowcount = await update_today_survey_answers(
            db,
            user_id=user_id,
            schema=schema.answers
        )
        if rowcount == 0:
            raise HTTPException(400, detail="Today's survey not exists or in generating state")
        
        await update_today_survey(
            db,
            user_id=user_id,
            status=SurveyStatus.COMPLTETED
        )

        return { "message": "Survey answers successfully updated" }