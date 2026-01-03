from fastapi import APIRouter, Depends
from .service import Service
from .schemas import SendCodeSchema, CheckCodeSchema

router = APIRouter(prefix="/codes")
service = Service()

@router.post("/send")
async def send_code(schema: SendCodeSchema):
    return await service.send(schema)

@router.get("/check_code")
async def check_code(schema: CheckCodeSchema=Depends()):
    return await service.check_code(schema)