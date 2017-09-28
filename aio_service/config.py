from typing import Union, Dict
from os import environ
import logging

from .app import App

logger = logging.getLogger(__name__)


def get_env(env: Dict[str, str],
            name: str,
            default: str='',
            prefix: Union[None, str]=None) -> str:
    prefixed_name = name
    if prefix is not None:
        prefixed_name = f'{prefix}_{name}'
    return env.get(prefixed_name, default)


class Config:
    def __init__(self, prefix=None):
        self.prefix = prefix
        self.redis_url = self.get_env('REDIS_URL', 'redis://localhost/0')
        self.postgres_url = self.get_env('POSTGRES_URL', '')
        self.sentry_dsn = self.get_env('SENTRY_DSN', '')
        self.logging_level = getattr(
            logging,
            self.get_env('LOGGING_LEVEL', 'ERROR'),
            logging.ERROR
        )

    def get_env(self, name, default):
        return get_env(
            environ,
            name,
            default,
            self.prefix
        )


def get_config(app: App) -> Config:
    return app.ctx['config']


def set_config(app: App, config: Config) -> None:
    app.ctx['config'] = config
