import functools

from pyppy.config.get_config import config


def and_(*args):
    def inner():
        result = []
        for arg in args:
            result.append(arg())
        return all(result)
    return inner


def or_(*args):
    def inner():
        result = []
        for arg in args:
            result.append(arg())
        return any(result)
    return inner


def s_(single_condition):
    def condition_evaluator():
        value = single_condition(config())
        if not isinstance(value, bool):
            raise Exception("Only boolean expressions are allowed!")
        return value
    return condition_evaluator


def condition(exp):

    def condition_decorator(func):
        condition_decorator.exp = exp

        @functools.wraps(func)
        def condition_check(*args, **kwargs):
            if condition_decorator.exp():
                return func(*args, **kwargs)
        return condition_check

    return condition_decorator