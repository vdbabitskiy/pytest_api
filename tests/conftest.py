import os

import pytest
from dotenv import load_dotenv

from api.api_client import ApiClient

load_dotenv()
API_KEY = os.environ.get('API_KEY')


@pytest.fixture()
def api_client():
    client = ApiClient()
    client.create()
    yield client
    client.close()


