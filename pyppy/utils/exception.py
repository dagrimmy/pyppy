"""
Contains exceptions for pyppy.
"""


class AlreadyInitializedException(Exception):
    """
    Exception indicating that a global config_ has already
    been initialized.
    """


class MissingConfigParamException(Exception):
    """
    MissingConfigParamException
    """


class ConditionRaisedException(Exception):
    """
    ConditionRaisedException
    """


class ConditionDidNotReturnBooleansException(Exception):
    """
    ConditionDidNotReturnBooleansException
    """


class FunctionSignatureNotSupportedException(Exception):
    """
    FunctionSignatureNotSupportedException
    """


class OnlyKeywordArgumentsAllowedException(Exception):
    """
    OnlyKeywordArgumentsAllowedException
    """


class IllegalStateException(Exception):
    """
    IllegalStateException
    """


class UnexpectedNumberOfReturnsException(Exception):
    """
    Exception indicating that a global config_ has already
    been initialized.
    """