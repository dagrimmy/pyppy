from contextlib import contextmanager
from argparse import Namespace

from pyppy.config.get_config import destroy_config, initialize_config, config
from pyppy.config.get_container import destroy_container, container


def _fake_config(**kwargs):
    destroy_config()

    namespace = Namespace()
    for k, v in kwargs.items():
        setattr(namespace, k, v)

    initialize_config(namespace)


@contextmanager
def fake_config(**kwargs):
    _fake_config(**kwargs)

    try:
        yield
    finally:
        destroy_config()


def _fake_container(**kwargs):
    destroy_container()

    for k, v in kwargs.items():
        setattr(container(), k, v)


@contextmanager
def fake_container(**kwargs):
    _fake_container(**kwargs)

    try:
        yield
    finally:
        destroy_container()


@contextmanager
def container_config_cleanup():
    try:
        yield
    finally:
        destroy_container()
        destroy_config()
