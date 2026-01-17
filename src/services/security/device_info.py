from fastapi import Request
from user_agents import parse
from config import PRODUCTION

async def get_client_ip_address(request: Request):
    if PRODUCTION:
        return request.headers.get("X-Real-IP")
    return request.client.host

async def device_info(request: Request):
    user_agent = parse(request.headers.get("User-Agent"))

    return {
        "ip": await get_client_ip_address(request),
        "os": f"{user_agent.os.family} {user_agent.os.version}",
        "client_app": f"{user_agent.browser.family} {user_agent.browser.version}",
        "is_mobile_device": user_agent.is_mobile
    }