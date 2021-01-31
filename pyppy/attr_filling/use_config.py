"""

"""
from typing import Type

from pyppy import config


class Attr:

    def __init__(self, attr_name):
        self._attr_name = attr_name

    def __get__(self, obj, obj_type=None):
        return getattr(config(), self._attr_name)


def use_config(*used_config_attributes: str):

    def decorator(decorated_class: Type):
        for attr in used_config_attributes:
            setattr(
                decorated_class,
                attr,
                Attr("param_1")
            )
        return decorated_class

    return decorator
