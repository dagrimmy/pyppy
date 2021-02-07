from contextlib import contextmanager
from types import SimpleNamespace

from pyppy.container import destroy, initialize


def _fake_container(name: str, **kwargs):
    destroy(name)

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
        destroy(name)
