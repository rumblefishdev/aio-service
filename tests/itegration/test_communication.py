from aio_service.communication import Result


async def handler(*a, **k):
    raise Exception('This should never happen!!')


async def test_dispatch_subscribe(app_creator, create_random_name):
    topic_1 = create_random_name('topic_1')
    topic_2 = create_random_name('topic_2')
    msg = ['test', ]

    with app_creator(handler) as app:
        await app._process_hook(app.on_startup)
        await app.dispatch(msg, [topic_1, topic_2])
        e = [
            (Result(topic_1, msg), ),
            (Result(topic_2, msg), )
        ]
        assert e == [
            await app.subscribe([topic_1, topic_2]),
            await app.subscribe([topic_1, topic_2])
        ]
