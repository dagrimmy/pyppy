from contextlib import contextmanager
from types import SimpleNamespace

from pyppy.container import initialize, destroy, destroy_all


def _fake_container(name: str, **kwargs):
    namespace = SimpleNamespace()
    for k, v in kwargs.items():
        setattr(namespace, k, v)

    initialize(name, namespace)


@contextmanager
def fake_container(name, **kwargs):
    _fake_container(name, **kwargs)

    try:
        yield
    finally:
        destroy_all()
