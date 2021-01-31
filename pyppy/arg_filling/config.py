from pyppy.arg_filling.args import fill_args_factory, _ArgFillingType


def fill_args_from_config(*args_to_be_filled):
    return fill_args_factory(_ArgFillingType.CONFIG)(*args_to_be_filled)
