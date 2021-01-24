"""
Contains functions for conditional execution of
functions based on the global config.
"""

import functools
from typing import Callable
from typing import Any

from pyppy.config import config
from pyppy.exc import ConditionRaisedException, ConditionDidNotReturnBooleansException
from pyppy.utils import _check_is_bool


def evaluate_single_condition(single_condition):
    """
    Evaluates the value of a single condition.
    """
    exceptions = []

    try:
        conf_value = single_condition(config())
    except Exception as exc:  # pylint: disable=W0703
        exceptions.append(exc)
        conf_value = None

    if conf_value is None:
        raise ConditionRaisedException(exceptions)

    if _check_is_bool(conf_value):
        return conf_value

    raise ConditionDidNotReturnBooleansException(
        "The condition did not return a valid boolean!"
    )


class Exp:  # pylint: disable=R0903
    """
    Class that represents a boolean logic based on the global
    config. On creation, a condition or keyword arguments are
    given (mutually exclusiv). When an object of this class is
    called the given condition is evaluated or the keyword
    arguments are transformed into exact matches with the global
    configs attributes.

    """

    def __init__(self, single_condition=None, **kwargs):
        self._single_condition = single_condition
        self._kwargs = kwargs

    def __call__(self):
        if self._single_condition:
            return evaluate_single_condition(self._single_condition)

        if len(self._kwargs) > 1:
            raise Exception("Only one key value pair allowed")
        key, val = list(self._kwargs.items())[0]

        if not hasattr(config(), key):
            return False

        if getattr(config(), key) is val:  # pylint: disable=R1703
            return True

        return False


def condition(exp: Callable[[], bool]) -> Callable[[Any], Any]:
    """
    Returns a function decorator that will evaluate the given expression
    when the decorated function is called and will execute the decorated
    function when the boolean value is True.

    The expressions boolean value is usually dependent on the global
    config object but it is only important that it is a boolean value
    and not how it is generated.
    """

    def condition_decorator(func):
        """
        Decorates a function and will evaluate the expression that has
        been given to the 'condition' function.

        """
        condition_decorator.exp = exp

        @functools.wraps(func)
        def condition_check(*args, **kwargs):
            condition_result = condition_decorator.exp()

            if condition_result:
                return func(*args, **kwargs)

            return None

        return condition_check

    return condition_decorator


def and_(*exps: Callable[[], bool]) -> Callable[[], bool]:
    """
    Returns a function that is able to build the
    logical conjunction of the given expressions.
    So, when the returned function is executed
    it is checked whether all given expressions
    return True.
    """

    def and_evaluator():
        for exp in exps:
            current = exp()
            if not current:
                return False
        return True

    return and_evaluator


def or_(*exps: Callable[[], bool]) -> Callable[[], bool]:
    """
    Returns a function that is able to build the
    logical dijunction of the given expressions.
    So, when the returned function is executed
    it is checked whether at least one of the
    given expressions returns True.
    """

    def or_evaluator():
        for exp in exps:
            if exp():
                return True
        return False

    return or_evaluator
