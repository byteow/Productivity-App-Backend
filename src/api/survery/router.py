from fastapi import APIRouter, Depends
from .service import Service
from db import get_session
from .schemas import UpdateAnswersSchema, SurveyGenerateSchema
from services import secure_access
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/survey")
service = Service()

@router.post("/generate")
async def generate_survey(
    schema: SurveyGenerateSchema=Depends(),
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.generate_survey(schema, user_id, db)


@router.put("/answers")
async def update_answers(
    schema: UpdateAnswersSchema,
    user_id: int=Depends(secure_access),
    db: AsyncSession=Depends(get_session)
):
    return await service.update_answers(schema, user_id, db)