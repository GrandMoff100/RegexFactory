"""The regexfactory module documetation!"""

from .pattern import RegexPattern
from .patterns import (
    Group,
    Or,
    Range,
    Set,
    NotSet,
    Amount,
    Optional,
)
from .chars import (
    ANY,
    WHITESPACE,
    NOTWHITESPACE,
    WORD,
    NOTWORD,
    DIGIT,
    NOTDIGIT
)


__version__ = "0.0.0"
