import aiohttp
from aiohttp import ClientTimeout
from loguru import logger

from config import TIME_OUT_TOTALL, TIME_OUT_CONNECTION
from api.request import Request
from api.response import Response


class ApiClient:

    def __init__(self):
        self.session = None

    def create(self):
        timeout = ClientTimeout(total=TIME_OUT_TOTALL, connect=TIME_OUT_CONNECTION)
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=timeout, trust_env=True)

    async def close(self):
        if self.session is not None:
            await self.session.close()
            if not self.session.closed:
                logger.error('Failed to close session')

    async def execute_request(self, request: Request):
        async with await self.session.request(
                method=request.method,
                url=request.url(),
                headers=request.headers,
                params=request.params,
                data=request.data,
                verify_ssl=False) as resp:
            return Response(resp, await resp.read())
