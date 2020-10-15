from collections import namedtuple


class Namespace:

    def __init__(self):
        pass


def get_fake_argparse_namespace(key_value_pairs):
    namespace = Namespace()

    for key_value_pair in key_value_pairs:
        if len(key_value_pair) != 2:
            raise Exception("Key value pairs not valid")
        setattr(namespace, key_value_pair[0], key_value_pair[1])

    return namespace