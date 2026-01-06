from fastapi import Request, HTTPException, WebSocket, Query, status
from services import JWTSecurity

jwt = JWTSecurity()

async def secure_access(request: Request):
    try:
        token_header = request.headers.get("Authorization")
        if not token_header:
            raise HTTPException(401, detail="Unauthorized") 
        token = token_header.split(" ")[1]
        data = jwt.verify_access_token(token)
        if not data:
            raise HTTPException(401, detail="Unauthorized")
        return data.get("user_id")
    except IndexError:
        raise HTTPException(401, detail="Unauthorized")
    
async def ws_secure_access(ws: WebSocket, access_token: str = Query(None)):
    data = jwt.verify_access_token(access_token)
    if not data:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
    return data.get("user_id")