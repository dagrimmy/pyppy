from contextlib import contextmanager
from argparse import Namespace

from pyppy import destroy_config, initialize_config
from pyppy import destroy_state, initialize_state


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


def _fake_state(**kwargs):
    destroy_state()

    namespace = Namespace()
    for k, v in kwargs.items():
        setattr(namespace, k, v)

    initialize_state(namespace)


@contextmanager
def fake_state(**kwargs):
    _fake_state(**kwargs)

    try:
        yield
    finally:
        destroy_state()

