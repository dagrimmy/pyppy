_CONFIG = "contayner"


class Container:

    def __init__(self):
        pass


def container():
    if not hasattr(container, _CONFIG):
        setattr(container, _CONFIG, Container())

    return getattr(container, _CONFIG)
