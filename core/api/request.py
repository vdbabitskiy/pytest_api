from typing import Optional, Any, Dict
from core import utils
from config import API_URL


class Request:

    def __init__(
            self,
            endpoint: str,
            method: str,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
    ):
        self.endpoint = endpoint
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.json = json

    def url(self):
        return utils.join(API_URL, self.endpoint)

    def update_params(self, params: Dict[str, Any]):
        if self.params:
            self.params.update(params)
        else:
            self.params = params
        return self
