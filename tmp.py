import argparse

from pyppy.config.get_config import config
from pyppy.config.get_config import initialize_config

parser = argparse.ArgumentParser(description="Test")
parser.add_argument("--tmp")

args = parser.parse_args(["--tmp", "val"])
initialize_config(args)

print(config())