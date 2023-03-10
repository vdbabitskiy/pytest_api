import os
import pytest
from dotenv import load_dotenv

from api.request import Request
from api.utils import transform_value, load_test_data
from tests.asserters import ResponseAssert


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
async def test_earth_imagery_functional(api_client, request_data, test_data):
    transform_value(test_data, API_KEY)
    request_data.params = test_data['params']
    response = await api_client.execute_request(request_data)
    checker = ResponseAssert(response)
    checker.assert_response(test_data)


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", load_test_data("test_data/validation_tests.json"))
async def test_earth_imagery_vailidation(api_client, request_data, test_data):
    transform_value(test_data, API_KEY)
    request_data.params = test_data['params']
    response = await api_client.execute_request(request_data)
    checker = ResponseAssert(response)
    checker.assert_response(test_data)


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", load_test_data("test_data/contract_tests.json"))
async def test_earth_imagery_contract(api_client, request_data, test_data):
    test_data = transform_value(test_data, API_KEY)
    request_data.params = test_data['params']
    response = await api_client.execute_request(request_data)
    checker = ResponseAssert(response)
    checker.assert_response(test_data)
