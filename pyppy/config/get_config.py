CONFIG = "pyppy"


def initialize_config():
    config()


def config():
    if not hasattr(config, CONFIG):
        config.pyppy = "tmp"

    return config.pyppy

