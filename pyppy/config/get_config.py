CONFIG = "pyppy"


def initialize_config(args):
    config(args)


def config(args=None):
    if not hasattr(config, CONFIG) and args:
        setattr(config, CONFIG, args)
    if not hasattr(config, CONFIG):
        raise Exception("Please initialize config first!")

    return getattr(config, CONFIG)


def destroy_config():
    if hasattr(config, CONFIG):
        delattr(config, CONFIG)
