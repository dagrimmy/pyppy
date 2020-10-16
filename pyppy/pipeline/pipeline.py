import functools
from inspect import signature

from pyppy.config.get_config import config
from pyppy.utils.exc import MissingPipelineException, MissingConfigParamException


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


def step(pipeline_name):

    def decorator(func):
        params = get_function_params(func)

        @functools.wraps(func)
        def inner():
            new_params = fill_function_parameters_from_config(params)
            return func(**new_params)

        Pipeline.pipelines.setdefault(
            pipeline_name, []
        ).append(inner)

        return inner
    return decorator


class Pipeline:

    pipelines = {}

    @staticmethod
    def _check_pipeline_name(pipeline_name):
        if pipeline_name not in Pipeline.pipelines:
            raise MissingPipelineException(
                f"Pipeline with name {pipeline_name} does not exist!"
            )

    @staticmethod
    def run_r(pipeline_name):
        Pipeline._check_pipeline_name(pipeline_name)
        for func in Pipeline.pipelines[pipeline_name]:
            yield func()

    @staticmethod
    def run(pipeline_name):
        Pipeline._check_pipeline_name(pipeline_name)
        for func in Pipeline.pipelines[pipeline_name]:
            func()

    @staticmethod
    def destroy():
        Pipeline.pipelines = {}
