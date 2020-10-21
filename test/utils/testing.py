from contextlib import contextmanager
from argparse import Namespace
from typing import List, Tuple

from pyppy.config.get_config import destroy_config, initialize_config
from pyppy.config.get_container import destroy_container, container


def _fake_config(fake_args: List[Tuple]):
    destroy_config()

    namespace = Namespace()
    for arg in fake_args:
        setattr(namespace, arg[0], arg[1])

    initialize_config(namespace)


@contextmanager
def fake_config(fake_args: List[Tuple]):
    _fake_config(fake_args)

    try:
        yield
    finally:
        destroy_config()


def _fake_container(fake_args):
    destroy_container(destroy_all=True)

    for arg in fake_args:
        setattr(container(), arg[0], arg[1])


@contextmanager
def fake_container(fake_args: List[Tuple]):
    _fake_container(fake_args)

    try:
        yield
    finally:
        destroy_container(destroy_all=True)


@contextmanager
def fake_container_and_config(container_fake_args, config_fake_args):
    _fake_container(container_fake_args)
    _fake_config(config_fake_args)

    try:
        yield
    finally:
        destroy_container(destroy_all=True)
        destroy_config()
