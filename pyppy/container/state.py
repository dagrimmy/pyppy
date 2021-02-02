"""
Usage is the same as for :mod:`~pyppy.container.config`.

The only difference usage-wise is a semantic one. Config should be used for a
static configuration that does not change at runtime. In contrast, the functions
for managing the global state should be used for managing non-static
"""

from types import SimpleNamespace
from pyppy.container.container import ContainerType, _initialize, _get, _destroy


def initialize_state(obj_: object = SimpleNamespace()):
    """
    Usage is the same as for :func:`~pyppy.container.config.initialize_config`.
    """
    _initialize(obj_, ContainerType.STATE)


def state():
    """
    Usage is the same as for :func:`~pyppy.container.config.config`.

    TODO: Say here that it is encouraged to change the state during run time
    and show an example of this.
    """
    return _get(ContainerType.STATE)


def destroy_state():
    """
    Usage is the same as for :func:`~pyppy.container.config.destroy_config`.
    """
    _destroy(ContainerType.STATE)
