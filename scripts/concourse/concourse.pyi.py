from typing import Any, Union


class ConcourseResource(object):
    def __init__(self, config: dict) -> None:
        return

    def mandatory_sources(self, *names: list) -> MandatorySources:
        return MandatorySources({}, [])

    def has_param(self, name: str) -> bool:
        return False

    def has_source(self, name: str) -> bool:
        return False

    def param(self, name: str, default=None) -> Union[str, Any]:
        return ''

    def source(self, name: str, default=None) -> Union[str, Any]:
        return ''


class MandatorySources(object):
    def __init__(self, config: dict, *names: list) -> None:
        return

    def __enter__(self):
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


class MissingSourceException(Exception):
    def __init__(self, name: str) -> None:
        return


def print_error(text: str) -> int:
    return 0
