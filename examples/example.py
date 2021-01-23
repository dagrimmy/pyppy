from pyppy.config import initialize_config
from pyppy.conditions import condition, exp, and_
import types

args = types.SimpleNamespace()
args.log_level = "WARN"
args.specific_log_level = "LEVEL_1"

initialize_config(args)

@condition(
    and_(
        exp(log_level="WARN"),
        exp(specific_log_level="LEVEL_1")
    )
)
def log_warn_level_1():
    print("WARNING LEVEL 1")

log_warn_level_1()