"""
API Reference
##############

The regexfactory module documentation!

.. automodule:: regexfactory.pattern

.. automodule:: regexfactory.patterns

.. automodule:: regexfactory.chars

"""

from .chars import (
    ANCHOR_END,
    ANCHOR_START,
    ANY,
    DIGIT,
    NOTDIGIT,
    NOTWHITESPACE,
    NOTWORD,
    WHITESPACE,
    WORD,
)
from .pattern import ESCAPED_CHARACTERS, RegexPattern, ValidPatternType, escape, join
from .patterns import (
    Amount,
    Comment,
    Extension,
    Group,
    IfAhead,
    IfBehind,
    IfGroup,
    IfNotAhead,
    IfNotBehind,
    Multi,
    NamedGroup,
    NamedReference,
    NumberedReference,
    Optional,
    Or,
)
from .sets import NotSet, Range, Set

__version__ = "1.0.1"
