import functools

from pyppy.config.get_config import config


def and_(*args):
    def inner():
        for arg in args:
            current = arg()
            if not current:
                return False
        return True
    return inner


def or_(*args):
    def inner():
        for arg in args:
            if arg():
                return True
        return False
    return inner


def s_(single_condition=None, **kwargs):
    def condition_evaluator():
        if single_condition:
            value = single_condition(config())
            if not isinstance(value, bool):
                raise Exception("Only boolean expressions are allowed!")
            return value

        if len(kwargs) > 1:
            raise Exception(
                "Only one key value pair allowed"
            )
        k, v = list(kwargs.items())[0]

        if not hasattr(config(), k):
            return False

        if getattr(config(), k) == v:
            return True
        else:
            return False

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