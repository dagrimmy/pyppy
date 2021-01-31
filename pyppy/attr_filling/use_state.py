from typing import Type

from pyppy import state
from pyppy.attr_filling.attr import Attr


class StateAttr(Attr):

    _container = state


def use_state(*used_state_attributes: str):

    def decorator(decorated_class: Type):
        for attr in used_state_attributes:
            setattr(
                decorated_class,
                attr,
                StateAttr(attr)
            )
        return decorated_class

    return decorator
