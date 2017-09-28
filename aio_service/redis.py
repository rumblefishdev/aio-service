from typing import Dict, Any

import urllib.parse as urlparse
import logging

import aioredis

from .app import App
from .config import get_config


logger = logging.getLogger(__name__)
REDIS_POOL_KEY = 'redis_pool'


def parse_redis_url(url: str) -> Dict[str, Any]:
    config = {}

    parsed_url = urlparse.urlparse(url)

    path = parsed_url.path[1:]
    path = path.split('?', 2)[0]
    host = parsed_url.hostname or 'localhost'
    port = int(parsed_url.port or 6379)
    db = int(path) or 0

    config.update({
        'db': db,
        'password': parsed_url.password or None,
        'address': (host, port)
    })

    return config


def get_redis_pool(app: App) -> aioredis.RedisPool:
    return app.ctx.get(REDIS_POOL_KEY)


async def destroy_redis_pool(app: App) -> None:
    pool = get_redis_pool(app)
    if pool:
        pool.close()
        await pool.wait_closed()
        del app.ctx[REDIS_POOL_KEY]
        logger.info('redis poll closed')


async def create_redis_pool(app: App) -> None:
    config = get_config(app)
    logger.info(config.redis_url)
    app.ctx[REDIS_POOL_KEY] = await aioredis.create_pool(
        loop=app.loop,
        maxsize=1000,
        encoding='utf8',
        **parse_redis_url(config.redis_url)
    )
    logger.info(f'redis poll created')
