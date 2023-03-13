import asyncio

import pytest

from core.api.api_client import ApiClient


@pytest.fixture()
def api_client():
    client = ApiClient()
    client.create()
    try:
        yield client
    finally:
        asyncio.get_event_loop().run_until_complete(client.close())




