import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from services.core import settings, redis_helper, broker
from services.worker.src import calculate_heavy_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()
    yield
    await redis_helper.dispose()
    await broker.shutdown()

app = FastAPI(
    lifespan=lifespan,
)

@app.post('/process/{seconds}')
async def porcess_task(
        seconds: int,
):
    task = await calculate_heavy_data.kiq(seconds)
    return {'task_id': task.task_id}


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
    )