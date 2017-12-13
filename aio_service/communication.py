import asyncio
import json
import logging
from collections import namedtuple
from typing import Callable

from .app import App
from .redis import get_redis_pool

logger = logging.getLogger(__name__)


Result = namedtuple('Result', ['topic', 'message'],)


def create_dispatcher(app: App) -> Callable:
    pool = get_redis_pool(app)
    loop = app.loop

    async def dispatcher(msg, topics=[], *a, **kw):
        packed = json.dumps(msg)
        async with pool.get() as conn:
            return await asyncio.gather(
                *[conn.rpush(
                    topic, packed, *a, **kw
                ) for topic in topics],
                loop=loop
            )

    return dispatcher


def create_subscriber(app: App) -> Callable:
    pool = get_redis_pool(app)

    async def subscriber(topics=[], *a, **kw):
        for topic in topics:
            async with pool.get() as conn:
                result = await conn.lpop(
                    topic, *a, **kw
                )
            if result:
                yield Result(topic, json.loads(result))

    return subscriber


async def add_queues(app: App) -> None:
    app.ctx['subscribe'] = create_subscriber(app)
    app.ctx['dispatch'] = create_dispatcher(app)
