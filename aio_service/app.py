import asyncio
import logging

logger = logging.getLogger(__name__)


class App:
    _started = False
    _pending = None

    def __init__(self, handler, loop):
        "docstring"
        self.loop = loop
        self.on_startup = []
        self.on_shutdown = []
        self._handler = handler
        self.ctx = {}

    @property
    def started(self):
        return self._started

    @property
    def subscribe(self):
        return self.ctx['subscribe']

    @property
    def dispatch(self):
        return self.ctx['dispatch']

    async def _process_hook(self, hook):
        for f in hook:
            await f(self)

    def handler(self):
        return self._handler(self)

    async def start(self, loop_sleep=1):
        await self._process_hook(self.on_startup)
        self._started = True
        try:
            while self.started:
                try:
                    self._pending = asyncio.ensure_future(self.handler())
                    await self._pending
                except Exception as e:
                    logger.exception('handler fail')
                await asyncio.sleep(loop_sleep)
        finally:
            await self._process_hook(self.on_shutdown)

    def stop(self):
        self._started = False
        if self._pending:
            self._pending.cancel()
