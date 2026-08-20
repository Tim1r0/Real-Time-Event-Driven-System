import asyncio
import json

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from .manager import manager
from services.core import settings, redis_helper, broker
from services.worker.src import calculate_heavy_data


async def redis_listener():
    pubsub = redis_helper.client.pubsub()
    await pubsub.subscribe('notifications')
    async for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])

            await manager.send_personal_message(
                user_id=str(data['user_id']),
                message=data['text']
            )
@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()
    listener_task = asyncio.create_task(redis_listener())
    yield
    listener_task.cancel()
    await redis_helper.dispose()
    await broker.shutdown()

app = FastAPI(
    lifespan=lifespan,
)

@app.post('/process/{seconds}/{user_id}')
async def process_task(
        seconds: int,
        user_id: str,
):
    task = await calculate_heavy_data.kiq(seconds, user_id)
    return {'task_id': task.task_id}



@app.websocket('/ws/{user_id}')
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):
    await manager.connect(
        user_id=user_id,
        ws=websocket,
    )
    try:
        while True:

            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(user_id)


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
    )