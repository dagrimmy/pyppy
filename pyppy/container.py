"""
TODO
"""
from types import SimpleNamespace
from typing import Any


DEFAULT_CONTAINER_NAME = "default"


class _Container:
    pass


def initialize(initial_content: Any = SimpleNamespace(), container_name: str = None):
    """docstring"""
    if container_name is None:
        setattr(_Container, DEFAULT_CONTAINER_NAME, initial_content)
    else:
        setattr(_Container, container_name, initial_content)


def get(container_name: str = None):
    if container_name is None:
        return getattr(_Container, DEFAULT_CONTAINER_NAME)
    else:
        return getattr(_Container, container_name)


def destroy(container_name: str = None):
    if container_name is None:
        delattr(_Container, DEFAULT_CONTAINER_NAME)
    else:
        delattr(_Container, container_name)


def destroy_all():
    for attr in list(vars(_Container)):
        if not attr.startswith("__"):
            delattr(_Container, attr)
