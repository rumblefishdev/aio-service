from unittest.mock import Mock

import pytest
from aio_service.app import App
from aio_service.communication import Result
from aio_service.routing import create_router, resolve_routing_key
from asynctest import CoroutineMock


class TestResolveRoutingKey:
    @pytest.fixture
    def result_message_without_type(self):
        return Result(
            topic='test_topic', message={'payload': {}}
        )

    @pytest.fixture
    def expected_key_for_message_without_type(self):
        return 'test_topic:all'

    def test_correctly_resolves_for_message_without_type(
            self, result_message_without_type,
            expected_key_for_message_without_type):
        key = resolve_routing_key(result_message_without_type)

        assert key == expected_key_for_message_without_type

    @pytest.fixture
    def result_message_with_type(self):
        return Result(
            topic='test_topic', message={'payload': {}, 'type': 'add'}
        )

    @pytest.fixture
    def expected_key_for_message_with_type(self):
        return 'test_topic:add'

    def test_correctly_resolves_for_message_with_type(
            self, result_message_with_type,
            expected_key_for_message_with_type):
        key = resolve_routing_key(result_message_with_type)

        assert key == expected_key_for_message_with_type


class TestRouter:

    @pytest.fixture
    def mocked_app(self):
        return Mock(spec=App)

    @pytest.fixture
    def result(self):
        return Result(topic='test_topic', message={})

    @pytest.fixture
    def routes(self):
        return {
            'correct_key:all': CoroutineMock(return_value='for_correct_key'),
        }

    @pytest.fixture
    def correct_key_resolver(self):
        return Mock(return_value='correct_key:all')

    @pytest.fixture
    def default_route(self):
        return CoroutineMock(return_value='for_default_route')

    @pytest.fixture
    def correct_resolver_router(
            self, routes, correct_key_resolver, default_route):
        return create_router(routes, correct_key_resolver, default_route)

    async def test_routes_to_correct_key_route(
            self, mocked_app, correct_resolver_router,
            result, correct_key_resolver, default_route, routes):
        route_result = await correct_resolver_router(mocked_app, result)

        assert route_result == 'for_correct_key'
        correct_key_resolver.assert_called_once_with(result)
        default_route.assert_not_called()
        routes['correct_key:all'].assert_called_once_with(
            mocked_app, result.message)

    @pytest.fixture
    def missing_key_resolver(self):
        return Mock(return_value='missing_key:all')

    @pytest.fixture
    def missing_resolver_router(
            self, routes, missing_key_resolver, default_route):
        return create_router(routes, missing_key_resolver, default_route)

    async def test_routes_to_default_key_route(
            self, mocked_app, missing_resolver_router, result,
            missing_key_resolver, default_route):
        route_result = await missing_resolver_router(mocked_app, result)

        assert route_result == 'for_default_route'
        missing_key_resolver.assert_called_once_with(result)
        default_route.assert_called_once_with(mocked_app, result.message)
