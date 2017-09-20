from typing import Callable
import asyncio
import json
import logging
from itertools import cycle
from collections import namedtuple

from .app import App
from .redis import (
    get_redis_pool
)


logger = logging.getLogger(__name__)


Result = namedtuple('Result', ['topic', 'message'],)


async def create_dispatcher(app: App) -> Callable:
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


async def create_subscriber(app: App) -> Callable:
    pool = get_redis_pool(app)

    async def subscriber(topics=[], *a, **kw):
        for topic in cycle(topics):
            async with pool.get() as conn:
                result = await conn.blpop(
                    topic, *a, timeout=1, **kw
                )
            if result:
                break

        topic, msg = result
        return (Result(
            topic,
            json.loads(msg)
        ), )

    return subscriber


async def add_queues(app: App) -> None:
    app.ctx['subscribe'] = await create_subscriber(app)
    app.ctx['dispatch'] = await create_dispatcher(app)
