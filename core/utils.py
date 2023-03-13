import asyncio
import json
from functools import wraps
from os.path import dirname, abspath
from pathlib import Path
from typing import Tuple, Type, Union, Optional, Callable, List

from aiohttp import ClientConnectorError, ClientHttpProxyError
from loguru import logger


def process_arguments(new_value, pattern='{replace}'):
    """
    Replaces all occurrences according pattern of a certain value with a new value
    in a JSON-like data structure (dicts, lists).
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, dict):
                    _transform_value(arg, new_value, pattern)
                elif isinstance(arg, str):
                    if is_json(arg):
                        _transform_value(json.loads(arg), new_value, pattern)
            if kwargs:
                _transform_value(kwargs, new_value, pattern)
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def load_test_data(file_name):
    """
        Loads test data as json and returns a dictionary
        representing the data.
    """
    try:
        with open(file_name) as f:
            test_data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File '{file_name}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file '{file_name}'.")
    return test_data


def join(base, path):
    """
        Joins a base URL and a path fragment, ensuring that there is only one
        separator character between them.
    """
    if not isinstance(base, str) or not isinstance(path, str):
        raise TypeError("Both 'base' and 'path' must be strings.")
    return _ensure_trailing_separator(base) + _ensure_no_leading_separator(path).replace(' ', '')


def get_root_path():
    """
        Returns the root path of the project, assuming that this function is
        called from a module inside the project.
    """
    return str(Path(dirname(abspath(dirname(__file__)))))


def is_json(myjson):
    """
        Checks if the passed argument is a valid JSON object.
    """
    try:
        if isinstance(myjson, dict):
            json.dumps(myjson)
        else:
            json.loads(myjson)
        return True
    except (TypeError, ValueError):
        return False


def handle_request_error(func):
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
        except (ClientConnectorError, ClientHttpProxyError) as con:
            logger.error('Сlient was unable to create a connection')
            raise con
        except asyncio.exceptions.TimeoutError as terr:
            logger.error(f'Time out error')
            raise terr
        return response
    return wrapper


def async_retry(exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]], max_tries: int, delay: int = 0,
                on_retry: Optional[List[Callable]] = None):
    """
        A decorator that allows for asynchronous retries of a function that raises a specific exception.
    """
    def decorator(function):
        async def wrapper(*args, **kwargs):
            for i in range(max_tries):
                try:
                    return await function(*args, **kwargs)
                except exceptions as ex:
                    if on_retry:
                        for func in on_retry:
                            await func()
                    if i < max_tries - 1:
                        await asyncio.sleep(delay)
                    else:
                        raise ex
        return wrapper
    return decorator


def _transform_value(json_data, new_value, pattern: str):
    """
       Replaces all occurrences according pattern of a certain value with a new value
       in a JSON-like data structure (dicts, lists).
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if value == pattern:
                json_data[key] = new_value
            elif isinstance(value, (dict, list)):
                _transform_value(value,  new_value, pattern)
    elif isinstance(json_data, list):
        for item in json_data:
            _transform_value(item, new_value, pattern)
    return json_data


def _ensure_trailing_separator(url: str) -> str:
    if not url.endswith('/'):
        return url + '/'
    return url


def _ensure_no_leading_separator(url: str) -> str:
    if url.startswith('/'):
        return url[1:]
    return url



