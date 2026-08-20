import asyncio

from services.core import broker

@broker.task
async def calculate_heavy_data(value: int):
    await asyncio.sleep(value)