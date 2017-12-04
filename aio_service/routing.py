import logging
from typing import Any, Awaitable, Callable, Dict

from .app import App
from .communication import Result

logger = logging.getLogger(__name__)


IKeyResolver = Callable[..., str]
IRoute = Callable[[Any, Any], Awaitable]


async def default_route(app: App, result: Result) -> None:
    raise ValueError("Route not find for given result")


def resolve_routing_key(result: Result) -> str:
    topic = result.topic
    event_type = result.message.get('type', 'all')
    return f'{topic}:{event_type}'


def create_router(
        routes: Dict[str, IRoute],
        key_resolver: IKeyResolver = resolve_routing_key,
        default: IRoute = default_route) -> Callable:
    async def router(app: App, result: Result):
        k = key_resolver(result)
        logger.info(f'route to: "{k}"')
        route = routes.get(k, default)
        return await route(app, result.message)
    return router
