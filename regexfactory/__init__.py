"""The regexfactory module documetation!"""

from .chars import (
    ANY,
    DIGIT,
    NOTDIGIT,
    NOTWHITESPACE,
    NOTWORD,
    WHITESPACE,
    WORD
)
from .pattern import RegexPattern
from .patterns import Amount, Group, NotSet, Optional, Or, Range, Set

__version__ = "0.0.0"
