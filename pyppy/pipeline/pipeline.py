from inspect import signature

from pyppy.config.get_config import config
from pyppy.utils.exc import MissingPipelineException, MissingConfigParamException, PipelineAlreadyExistsException


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


def step(pipeline_name, step_name=None):

    def decorator(func):
        if not step_name:
            inner_step_name = func.__name__
        else:
            inner_step_name = step_name

        Pipeline.pipelines.setdefault(
            pipeline_name, []
        ).append((inner_step_name, func))

        return func
    return decorator


class Pipeline:

    pipelines = {}

    @staticmethod
    def _pipeline_exists(pipeline_name):
        if pipeline_name in Pipeline.pipelines:
            return True
        else:
            return False

    @staticmethod
    def run_r(pipeline_name):
        if not Pipeline._pipeline_exists(pipeline_name):
            raise MissingPipelineException((
                f"Pipeline with name {pipeline_name} does "
                f"not exist!"
            ))
        for func in Pipeline.pipelines[pipeline_name]:
            yield func[0], func[1]()

    @staticmethod
    def run(pipeline_name):
        if not Pipeline._pipeline_exists(pipeline_name):
            raise MissingPipelineException((
                f"Pipeline with name {pipeline_name} does "
                f"not exist!"
            ))
        for func in Pipeline.pipelines[pipeline_name]:
            func[1]()

    @staticmethod
    def destroy(pipeline_name=None):
        if not pipeline_name:
            Pipeline.pipelines = {}
        else:
            Pipeline.pipelines.pop(pipeline_name, None)

    @staticmethod
    def create_pipeline(pipeline_name, iterable_of_tuples, extend=False):
        if Pipeline._pipeline_exists(pipeline_name) and not extend:
            raise PipelineAlreadyExistsException((
                f"Pipeline with name {pipeline_name} already exists!"
            ))
        for item in iterable_of_tuples:
            Pipeline.pipelines.setdefault(
                pipeline_name, []
            ).append(item)
