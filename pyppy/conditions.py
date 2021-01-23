"""
Contains functions for conditional execution of
functions based on the global config.
"""

import functools

from pyppy.config import config
from pyppy.exc import (
    ConditionRaisedException,
    ConditionDidNotReturnBooleansException
)


def and_(*exps):
    """
    Takes a variable number of expressions and builds
    the logical 'and' value from all of the boolean values
    return by the single expressions.
    """
    def inner():
        for arg in exps:
            current = arg()
            if not current:
                return False
        return True
    return inner


def or_(*args):
    """
    Takes a variable number of expressions and builds
    the logical 'or' value from all of the boolean values
    return by the single expressions.
    """
    def inner():
        for arg in args:
            if arg():
                return True
        return False
    return inner


def _check_bool(value):
    if isinstance(value, bool):  # pylint: disable=R1703
        return True

    return False


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

    if _check_bool(conf_value):
        return conf_value

    raise ConditionDidNotReturnBooleansException(
        "The condition did not return a valid boolean!"
    )


def exp(single_condition=None, **kwargs):
    """
    Expression that returs true based on the given condition.
    """
    def condition_evaluator():
        if single_condition:
            return evaluate_single_condition(single_condition)

        if len(kwargs) > 1:
            raise Exception(
                "Only one key value pair allowed"
            )
        key, val = list(kwargs.items())[0]

        if not hasattr(config(), key):
            return False

        if getattr(config(), key) is val:  # pylint: disable=R1703
            return True

        return False

    return condition_evaluator


def condition(exp_):
    """
    Function decorator that assumes an expression
    yielding a boolean value based on which the
    decorated function is executed or not.
    """
    def condition_decorator(func):
        condition_decorator.exp = exp_
        func.exp = exp_

        @functools.wraps(func)
        def condition_check(*args, **kwargs):
            condition_check.exp = exp_
            condition_result = condition_decorator.exp()

            if condition_result:
                return func(*args, **kwargs)

            return None
        return condition_check
    return condition_decorator
