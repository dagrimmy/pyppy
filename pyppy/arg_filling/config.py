"""Automatic Argument Filling from Config

Contains a decorator generator that allows to automatically fill
function arguments based on attributes of the global config_ created
with ``initialize_config(obj)``.

General Example
---------------
Sounds too abstract? Here's an example::

    from argparse import ArgumentParser
    from pyppy.args import fill_args
    from pyppy.config_ import initialize_config

    parser = ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False
    )

    cli_args = ["--debug"]
    args = parser.parse_args(cli_args)

    initialize_config(args)


    @fill_args()
    def log_debug(debug, message):
        if debug is True:
            print(message)


    log_debug(message="debugging")
    # will print "debugging"

Let's go through the example step by step. First, we define an
``ArgumentParser`` which can read in some arguments and parse them.
In this case, we have an argument `--debug` which will, when specified,
be ``True`` otherwise ``False``. The ``ArgumentParser`` will return
an ``argparse.Namespace`` object that holds an attribute ``debug``
with the corresponding value.

Then, we initialize our config_ with the returned ``Namespace`` object.
This will register a global config_ that we can access by calling
``pyppy.config_.config_()``. So, calling ``config_().debug``
will result in ``True``.


After that, we
define a function and tell it to automatically fill its arguments based
on the attributes of the global configuration we just registered. For
this, we use the decorator generator ``fill_args`` that will, when called,
return a function generator able to fill the arguments of the function.
It will look for parameters in the function's definition that have the
same name as attributes of the global config_. In this case we have
an exact match between ``debug`` in the function parameters and the
global configuration attribute ``debug``. So, when executing the function
``log_debug`` we don't have to provide debug because it has already assigned
an value equal to the attribute's value in the global config_.```

When calling ``log_debug``, we have to provide the ``message`` argument
as keyword argument (this is currently necessary; we're working on
allowing positional parameters too...). That's it. You can use this
for whatever parameters you want to be filled from the global config_.

Explicit Argument Filling
-------------------------

There are cases where you might not want ``fill_args``  to
automatically detect the arguments to be filled for you. In these
cases, you can tell ``fill_args`` explicitly which arguments you
want to fill from the config_::

    @fill_args("debug")
    def log_debug(debug, message):
        if debug is True:
            print(message)

When specifying explicitly filled arguments, only these arguments
are filled. So if there are other matching parameters they will be
left untouched. You can specify as many explicit arguments as you want;
just pass the comma-separated as strings to the ``fill_args`` method.

Note
----
    Currently only function signatures are allowed where each argument
    can be specified as keyword argument when calling the function.
    E.g. you can not use positional-only arguments when using the
    ``fill_args`` function. The following signature, for example,
    will not work: ``func(x, y, /, z, a="b")``.
"""

from pyppy.arg_filling.args import fill_args_factory, _ArgFillingType


def fill_args_from_config(*args_to_be_filled):
    """
    Returns a function decorator that automatically fills function
    arguments based on the global config_ object attributes. Function arguments
    that have the same name as an attribute of the global config_ will
    be automatically filled with the corresponding value when the
    decorated function is executed.

    Parameters
    ----------
    args_to_be_filled : str
        Varargs parameter that allows to explicitly set the arguments that
        are filled from the global configs attributes. The Decorator returned
        from ``fill_args`` will only fill the explicitly mentioned arguments
        and will leave every other argument untouched.

    Returns
    -------
    Callable :
        Wrapper around the original function that will take care of argument
        filling functionality when the decorated function is called.

    Examples
    --------
    >>> from pyppy import config
    >>> from pyppy import initialize_config, destroy_config
    >>> from types import SimpleNamespace
    >>> destroy_config()
    >>> c = SimpleNamespace()
    >>> c.debug_level = "WARN"
    >>> initialize_config(c)
    >>> config_().debug_level
    'WARN'
    >>> @fill_args()
    ... def debug(debug_level, message):
    ...     if debug_level == "WARN":
    ...         return message
    >>> debug(message="WARNING!!!")
    'WARNING!!!'
    """
    return fill_args_factory(_ArgFillingType.CONFIG)(*args_to_be_filled)
