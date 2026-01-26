from pydantic import BaseModel, Field
from typing import Annotated, Dict, Optional
from api.profile.enums import Language

class UpdateAnswersSchema(BaseModel):
    answers: Annotated[Dict[str, str], Field(min_length=5, max_length=5)]

class SurveyGenerateSchema(BaseModel):
    lang: Optional[Language] = Language.EN