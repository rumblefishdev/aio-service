from contextlib import contextmanager
import pytest
import logging

from aio_service.app import App
from aio_service.redis import (
    create_redis_pool,
    destroy_redis_pool
)

from aio_service.communication import (
    add_queues
)

from aio_service.config import (
    Config,
    set_config
)


def create_app(handler, loop, logger):
    app = App(handler, loop)
    set_config(app, Config('TEST'))
    app.on_startup.append(create_redis_pool)
    app.on_startup.append(add_queues)
    app.on_shutdown.append(destroy_redis_pool)
    return app


@pytest.fixture
def app_creator(loop):

    @contextmanager
    def app_creator_inner(handler):
        logger = logging.getLogger(__name__)
        app = create_app(handler, loop, logger)
        yield app
        app.stop()

    return app_creator_inner
