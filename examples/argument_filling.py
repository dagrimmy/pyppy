from pyppy.args import fill_args
from pyppy.config import config, initialize_config

initialize_config()
config().debug = True

@fill_args()
def debug_log(debug):
    if debug:
        return "debugging"

assert debug_log() == "debugging"

config().debug = False

assert not debug_log()
