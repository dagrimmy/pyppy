"""
TODO
"""
from types import SimpleNamespace
from typing import Any


class _Container:

    def __init__(self):
        self._content = SimpleNamespace()

    def initialize(self, obj: Any or None = None):
        if obj is None:
            return
        self._content = obj

    def __call__(self):
        return self._content


class Container:

    def __init__(self):
        self._registered_containers = []

    def _get_or_create_container(self, container_name):
        if container_name not in self.__dict__:
            self.__dict__[container_name] = _Container()
            self._registered_containers.append(container_name)

        return self.__dict__[container_name]

    def __getattr__(self, container_name: str):
        return self._get_or_create_container(container_name)

    def __delattr__(self, container_name):
        del self.__dict__[container_name]
        self._registered_containers.remove(container_name)

    def destroy_all(self):
        for container_name in self._registered_containers:
            del self.__dict__[container_name]
        self._registered_containers = []

    def __getitem__(self, container_name):
        return self._get_or_create_container(container_name)()


container = Container()
container.__doc__ = """fill is shorthand for Fill()"""
