import functools
from typing import Callable
from typing import Any

from pyppy.container import get
from pyppy.utils.data_type import _check_is_bool
from pyppy.utils.exception import ConditionRaisedException, ConditionDidNotReturnBooleansException


def _evaluate_condition_func(container_name, single_condition: Callable[[object], bool]) -> bool:
    """
    Evaluates a condition function based on the state
    of the global config.
    """

    try:
        conf_value = single_condition(config())
    except Exception as exc:  # pylint: disable=W0703
        raise ConditionRaisedException from exc

    if _check_is_bool(conf_value):
        return conf_value

    raise ConditionDidNotReturnBooleansException(
        "The condition did not return a valid boolean!"
    )


class Exp:  # pylint: disable=R0903

    def __init__(self, condition_func=None, **kwargs):
        self._single_condition = condition_func
        self._kwargs = kwargs

    def __call__(self, container_name):
        if self._single_condition:
            return _evaluate_condition_func(container_name, self._single_condition)

        if len(self._kwargs) > 1:
            raise Exception("Only one key value pair allowed")
        key, val = list(self._kwargs.items())[0]

        if not hasattr(get(container_name), key):
            return False

        if getattr(get(container_name), key) is val:  # pylint: disable=R1703
            return True

        return False


def _condition_factory(container_name):
    def _condition(exp: Callable[[str], bool]) -> Callable[[Any], Any]:

        def condition_decorator(func):

            condition_decorator.exp = exp

            @functools.wraps(func)
            def condition_check(*args, **kwargs):
                condition_result = condition_decorator.exp(container_name)

                if condition_result:
                    return func(*args, **kwargs)

                return None

            return condition_check

        return condition_decorator

    return _condition


def and_(*exps: Callable[[], bool]) -> Callable[[], bool]:

    def and_evaluator():
        for exp in exps:
            current = exp()
            if not current:
                return False
        return True

    return and_evaluator


def or_(*exps: Callable[[], bool]) -> Callable[[], bool]:
    def or_evaluator():
        for exp in exps:
            if exp():
                return True
        return False

    return or_evaluator


class Condition:

    """Kind of a fill_args factory"""

    def __getattr__(self, container_name):
        return _condition_factory(container_name)


condition = Condition()
condition.__doc__ = """fill is shorthand for Fill()"""