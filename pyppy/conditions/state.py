from .conditions import _Exp
from pyppy import state


class StateExp(_Exp):
    _container = state
