from typing import Type

from pyppy.state import state


class Attr:

    def __init__(self, attr_name):
        self._attr_name = attr_name

    def __get__(self, obj, obj_type=None):
        return getattr(state(), self._attr_name)


def use_state(*used_state_attributes: str):

    def decorator(decorated_class: Type):
        for attr in used_state_attributes:
            setattr(
                decorated_class,
                attr,
                Attr("param_1")
            )
        return decorated_class

    return decorator
