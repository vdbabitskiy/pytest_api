import json


class Response:
    def __init__(self, raw_response, content):
        self._raw_response = raw_response
        self._content = content

    @property
    def status_code(self):
        return int(self._raw_response.status)

    @property
    def headers(self):
        return self._raw_response.headers

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def json(self):
        return json.loads(self._content)

    @property
    def request_info(self):
        return self._raw_response.request_info

    @property
    def error_msg(self) -> str:
        return str(self.json['msg'])

    @property
    def error_code(self) -> str:
        return str(self.json['error']['code'])
