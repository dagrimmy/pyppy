"""

"""
from typing import Type

from pyppy import config
from pyppy.attr_filling.attr import Attr


class ConfigAttr(Attr):
    _container = config


def use_config(*used_config_attributes: str):

    def decorator(decorated_class: Type):
        for attr in used_config_attributes:
            setattr(
                decorated_class,
                attr,
                ConfigAttr(attr)
            )
        return decorated_class

    return decorator
