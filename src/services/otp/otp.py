from redis import Redis
from redis.asyncio import from_url
import random
from db import Service
from config import REDIS_URL

client = from_url(REDIS_URL, decode_responses=True)

def get_otp_manager():
    return OTPManager(client)

class OTPManager:
    def __init__(self, client: Redis, otp_exp: int=300):
        self.redis = client
        self.otp_exp = otp_exp


    async def save_otp(self, email: str, service: Service):
        key = f'otp:{email}:{service.value}'
        code = str(random.randint(1000, 9999))
        await self.redis.setex(key, self.otp_exp, code)
        return code
    

    async def verify_otp(self, email: str, code: int, service: Service, is_delete: bool=True):
        key = f'otp:{email}:{service.value}'
        stored_code = await self.redis.get(key)
        if stored_code and str(code) == stored_code:
            if is_delete:
                await self.redis.delete(key)
            return True
        return False