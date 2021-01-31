from types import SimpleNamespace

from pyppy.container.container import ContainerType, _initialize, _get, _destroy


def initialize_state(obj_: object = SimpleNamespace()):
    _initialize(obj_, ContainerType.STATE)


def state():
    return _get(ContainerType.STATE)


def destroy_state():
    _destroy(ContainerType.STATE)