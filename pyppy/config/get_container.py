_CONTAINER = "contayner"


class Container:

    def __init__(self):
        pass

    def __str__(self):
        output = ""
        for _, var in vars(self).items():
            output += str(var)
        return output


def destroy_container(container_name=None, destroy_all=False):
    if destroy_all:
        keys = list(container.__dict__.keys())
        for key in keys:
            container.__dict__.pop(key)

    def _destroy(name):
        if not hasattr(container, name):
            return
        delattr(container, name)

    if not container_name:
        _destroy(_CONTAINER)
    else:
        _destroy(container_name)


def container(container_name=None):

    def _get_container(name):
        if not hasattr(container, name):
            setattr(container, name, Container())

        return getattr(container, name)

    if not container_name:
        return _get_container(_CONTAINER)
    else:
        return _get_container(container_name)

