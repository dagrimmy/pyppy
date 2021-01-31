import functools
from typing import Callable
from typing import List

from pyppy.utils.exception import UnexpectedNumberOfReturnsException
from pyppy import state


def return_to_state(arg_names: List[str], args_to_return_to_state: List[int] = None) -> Callable:

    def return_to_state_decorator(func: Callable) -> Callable:

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            original_func_return = func(*args, **kwargs)

            if not isinstance(original_func_return, tuple):
                tuple_original_func_return = (original_func_return, )
            else:
                tuple_original_func_return = original_func_return

            if len(tuple_original_func_return) != len(arg_names):
                raise UnexpectedNumberOfReturnsException(
                    (f"The given arg_names {arg_names} have length of {len(arg_names)} but the "
                     f"function decorated with {return_to_state.__name__} returned "
                     f"{len(tuple_original_func_return)} value(s).\n Please make sure the decorated "
                     f"function always returns the correct number of values.")
                )

            if args_to_return_to_state is None:
                _args_to_return_to_state = range(len(arg_names))
            else:
                _args_to_return_to_state = args_to_return_to_state

            for idx in _args_to_return_to_state:
                try:
                    return_val = tuple_original_func_return[idx]
                except IndexError:
                    raise IndexError(
                        (f"Index {idx} is out of range for the returned values of the "
                         f"function decorated with return_to_state.\n The function returned "
                         f"{len(tuple_original_func_return)} values. Please make sure the "
                         f"indices give with the args_to_return_to_state argument have correct "
                         f"values.")
                    )
                setattr(state(), arg_names[idx], return_val)

            return original_func_return

        return wrapper

    return return_to_state_decorator
