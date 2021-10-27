from .pattern import RegexPattern
from .patterns import (
    Group,
    Or,
    Range,
    Set,
    NotSet,
    Amount,
    Optional
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


__name__ = "RegexFactory"
__version__ = "0.0.0"
__description__ = "Dynamically generate regex patterns"
__author__ = "GrandMoff100"
__author_email__ = "nlarsen23.student@gmail.com"
