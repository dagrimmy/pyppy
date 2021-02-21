"""
TODO
"""
from types import SimpleNamespace
from typing import Any


class _Container:
    pass


class _Initialize:
    def __call__(self, container_name: str, initial_content: Any = SimpleNamespace()):
        setattr(_Container, container_name, initial_content)


class _Initializer:

    def __getattr__(self, container_name: str):
        return lambda initial_content = SimpleNamespace(): setattr(_Container, container_name, initial_content)


initialize = _Initialize()
"""initialize"""

initializer = _Initializer()
"""initializer"""
def fun():
    pass

class Tmp:

    def __call__(self, name, content):
        print(name, content)

    def __getattr__(self, item):
        return fun

a = Tmp()
"""asdfasdf"""


class _Getter:

    def __getattr__(self, container_name):
        return getattr(_Container, container_name)

    def __getitem__(self, container_name):
        return getattr(_Container, container_name)


get = _Getter()
get.__doc__ = """get"""


class _Destroy:

    def __call__(self, container_name):
        delattr(_Container, container_name)


class _Destroyer:
    def __getattr__(self, container_name):
        return lambda: delattr(_Container, container_name)


destroy = _Destroyer()
destroy.__doc__ = """destroy"""


def destroy_all():
    for attr in list(vars(_Container)):
        if not attr.startswith("__"):
            delattr(_Container, attr)
