from fastapi import APIRouter, Depends
from .service import Service
from .schemas import SendCodeSchema, CheckCodeSchema
from fastapi_limiter.depends import RateLimiter
from services import get_client_ip_address

router = APIRouter(prefix="/codes")
service = Service()

@router.post("/send", dependencies=[
    Depends(RateLimiter(times=5, hours=1, identifier=get_client_ip_address))
])
async def send_code(schema: SendCodeSchema):
    return await service.send(schema)

@router.get("/check_code")
async def check_code(schema: CheckCodeSchema=Depends()):
    return await service.check_code(schema)