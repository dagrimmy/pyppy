"""
TODO
"""
from typing import Type

from pyppy.container.config import config
from pyppy.attr_filling.attr import Attr


class ConfigAttr(Attr):  # pylint: disable=R0903
    """
    TODO
    """
    _container = config


def use_config(*used_config_attributes: str):
    """
    TODO
    """

    def decorator(decorated_class: Type):
        for attr in used_config_attributes:
            setattr(
                decorated_class,
                attr,
                ConfigAttr(attr)
            )
        return decorated_class

    return decorator
