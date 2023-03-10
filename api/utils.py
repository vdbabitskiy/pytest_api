import json
from os.path import dirname, abspath
from pathlib import Path


def transform_value(json_data, new_value):
    pattern = '{replace}'
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if value == pattern:
                json_data[key] = new_value
            elif isinstance(value, (dict, list)):
                transform_value(value,  new_value)
    elif isinstance(json_data, list):
        for item in json_data:
            transform_value(item, new_value)
    return json_data


def load_test_data(file_name):
    with open(file_name) as f:
        test_data = json.load(f)
    return test_data


def join(base, path):
    return ensure_trailing_separator(base) + _ensure_no_leading_separator(path).replace(' ', '')


def ensure_trailing_separator(url: str) -> str:
    if not url.endswith('/'):
        return url + '/'
    return url


def ensure_leading_separator(url: str) -> str:
    if not url.startswith('/'):
        return '/' + url
    return url


def _ensure_no_leading_separator(url: str) -> str:
    if url.startswith('/'):
        return url[1:]
    return url


def get_root_path():
    return str(Path(dirname(abspath(dirname(__file__)))))