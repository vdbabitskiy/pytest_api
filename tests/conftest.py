import pytest

from api.api_client import ApiClient


@pytest.fixture()
def api_client():
    client = ApiClient()
    client.create()
    yield client
    client.close()


