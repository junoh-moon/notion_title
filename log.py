import inspect
import logging
import os
import sys
from operator import attrgetter

log_level = attrgetter(os.environ.get("LOG_LEVEL", "INFO").upper())(logging)
logging.basicConfig(
    stream=sys.stderr,
    level=log_level,
    format=(
        "[%(levelname).1s %(asctime)s.%(msecs)03d+09:00 "
        "%(processName)s:%(filename)s:%(funcName)s:"
        "%(module)s:%(lineno)d] "
        "%(message)s"
    ),
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def init(name: str | None = None) -> logging.Logger:
    """
    logger 생성
    """
    if name is not None:
        _logger_name = name
    else:
        _logger_name = _get_caller_module_name()

    return logging.getLogger(_logger_name)


def _get_caller_module_name() -> str:
    """이 모듈에 접근한 caller module 의 이름을 반환"""
    _stack: list[inspect.FrameInfo] = inspect.stack()
    module_name = "undefined"
    for _frame_info in _stack:
        _module = inspect.getmodule(_frame_info.frame)
        if _module is None:
            module_name = "<stdin>"
        else:
            module_name = _module.__name__

        if module_name != __name__:
            break

    return module_name
