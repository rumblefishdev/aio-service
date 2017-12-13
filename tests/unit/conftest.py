import asyncio
import pytest
from contextlib import contextmanager

from aio_service.app import App


@pytest.fixture
def q_dispatch(loop):
    return asyncio.Queue(loop=loop)


@pytest.fixture
def q_subscribe(loop):
    return asyncio.Queue(loop=loop)


@pytest.fixture
def dispatch(q_dispatch):
    async def d(msg):
        await q_dispatch.put(msg)
    return d


@pytest.fixture
def subscribe(q_subscribe):
    async def s():
        yield await q_subscribe.get()
    return s


@pytest.fixture
def fake_app_creator(loop, dispatch, subscribe):
    @contextmanager
    def app_creator_inner(handler):
        app = App(handler, loop)
        app.ctx['dispatch'] = dispatch
        app.ctx['subscribe'] = subscribe
        loop.create_task(app.start())
        yield app
        app.stop()
    return app_creator_inner
