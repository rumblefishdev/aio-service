import pytest
import uuid


@pytest.fixture
def async_val(request):
    def _async_val(val):
        async def __async_val(*args, **kwargs):
            return val
        return __async_val
    return _async_val


@pytest.fixture
def create_random_name():
    def creator(prefix=None):
        id_ = uuid.uuid4().hex
        if prefix is None:
            prefix = __name__
        return f'{prefix}:{id_}'
    return creator
