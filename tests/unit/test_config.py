import pytest
from mock import call
import logging

from aio_service.config import (
    get_env,
    Config
)


@pytest.mark.parametrize('args, expected', [
    (({'db_host': 'db'}, 'db_host'),
     'db'),
    (({'db_host': 'db'}, 'DB_HOST'),
     ''),
    (({'db_host': 'db'}, 'DB_HOST', 'default_db_host'),
     'default_db_host'),
    (({'XYZ_db_host': 'db'}, 'db_host', '', 'XYZ'),
     'db'),
    (({'_db_host': 'db'}, 'db_host', '', ''),
     'db'),
    (({'db_host': 'db'}, 'db_host', 'default_db_host', 'XYZ'),
     'default_db_host')
])
def test_get_env(args, expected):
    assert get_env(*args) == expected


def test_get_env_calls_in_Config_prefix(mocker):
    prefix = 'SOME_PREFIX'
    env = {'FOO': 'BAR'}
    get_env = mocker.patch(
        'aio_service.config.get_env',
        return_value='value',
        autospec=True
    )
    mocker.patch(
        'aio_service.config.environ',
        env
    )
    Config(prefix)
    assert get_env.call_args_list == [
        call(env, 'REDIS_URL', 'redis://localhost/0', prefix),
        call(env, 'POSTGRES_URL', '', prefix),
        call(env, 'SENTRY_DNS', '', prefix),
        call(env, 'LOGGING_LEVEL', 'ERROR', prefix),
    ]


@pytest.mark.parametrize('value, expected', [
    ('INFO', logging.INFO),
    ('FOO', logging.ERROR),
    ('DEBUG', logging.DEBUG)
])
def test_config_leging_level(value, expected, mocker):
    env = {'LOGGING_LEVEL': value}
    mocker.patch(
        'aio_service.config.environ',
        env
    )
    config = Config()
    assert config.logging_level == expected
