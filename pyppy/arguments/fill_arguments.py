import functools
from inspect import signature

from pyppy.config.get_config import config
from pyppy.config.get_container import container
from pyppy.utils.constants import UNSET_VALUE
from pyppy.utils.exc import MissingConfigParamException, ConflictingArgumentValuesException, \
    FunctionSignatureNotSupportedException, OnlyKeywordArgumentsAllowedException, IllegalStateException


def _get_value(param_name, obj):
    val = UNSET_VALUE
    if hasattr(obj, param_name):
        val = getattr(obj, param_name)

    return val


def _get_value_from_config_or_container(param_name):
    config_val = _get_value(param_name, config())
    container_val = _get_value(param_name, container())

    if config_val is UNSET_VALUE and container_val is UNSET_VALUE:
        return UNSET_VALUE

    if config_val is not UNSET_VALUE and container_val is not UNSET_VALUE:
        if container_val is not config_val:
            raise ConflictingArgumentValuesException(
                (f"Found param with name {param_name} in config and "
                 f"container with conflicting values!")
            )

    if container_val is not UNSET_VALUE:
        val = container_val

    if config_val is not UNSET_VALUE:
        val = config_val

    return val


def _check_function_signature_supported(func):
    sig = signature(func)

    for name, param in sig.parameters.items():
        if param.kind in (param.POSITIONAL_ONLY,
                          param.VAR_KEYWORD,
                          param.VAR_POSITIONAL):
            raise FunctionSignatureNotSupportedException(
                f"Currently only functions with arguments that have types "
                f"of POSITIONAL_OR_KEYWORD and KEYWORD_ONLY are supported."
            )


def fill_arguments(*arguments_to_be_filled):

    def fill_arguments_decorator(func):
        _check_function_signature_supported(func)
        sig = signature(func)
        filled_kwargs = {}

        for name, param in sig.parameters.items():
            if name in arguments_to_be_filled or len(arguments_to_be_filled) == 0:
                value = _get_value_from_config_or_container(name)
                filled_kwargs[name] = value

        @functools.wraps(func)
        def argument_filler(*args, **kwargs):
            if len(args) > 0:
                raise OnlyKeywordArgumentsAllowedException(
                    (f"Only keyword arguments are allowed when executing a "
                     f"function defined with the {fill_arguments.__name__} "
                     f"decorator.")
                )

            filled_kwargs.update(kwargs)

            for name, value in filled_kwargs.items():
                if value == UNSET_VALUE:
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
