from pydantic import BaseModel, Field
from typing import Annotated, Dict

class UpdateAnswersSchema(BaseModel):
    answers: Annotated[Dict[str, str], Field(min_length=5, max_length=5)]