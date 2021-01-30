from pyppy.config_.args import fill_args
from pyppy.config_ import initialize_config, config

initialize_config()
config().debug = True

@fill_args()
def debug_log(debug, message):
    if debug:
        return f"debugging: {message}"

assert debug_log(message="useful logs") == "debugging: useful logs"

config().debug = False

assert not debug_log(message="useful logs")
