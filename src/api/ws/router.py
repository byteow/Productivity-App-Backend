from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from services import ws_secure_access
import redis.asyncio as redis
from config import REDIS_URL
import asyncio

router = APIRouter(prefix="/ws")
redis_pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)

async def get_redis_pubsub():
    client = redis.Redis(connection_pool=redis_pool)
    pubsub = client.pubsub()
    try:
        yield pubsub
    finally:
        await pubsub.close()
        await client.close()

@router.websocket("/events")
async def events(
    ws: WebSocket,
    user_id: int=Depends(ws_secure_access),
    pubsub:redis.client.PubSub = Depends(get_redis_pubsub)
):
    if not user_id:
        return
    
    await ws.accept()
    channel = f"user_event_{user_id}"
    await pubsub.subscribe(channel)

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            
            if message:
                data = message['data']
                await ws.send_text(data)    

            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        await pubsub.unsubscribe(channel)
        print(f"Client {user_id} disconnected")