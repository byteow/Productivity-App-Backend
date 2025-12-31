from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import SendCodeSchema, CheckCodeSchema
from fastapi import HTTPException
from worker import send_code
from db import (
    get_recent_send_codes,
    create_sms_code,
    get_last_send_code
)
import random

class Service:
    def __init__(self):
        ...


    def _generate_code(self):
        return random.randint(1000, 9999)
    

    async def send(self, schema: SendCodeSchema, db: AsyncSession):
        last_codes = await get_recent_send_codes(
            db, 
            email=schema.email, 
            service=schema.service
        )
        if last_codes and len(last_codes) >= 3:
            raise HTTPException(status_code=400, detail="Too many codes has been sent")

        code = self._generate_code()
        await create_sms_code(
            db, 
            email=schema.email, 
            service=schema.service,
            code=code
        )
        send_code.delay(schema.email, code)

        return { "message": "Code sent" }
    

    async def check_code(self, schema: CheckCodeSchema, db: AsyncSession):
        last_code = await get_last_send_code(
            db,
            email=schema.email,
            service=schema.service
        )
        if not last_code or last_code.code != schema.code:
            raise HTTPException(400, detail="Invalid code")
        
        return { "detail": "Correct code" }