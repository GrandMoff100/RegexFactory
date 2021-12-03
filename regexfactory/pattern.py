"""The module for the RegexPattern class and other functions"""

import re
from typing import Tuple, Union


escaped_characters = {
    "*",
    ".",
    "\r",
    "\t",
    "\n",
    "\\",
    "?",
    "+"
}
"""A set of all characters that need to be escaoed in regex."""




class RegexPattern:
    """
    The base class for constructinn patterns.
    You can add patterns together like :code:`pattern1 + pattern2`
    To turn a string into a RegexPattern object simply pass it to it's init method, like :code:`patt = RegexPattern("myregex")`.

    :ivar regex: The regular expression content for any RegexPattern object.
    """

    regex: str

    def __init__(self, pattern):
        if isinstance(pattern, RegexPattern):
            pattern = pattern.regex
        self.regex = pattern

    def __str__(self):
        return self.regex

    def __add__(self, other):
        if isinstance(other, RegexPattern):
            other = other.regex

        return RegexPattern(self.regex + other)

    def compile(self, flags=0):
        return re.compile(str(self), flags=flags)


def join(*patterns: Tuple[Union[str, RegexPattern]]) -> RegexPattern:
    """Concatenates a tuple of RegexPattern and string objects into a single RegexPattern object."""
    joined = ''
    for pattern in patterns:
        joined += str(pattern)
    return joined


def escape(character: str) -> str:
    """Escapes a regex metacharacter into a raw string character."""
    if character in escaped_characters:
        character = "\\" + character
    return character
