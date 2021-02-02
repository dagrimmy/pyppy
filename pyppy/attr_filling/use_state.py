"""
TODO
"""
from typing import Type

from pyppy.container.state import state
from pyppy.attr_filling.attr import Attr


class StateAttr(Attr):  # pylint: disable=R0903
    """
    TODO
    """

    _container = state


def use_state(*used_state_attributes: str):
    """
    TODO
    """

    def decorator(decorated_class: Type):
        for attr in used_state_attributes:
            setattr(
                decorated_class,
                attr,
                StateAttr(attr)
            )
        return decorated_class

    return decorator
