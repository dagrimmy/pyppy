"""
Usage is the same as for :mod:`~pyppy.arg_filling.config`.
"""

from pyppy.arg_filling.args import fill_args_factory, _ArgFillingType


def fill_args_from_state(*args_to_be_filled):
    """
    Usage is the same as for :func:`~pyppy.arg_filling.config.fill_args_from_config`.

    The only difference is that arguments are filled from the
    global state (:func:`~pyppy.container.state.state`) instead of the
    global config (:func:`~pyppy.container.config.config`).
    """
    return fill_args_factory(_ArgFillingType.STATE)(*args_to_be_filled)
