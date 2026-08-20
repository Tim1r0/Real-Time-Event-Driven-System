import asyncio
import json
import logging
from services.core import broker, redis_helper

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
@broker.task
async def calculate_heavy_data(value: int, user_id: str):
    log.info(f"Calculating heavy data: {value}")
    await asyncio.sleep(value)
    log.info(f'task successfully')
    notification = {
        'user_id': user_id,
        'text': f'Your task for {value} has been completed!'
    }
    await redis_helper.client.publish(
        "notifications",
        json.dumps(notification)
    )
