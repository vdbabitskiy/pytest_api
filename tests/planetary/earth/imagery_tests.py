import os
import pytest
from dotenv import load_dotenv

from core.api.request import Request
from core.utils import load_test_data, process_arguments
from core.asserts import ResponseAssert


load_dotenv()
API_KEY = os.environ.get('API_KEY')


@pytest.fixture()
def request_data():
    return Request(
        method='GET',
        endpoint='/planetary/earth/imagery',
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", load_test_data("test_data/functional_tests.json"))
@process_arguments(API_KEY)
async def test_earth_imagery_functional(api_client, request_data, test_data):
    response = await api_client.execute_request(request_data.update_params(test_data['params']))
    ResponseAssert(response).assert_response(test_data)


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", load_test_data("test_data/validation_tests.json"))
@process_arguments(API_KEY)
async def test_earth_imagery_vailidation(api_client, request_data, test_data):
    response = await api_client.execute_request(request_data.update_params(test_data['params']))
    ResponseAssert(response).assert_response(test_data)


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", load_test_data("test_data/contract_tests.json"))
@process_arguments(API_KEY)
async def test_earth_imagery_contract(api_client, request_data, test_data):
    response = await api_client.execute_request(request_data.update_params(test_data['params']))
    ResponseAssert(response).assert_response(test_data)
