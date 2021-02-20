from pyppy.conditions import _condition, Exp, and_
import types

from pyppy.config_ import initialize_config, config

args = types.SimpleNamespace()
args.log_level = "WARN"
args.specific_log_level = "LEVEL_1"

initialize_config(args)

@_condition(
    and_(
        Exp(log_level="WARN"),
        Exp(specific_log_level="LEVEL_1")
    )
)
def log_warn_level_1():
    return "WARNING LEVEL 1"

assert log_warn_level_1() == "WARNING LEVEL 1"

config().log_level = "INFO"

assert not log_warn_level_1()