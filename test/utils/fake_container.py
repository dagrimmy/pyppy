from contextlib import contextmanager
from types import SimpleNamespace

from pyppy.container import container


def _fake_container(name: str, **kwargs):
    namespace = SimpleNamespace()
    for k, v in kwargs.items():
        setattr(namespace, k, v)

    container[name].initialize(namespace)


@contextmanager
def fake_container(name, **kwargs):
    _fake_container(name, **kwargs)

    try:
        yield
    finally:
        container.destroy_all()
