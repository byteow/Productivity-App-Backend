from pydantic import BaseModel
from db import Service

class SendCodeSchema(BaseModel):
    email: str
    service: Service