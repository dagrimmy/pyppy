import functools
from inspect import signature

from pyppy.config.get_config import config
from pyppy.config.get_container import container
from pyppy.utils.constants import UNSET_VALUE
from pyppy.utils.exc import MissingConfigParamException, ConflictingArgumentValuesException


def get_function_params(function):
    sig = signature(function)

    out = []

    for name, param in sig.parameters.items():
        if param.default is param.empty:
            value = None
        else:
            value = param.default

        out.append((name, value))

    return out


def fill_function_parameters(params):
    new_params = {}
    for param in params:
        name, val = param
        conf_val = UNSET_VALUE
        if name in config():
            conf_val = getattr(config(), name)

        cont_val = UNSET_VALUE
        if hasattr(container(), name):
            cont_val = getattr(container(), name)

        if conf_val is UNSET_VALUE and cont_val is UNSET_VALUE:
            raise MissingConfigParamException(
                f"Param {name} not found in config or container!"
            )

        if conf_val is not UNSET_VALUE and cont_val is not UNSET_VALUE:
            if cont_val is not conf_val:
                raise ConflictingArgumentValuesException(
                    (f"Found param with name {name} in config and "
                     f"container with conflicting values!")
                )

        if cont_val is not UNSET_VALUE:
            val = cont_val

        if conf_val is not UNSET_VALUE:
            val = conf_val

        new_params[name] = val

    return new_params


def fill_arguments(func):
    params = get_function_params(func)

    @functools.wraps(func)
    def argument_filler():
        new_params = fill_function_parameters(params)
        return func(**new_params)

    return argument_filler
