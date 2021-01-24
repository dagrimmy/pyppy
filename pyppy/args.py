"""
Contains functions for automatic argument filling from the
global config object. This file also has some helper functions
for accomplishing this task.
"""

import functools
from inspect import signature
from typing import Callable, Iterable, Any

from pyppy.config import config
from pyppy.const import UNSET_VALUE
from pyppy.exc import (
    FunctionSignatureNotSupportedException,
    OnlyKeywordArgumentsAllowedException,
    IllegalStateException,
)


def _check_func_signature_supported(func: Callable) -> None:
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


def fill_args(*args_to_be_filled: Iterable[str]) -> Callable:
    """
    Returns a function decorator that automatically fills function
    arguments based on the global config object. Function arguments
    that have the same name as an attribute of the global config will
    be automatically filled with the corresponding value when the
    decorated function is executed.

    Arguments to be filled can be set explictly via the arguments_to_be_filled
    varargs argument.
    """

    def fill_args_decorator(func: Callable) -> Callable:
        """
        Function decorator that takes a function and return a new
        function that will, when executed, fill arguments of the
        original function based on their value in the global config.

        Currently specific function signatures are supported.
        The decorator checks if a function signature is supported
        and raises an exception otherwise.
        """
        _check_func_signature_supported(func)
        sig = signature(func)
        filled_kwargs = {}

        @functools.wraps(func)
        def argument_filler(*args: Any, **kwargs: Any) -> Callable:
            """
            Wrapper around the original function. This function checks
            if arguments of the original function have the same name
            as attributes of the global config.

            If the arguments to be filled have been set explicitly
            in the fill_args function only the corresponding arguments
            are checked.

            If arguments are declared a arguments to be filled but are
            not present in the global config object it is still
            possible to provide them as keyword argument on function
            execution. If the corresponding arguments are not filled
            from the config and not provided on function execution
            an exception is raised.
            """
            for name, _ in sig.parameters.items():
                if name in args_to_be_filled or len(args_to_be_filled) == 0:
                    try:
                        value = getattr(config(), name)
                    except AttributeError:
                        value = UNSET_VALUE
                    filled_kwargs[name] = value

            if len(args) > 0:
                raise OnlyKeywordArgumentsAllowedException(
                    (
                        f"Only keyword arguments are allowed when executing a "
                        f"function defined with the {fill_args.__name__} "
                        f"decorator."
                    )
                )

            filled_kwargs.update(kwargs)

            for name, value in filled_kwargs.items():
                if value is UNSET_VALUE:
                    raise IllegalStateException(
                        f"\n\tArgument {name} was not present in the global \n\t"
                        f"config and was not provided as keyword argument when \n\t"
                        f"the function {func} was executed. Please make sure \n\t"
                        f"needed arguments are either provided within the config \n\t"
                        f"or when running a 'fill_arguments'-decorated function."
                    )

            return func(**filled_kwargs)

        return argument_filler

    return fill_args_decorator
