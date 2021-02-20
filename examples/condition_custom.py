from pyppy.conditions import Exp, _condition
from pyppy.config_ import initialize_config, config
import types

args = types.SimpleNamespace()
args.log_level = "WARN_LEVEL_1"

initialize_config(args)

@_condition(Exp(lambda config: config.log_level.startswith("WARN")))
def log_warn():
    return "WARNING"

assert log_warn() == "WARNING"

config().log_level = "INFO_LEVEL_2"

assert not log_warn()
