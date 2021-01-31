from pyppy.arg_filling.args import fill_args_factory, _ArgFillingType


def fill_args_from_state(*args_to_be_filled):
    return fill_args_factory(_ArgFillingType.STATE)(*args_to_be_filled)
