"""
Contains functions for automatic argument filling from the
global config object. This file also has some helper functions
for accomplishing this task.
"""

import functools
from inspect import signature
from typing import Callable, Iterable, Any

from pyppy.config import config
from pyppy.constants import UNSET_VALUE
from pyppy.exc import (
    FunctionSignatureNotSupportedException,
    OnlyKeywordArgumentsAllowedException,
    IllegalStateException,
)


def _get_attribute(attribute: str, obj: object) -> object:
    """
    Get specified attribute from the given object or
    else return the value of the constant UNSET_VALUE.
    """
    val = UNSET_VALUE
    if hasattr(obj, attribute):
        val = getattr(obj, attribute)

    return val


def _get_value_from_config_or_container(param_name: str) -> object:
    config_val = _get_attribute(param_name, config())

    if config_val is UNSET_VALUE:
        return UNSET_VALUE

    return config_val


def _check_function_signature_supported(func: Callable) -> None:
    """
    Checks if a given function has a supported type.
    If function signature includes parameters that are
    of kind POSTIONAL_ONLY, VAR_KEYWORD or VAR_POSITIONAL
    an FunctionSignatureNotSupportedException is raised.
    """
    sig = signature(func)

    for _, param in sig.parameters.items():
        if param.kind in (
            param.POSITIONAL_ONLY,
            param.VAR_KEYWORD,
            param.VAR_POSITIONAL,
        ):
            raise FunctionSignatureNotSupportedException(
                (
                    "Currently only functions with arguments that have types "
                    "of POSITIONAL_OR_KEYWORD and KEYWORD_ONLY are supported."
                )
            )


def fill_arguments(*arguments_to_be_filled: Iterable[str]) -> Callable:
    """
    Function decorator that can be used to fill arguments
    of the decorated function by looking them up in the global
    config object.
    """

    def fill_arguments_decorator(func: Callable) -> Callable:
        _check_function_signature_supported(func)
        sig = signature(func)
        filled_kwargs = {}

        @functools.wraps(func)
        def argument_filler(*args: Any, **kwargs: Any) -> Callable:
            for name, _ in sig.parameters.items():
                if name in arguments_to_be_filled or len(arguments_to_be_filled) == 0:
                    value = _get_value_from_config_or_container(name)
                    filled_kwargs[name] = value

            if len(args) > 0:
                raise OnlyKeywordArgumentsAllowedException(
                    (
                        f"Only keyword arguments are allowed when executing a "
                        f"function defined with the {fill_arguments.__name__} "
                        f"decorator."
                    )
                )

            filled_kwargs.update(kwargs)

            for name, value in filled_kwargs.items():
                if value is UNSET_VALUE:
                    raise IllegalStateException(
                        f"\n\tArgument {name} was not filled from context \n\t"
                        f"(container, config) and was not provided when \n\t"
                        f"the function {func} was executed. Please make sure \n\t"
                        f"needed arguments are either provided within the context "
                        f"or when running a 'fill_arguments'-decorated function."
                    )

            return func(**filled_kwargs)

        return argument_filler

    return fill_arguments_decorator
