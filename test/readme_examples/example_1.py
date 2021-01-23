from argparse import ArgumentParser
from pyppy.config import initialize_config, config

parser = ArgumentParser()
parser.add_argument(
    "--debug",
    action="store_true",
    default=False
)

cli_args = ["--debug"]
args = parser.parse_args(cli_args)

initialize_config(args)


def debug_log():
    if config().debug:
        print("debugging")