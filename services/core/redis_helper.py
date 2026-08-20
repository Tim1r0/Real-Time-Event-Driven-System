import redis.asyncio as redis
from typing import AsyncGenerator
from .config import settings

class RedisHelper:
    def __init__(
        self,
        url: str,
        decode_responses: bool = True,
    ):
        self.client: redis.Redis = redis.from_url(
            url,
            decode_responses=decode_responses
        )
    async def dispose(self) -> None:
        await self.client.close()

    async def get_redis(self) -> AsyncGenerator[redis.Redis, None]:
        yield self.client

redis_helper = RedisHelper(
    url=f"redis://{settings.redis.host}:{settings.redis.port}",
)