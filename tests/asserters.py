from PIL import Image
from io import BytesIO

import jsonpath_ng
from assertpy import assert_that
from api.response import Response


class ResponseAssert:

    def __init__(self, response: Response):
        self.response = response

    def assert_status_code(self, expected_status_code):
        assert_that(self.response.status_code).is_equal_to(expected_status_code)

    def assert_headers(self, expected_headers):
        for header_name, header_value in expected_headers.items():
            assert_that(self.response.headers.get(header_name)).is_equal_to(header_value)

    def assert_jsonpath(self, jsonpath_expression, expected_value):
        json_data = self.response.json()
        jsonpath_expr = jsonpath_ng.parse(jsonpath_expression)
        matches = [match.value for match in jsonpath_expr.find(json_data)]
        assert_that(matches).contains(expected_value)

    def assert_error_msg(self, expected_error):
        assert_that(self.response.error_msg).is_equal_to(expected_error)

    def assert_error_code(self, expected_error):
        assert_that(self.response.error_code).is_equal_to(expected_error)

    def assert_content_type(self, expected_content_type):
        assert_that(self.response.headers.get('content-type')).contains(expected_content_type)

    def assert_image(self):
        content_type = self.response.headers.get('content-type')
        assert_that(content_type).contains('image')
        image_data = BytesIO(self.response.content)
        with Image.open(image_data) as img:
            assert_that(img.format).is_in('JPEG', 'PNG', 'GIF', 'BMP')

    def assert_response(self, test_data: dict):
        for assert_func, assert_args in test_data.get("asserts", {}).items():
            func = getattr(self, assert_func)
            func(*assert_args)

