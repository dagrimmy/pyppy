from types import SimpleNamespace

from pyppy.container.container import ContainerType, _initialize, _get, _destroy


def initialize_config(obj_: object = SimpleNamespace()):
    _initialize(obj_, ContainerType.CONFIG)


def initialize_state(obj_: object = SimpleNamespace()):
    _initialize(obj_, ContainerType.STATE)


def config():
    return _get(ContainerType.CONFIG)


def state():
    return _get(ContainerType.STATE)


def destroy_config():
    _destroy(ContainerType.CONFIG)


def destroy_state():
    _destroy(ContainerType.STATE)