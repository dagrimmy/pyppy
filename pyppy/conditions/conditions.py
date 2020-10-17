import functools
import inspect

from pyppy.config.get_config import config
from pyppy.config.get_container import container
from pyppy.utils.exc import AmbiguousConditionValuesException, ConditionRaisedException


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


def evaluate_single_condition(single_condition):
    exceptions = []

    try:
        conf_value = single_condition(config())
    except Exception as e1:
        exceptions.append(e1)
        conf_value = None

    try:
        cont_value = single_condition(container())
    except Exception as e2:
        exceptions.append(e2)
        cont_value = None

    if conf_value is None and cont_value is None:
        raise ConditionRaisedException(exceptions)

    if conf_value is not None and cont_value is not None:
        if conf_value != cont_value:
            raise AmbiguousConditionValuesException(
                ("\n\tAmbiguous condition values for "
                 "config and container! \n\tThis happens "
                 "because config() and container() hold "
                 "attributes with same names\n\tbut evaluate to "
                 "different boolean values with the current "
                 "condition.\n\tYou might want to choose unique"
                 " names to avoid these errors.")
            )

    if conf_value:
        return conf_value

    if cont_value:
        return cont_value


def s_(single_condition=None, container_name=None, **kwargs):
    def condition_evaluator():
        if single_condition:
            return evaluate_single_condition(single_condition)

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
            condition_check.exp = exp
            if condition_decorator.exp():
                return func(*args, **kwargs)
        return condition_check
    return condition_decorator
