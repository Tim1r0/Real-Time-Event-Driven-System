from taskiq_aio_pika.broker import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend
from services.core import settings

redis_backend = RedisAsyncResultBackend(
    redis_url=f'redis://{settings.redis.host}:{settings.redis.port}'
)

broker = AioPikaBroker(
    url=settings.rabbit.url
).with_result_backend(redis_backend)