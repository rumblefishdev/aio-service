import inspect
from aio_service.communication import Result


async def handler(*a, **k):
    raise Exception('This should never happen!!')


async def test_dispatch_subscribe(app_creator, create_random_name):
    topics = create_random_name('topic_1'), create_random_name('topic_2')
    msg = ['test', ]

    with app_creator(handler) as app:
        await app._process_hook(app.on_startup)
        await app.dispatch(msg, topics)
        expected = [Result(topics[0], msg), Result(topics[1], msg)]
        await assert_subscribe(app, topics, expected)


async def assert_subscribe(app, topics, expected):
    generator = app.subscribe(topics)
    assert inspect.isasyncgen(generator)
    result = [x async for x in generator]
    assert result == expected
