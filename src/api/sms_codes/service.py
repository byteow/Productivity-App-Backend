from .schemas import SendCodeSchema, CheckCodeSchema
from fastapi import HTTPException
from celery_worker import send_code_task
from services import get_otp_manager

class Service:
    def __init__(self):
        self.otp_manager = get_otp_manager()


    async def send(self, schema: SendCodeSchema):
        code = await self.otp_manager.save_otp(schema.email, schema.service)
        send_code_task.delay(schema.email, code)
        return { "message": "Code sent" }
    

    async def check_code(self, schema: CheckCodeSchema):
        is_valid_code = await self.otp_manager.verify_otp(schema.email, schema.code, schema.service, is_delete=False)
        if not is_valid_code:
            raise HTTPException(status_code=400, detail="Invalid code")
        
        return { "detail": "Correct code" }