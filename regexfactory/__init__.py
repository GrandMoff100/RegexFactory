"""The regexfactory module documentation!"""

from .chars import ANY, DIGIT, NOTDIGIT, NOTWHITESPACE, NOTWORD, WHITESPACE, WORD
from .pattern import RegexPattern
from .patterns import (
    Amount,
    Group,
    Lookahead,
    NegLookahead,
    NotSet,
    Optional,
    Or,
    Range,
    Reference,
    Set,
)

__version__ = "0.0.0"
