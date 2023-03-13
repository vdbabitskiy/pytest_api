import json
import sys
from loguru import logger

from core.api.request import Request
from core.api.response import Response
from core.utils import is_json


def request_logger(func):
    async def wrapped(*args, **kwargs):
        result = await func(*args, **kwargs)
        pretty_print_request(result, args[1])
        return result

    return wrapped


def pretty_print_request(resp: Response, req: Request):
    init_unformatted_logger()
    logger.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '\n\n<<<REQUEST>>>\n',
        resp.request_info.method + ' ' + str(resp.request_info.url),
        '\n'.join('{}: {}'.format(k, v) for k, v in resp.request_info.headers.items()),
        show_request_body(req)))

    logger.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '\n<<<RESPONSE>>>\n',
        'Status code:' + str(resp.status_code),
        '\n'.join('{}: {}'.format(k, v) for k, v in resp.headers.items()),
        json.dumps(json.loads(resp.content), indent=4, ensure_ascii=False) if resp.content is not None and is_json(
            resp.content) else ''))
    init_default_logger()


def show_request_body(req: Request):
    if req.data is not None:
        return json.dumps(req.json, indent=4, ensure_ascii=False) if req.json is not None and is_json(
            req.json) else ''
    elif req.params is not None:
        return "Params:\n"+"\n".join('{}: {}'.format(k, v) for k, v in req.params.items())
    else:
        return ''


def init_default_logger():
    logger.remove()
    logger.level("INFO", color="<white>")
    logger.level("ERROR", color="<red>")

    log_format_stdout = "<green>{time:HH:mm:ss}</green>|" \
                        "<b><level>{level:<8}</level></b>|" \
                        "<blue>{function}</blue> |" \
                        "<blue>{line}</blue>: {message}"

    logger.add(sys.stdout, colorize=True, format=log_format_stdout)


def init_unformatted_logger():
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="{message}")

