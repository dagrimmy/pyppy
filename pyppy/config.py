"""
Contains functions for managing a global config
object.
"""

from argparse import Namespace

from pyppy.exc import ConfigAlreadyInitializedException

_CONFIG = "confyg"


def initialize_config(args=Namespace()):
    """
    Initialize the global config with the specified
    object. The input object should only contain
    instance attributes that can be access by using
    the dot notation: "obj.<attribute>".
    """
    if hasattr(config, _CONFIG):
        raise ConfigAlreadyInitializedException((
            "Config has already been initialized. "
            "If you want to initialize a new config call "
            f"{destroy_config.__name__}()."
        ))
    config(args)


def config(args=None):
    """
    Provides access to the global config object.
    """
    if not hasattr(config, _CONFIG) and args:
        setattr(config, _CONFIG, args)
    if not hasattr(config, _CONFIG):
        raise Exception("Please initialize config first!")

    return getattr(config, _CONFIG)


def destroy_config():
    """
    Destroys the current global config so a new one
    can be initialized.
    """
    if hasattr(config, _CONFIG):
        delattr(config, _CONFIG)
