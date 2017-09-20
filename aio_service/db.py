from .app import App
from .config import get_config

import peewee
import peewee_async
import peewee_asyncext

from playhouse.db_url import parse

database_proxy = peewee.Proxy()


def get_objects(app: App) -> peewee_async.Manager:
    return app.ctx['objects']


def get_database(app: App) -> peewee_asyncext.PooledPostgresqlExtDatabase:
    return app.ctx['database']


def create_database(app: App) -> None:
    config = get_config(app)
    database = peewee_asyncext.PooledPostgresqlExtDatabase(
        **parse(config.postgres_url)
    )
    database_proxy.initialize(database)
    app.ctx['database'] = database_proxy
    objects = peewee_async.Manager(database_proxy)
    database.set_allow_sync(False)
    app.ctx['objects'] = objects
