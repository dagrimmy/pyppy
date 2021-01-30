"""Global state management

This module provides functions for initializing, accessing and destroying
a global state object. You can initialize a global state from any object.
However, in the context of pyppy, only the instance attributes of the
object are used and work with the decorators ``fill_args`` and ``condition``.
But you can use any object you like. The state management methods are
just a convenience reference to the original object.

Initialization
--------------
In this example, we initialize a global state from a ``NameSpace`` parsed
with a custom ``ArgumentParser``. For demonstration purposes, the parser
will not parse args from the commandline but from a list::

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--message")

    # parse_args returns an argparse.Namespace
    args = parser.parse_args(["--message", "hello!"])

To initialize a global state object, import the function ``initialize_state``
and pass the args variable::

    from pyppy.state import initialize_state
    initialize_state(args)

You can also create an empty global object (which just holds a reference
to an empty ``object``) and change it afterwards via
accessing the global state object (see State access section)::

    from pyppy.state import initialize_state
    initialize_state(args)

Access
------
Now that you have initialized the global state, you can use it
throughout your code::

    from pyppy.state import state
    print(state().message)
    # "hello!"

Note
----
    The original object that you used to initialize the global state
    is returned any time you call ``state()``, so you can do everything
    with the object that you could also do before.

Modification
------------
It is possible to change the global state object during time, e.g. to pass
information between objects in your code. We know that the term 'state'
is not ideal for these use cases and we're working on functionality to
handle these use cases in a better way. Here's an example of state
modification::

    state().message = "bye!"
    print(state().message)

Reset
-----
There can be only one global state object. So whenever you have
initialized a state you cannot initialize a new one. If you try to
an exception is raised. In the rare cases you might want to have
a new global state you can explicitly destroy the current one and
initialize a new one::

    from pyppy.state import destroy_state
    destroy_state()
    initialize_state(args2)

"""
from types import SimpleNamespace
from pyppy.exc import StateAlreadyInitializedException

_STATE = "pyppy-state"


def initialize_state(obj: object = SimpleNamespace()) -> None:
    """
    Initialize a global state with the specified object or
    with an empty ``object`` if no object is given.

    Parameters
    ----------
    obj : object
        Object to initialize the global state with. Whenever
        you will call ``pyppy.state.state()`` you will get a r
        reference to this object.
    Returns
    -------
    None

    Examples
    --------
    >>> destroy_state()
    >>> c = SimpleNamespace()
    >>> c.option = "say_hello"
    >>> initialize_state(c)
    >>> state().option
    'say_hello'
    >>> destroy_state()

    """
    if hasattr(state, _STATE):
        raise StateAlreadyInitializedException(
            (
                "State has already been initialized. "
                "If you want to initialize a new state call "
                f"{destroy_state.__name__}()."
            )
        )
    state(obj)


def state(_obj: object = None) -> object:
    """
    Accesses a previously initialized global state.

    Returns
    -------
    object:
        The object that was used to initialize the global
        state.

    Examples
    --------
    >>> destroy_state()
    >>> c = SimpleNamespace()
    >>> c.option = "say_hello"
    >>> initialize_state(c)
    >>> state().option
    'say_hello'
    >>> destroy_state()
    """
    if not hasattr(state, _STATE) and _obj:
        setattr(state, _STATE, _obj)
    if not hasattr(state, _STATE):
        raise Exception("Please initialize state first!")

    return getattr(state, _STATE)


def destroy_state() -> None:
    """
    Deletes the global reference to the object that the state
    was initialized with.

    Examples
    --------
    >>> destroy_state()
    >>> c = SimpleNamespace()
    >>> c.option = "say_hello"
    >>> initialize_state(c)
    >>> state().option
    'say_hello'
    >>> destroy_state()
    >>> state().option
    Traceback (most recent call last):
    ...
    Exception: Please initialize state first!
    """
    if hasattr(state, _STATE):
        delattr(state, _STATE)
