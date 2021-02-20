from pyppy.conditions import Exp, _condition
from pyppy.config_ import initialize_config, config
import types

args = types.SimpleNamespace()
args.debug = False
initialize_config(args)

@_condition(Exp(debug=True))
def debug_log():
    return "hello"


assert not debug_log()

config().debug = True

assert debug_log() == "hello"