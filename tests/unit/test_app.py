import pytest

from aio_service.app import App


async def handler(app):
    async for msg in app.subscribe():
        if msg:
            await app.dispatch(msg)


@pytest.fixture
def app(fake_app_creator, loop):
    with fake_app_creator(handler) as app:
        yield app


async def test_echo_app(app, q_subscribe, q_dispatch, loop):
    msg = ['hello']
    await q_subscribe.put(msg)
    assert await q_dispatch.get() == msg


async def test_echo_app_with_exception(app, q_subscribe, q_dispatch):
    msg = ['hello']
    await q_subscribe.put(False)
    await q_subscribe.put(msg)
    # loop wil skip error and wait for another msg
    assert await q_dispatch.get() == msg


async def test_app_hooks(loop):
    called_on_startup = []
    called_on_shutdown = []

    excepted_on_startup = ['s1', 's2']
    excepted_on_shutdown = ['e1', 'e2']

    async def handler(app, *a, **kw):
        app.stop()

    app = App(handler, loop)

    def make_handler(x, called):
        async def proc(app):
            assert app == app
            called.append(x)
        return proc

    for i in excepted_on_startup:
        app.on_startup.append(make_handler(
            i,
            called_on_startup
        ))

    for i in excepted_on_shutdown:
        app.on_shutdown.append(make_handler(
            i,
            called_on_shutdown
        ))

    await app.start()
    assert excepted_on_startup == called_on_startup
    assert excepted_on_shutdown == called_on_shutdown
