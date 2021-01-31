from enum import Enum
from types import SimpleNamespace
from typing import Any

from pyppy.utils.exception import AlreadyInitializedException


class _Container:

    name = None

    @classmethod
    def _check_name_is_present(cls) -> None:
        if cls.name is None:
            raise ValueError(
                f"Attribute 'name' must be set on subclasses of {_Container.__name__}.\nNever "
                f"use the {_Container.__name__} class directly; create a subclass and set the 'name' attribute "
                f"as class attribute. "
            )

    @classmethod
    def initialize(cls, obj: Any) -> None:
        cls._check_name_is_present()
        if hasattr(cls, cls.name):
            raise AlreadyInitializedException(
                (
                    f"{cls.name} has already been initialized. "
                    "If you want to initialize a new config_ call "
                    f"{cls.destroy.__name__}()."
                )
            )
        setattr(cls, cls.name, obj)

    @classmethod
    def get(cls) -> Any:
        cls._check_name_is_present()
        return getattr(cls, cls.name)

    @classmethod
    def destroy(cls) -> None:
        cls._check_name_is_present()
        if hasattr(cls, cls.name):
            delattr(cls, cls.name)


class ContainerType(Enum):
    CONFIG = "config_"
    STATE = "state_"


class _Config(_Container):
    name = ContainerType.CONFIG.value


class _State(_Container):
    name = ContainerType.STATE.value


CONTAINER_TYPE_TO_CLASS_MAP = {
    ContainerType.CONFIG: _Config,
    ContainerType.STATE: _State
}


def _initialize(obj_: Any, type_: ContainerType):
    try:
        CONTAINER_TYPE_TO_CLASS_MAP[type_].initialize(obj_)
    except KeyError:
        raise ValueError(
            f"Please give a valid {ContainerType.__name__}."
        )


def _get(type_: ContainerType):
    try:
        return CONTAINER_TYPE_TO_CLASS_MAP[type_].get()
    except KeyError:
        raise ValueError(
            f"Please give a valid {ContainerType.__name__}."
        )


def _destroy(type_: ContainerType):
    try:
        CONTAINER_TYPE_TO_CLASS_MAP[type_].destroy()
    except KeyError:
        raise ValueError(
            f"Please give a valid {ContainerType.__name__}."
        )