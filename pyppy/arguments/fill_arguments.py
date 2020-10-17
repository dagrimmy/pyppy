from inspect import signature

from pyppy.config.get_config import config
from pyppy.utils.exc import MissingConfigParamException


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


def fill_function_parameters_from_config(params):
    new_params = {}
    for param in params:
        name, val = param
        if name in config():
            val = getattr(config(), name)
        if not val:
            raise MissingConfigParamException(
                f"Param {name} not found in config!"
            )
        new_params[name] = val

    return new_params


def fill_arguments(func):
    params = get_function_params(func)

    def inner():
        new_params = fill_function_parameters_from_config(params)
        return func(**new_params)

    return inner
