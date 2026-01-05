from fastapi import Request
from user_agents import parse

async def device_info(request: Request):
    user_agent = parse(request.headers.get("User-Agent"))

    return {
        "ip": request.client.host,
        "os": f"{user_agent.os.family} {user_agent.os.version}",
        "client_app": f"{user_agent.browser.family} {user_agent.browser.version}",
        "is_mobile_device": user_agent.is_mobile
    }