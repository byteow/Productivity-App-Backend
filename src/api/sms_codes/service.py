from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import SendCodeSchema
from fastapi import HTTPException
from random import randint
from db import (
    get_recent_send_codes,
    create_sms_code
)

class Service:
    def __init__(self):
        ...


    def _generate_code(self):
        return randint(1000, 9999)
    

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

        # send code on email login here

        return { "message": "Code sent" }