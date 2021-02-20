"""
TODO
"""
from types import SimpleNamespace
from typing import Any


class _Container:

    pass


class _Initializer:

    def __call__(self, container_name: str, initial_content: Any = SimpleNamespace()):
        setattr(_Container, container_name, initial_content)

    def __getattr__(self, container_name):
        return lambda initial_content = SimpleNamespace(): setattr(_Container, container_name, initial_content)


initialize = _Initializer()
initialize.__doc__ = """initialize"""


class _Getter:

    def __getattr__(self, container_name):
        return getattr(_Container, container_name)

    def __getitem__(self, container_name):
        return getattr(_Container, container_name)


get = _Getter()
get.__doc__ = """get"""


class _Destroyer:

    def __call__(self, container_name):
        delattr(_Container, container_name)

    def __getattr__(self, container_name):
        return lambda: delattr(_Container, container_name)


destroy = _Destroyer()
destroy.__doc__ = """destroy"""


def destroy_all():
    for attr in list(vars(_Container)):
        if not attr.startswith("__"):
            delattr(_Container, attr)
