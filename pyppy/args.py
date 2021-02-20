"""
TODO
"""

import functools
from inspect import signature
from typing import Callable, Any

from pyppy.container import get
from pyppy.utils.exception import (
    FunctionSignatureNotSupportedException,
    OnlyKeywordArgumentsAllowedException,
    IllegalStateException,
)


_UNSET_VALUE = "<pyppy-unset-value>"


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


def fill_args_factory(container_name: str) -> Callable:
    """
    TODO
    """

    def _fill_args(*args_to_be_filled: str) -> Callable:

        def _fill_args_decorator(func: Callable) -> Callable:
            """
            Function decorator that takes a function and return a new
            function that will, when executed, fill arguments of the
            original function based on their value in the global config_.
            Currently specific function signatures are supported.
            The decorator checks if a function signature is supported
            and raises an exception otherwise.
            """
            _check_func_signature_supported(func)
            sig = signature(func)
            filled_kwargs = {}

            @functools.wraps(func)
            def _argument_filler(*args: Any, **kwargs: Any) -> Callable:
                """
                Wrapper around the original function. This function checks
                if arguments of the original function have the same name
                as attributes of the global config_.
                If the arguments to be filled have been set explicitly
                in the fill_args function only the corresponding arguments
                are checked.
                If arguments are declared a arguments to be filled but are
                not present in the global config_ object it is still
                possible to provide them as keyword argument on function
                execution. If the corresponding arguments are not filled
                from the config_ and not provided on function execution
                an exception is raised.
                """
                for name, _ in sig.parameters.items():
                    if name in args_to_be_filled or len(args_to_be_filled) == 0:
                        try:
                            value = getattr(get[container_name], name)
                        except AttributeError:
                            value = _UNSET_VALUE
                        filled_kwargs[name] = value

                if len(args) > 0:
                    raise OnlyKeywordArgumentsAllowedException(
                        (
                            f"Only keyword arguments are allowed when executing a "
                            f"function defined with the {_fill_args.__name__} "
                            f"decorator."
                        )
                    )

                filled_kwargs.update(kwargs)

                for name, value in filled_kwargs.items():
                    if value is _UNSET_VALUE:
                        raise IllegalStateException(
                            f"\n\tArgument {name} was not present in the global \n\t"
                            f"config_ and was not provided as keyword argument when \n\t"
                            f"the function {func} was executed. Please make sure \n\t"
                            f"needed arguments are either provided within the config_ \n\t"
                            f"or when running a {_fill_args.__name__}-decorated function."
                        )

                return func(**filled_kwargs)

            return _argument_filler

        return _fill_args_decorator

    return _fill_args


class Fill:

    """Kind of a fill_args factory"""

    def __getattr__(self, container_name):
        return fill_args_factory(container_name)


fill = Fill()
fill.__doc__ = """fill is shorthand for Fill()"""