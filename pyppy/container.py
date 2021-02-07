"""
TODO
"""

from typing import Any


class _Container:

    @classmethod
    def initialize(cls, name: str, obj: Any) -> None:
        setattr(cls, name, obj)

    @classmethod
    def destroy(cls, name) -> None:
        if hasattr(cls, name):
            delattr(cls, name)


def initialize(name: str, obj: Any) -> None:
    _Container.initialize(name, obj)


def get(name: str):
    return getattr(_Container, name)


def destroy(name: str) -> None:
    _Container.destroy(name)


