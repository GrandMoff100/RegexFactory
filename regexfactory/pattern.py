"""Module for the RegexPattern class"""

from re import Pattern
from typing import Union

ValidPatternType = Union[Pattern, str, "RegexPattern"]
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


def join(*patterns: ValidPatternType) -> str:
    joined = ''
    for pattern in patterns:
        joined += str(pattern)
    return joined


def escape(character: str) -> str:
    if character in escaped_characters:
        character = "\\" + character
    return character


class RegexPattern:
    regex: str

    def __init__(self, pattern: ValidPatternType):
        self.regex = self.get_regex(pattern)

    @staticmethod
    def get_regex(obj: ValidPatternType) -> str:
        if isinstance(obj, RegexPattern):
            return obj.regex
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, Pattern):
            return obj.pattern

        raise TypeError(f"Can't get regex from {obj.__class__.__qualname__} object.")

    def __str__(self):
        return self.regex

    def __add__(self, other: ValidPatternType) -> "RegexPattern":
        try:
            other = self.get_regex(other)
        except TypeError:
            return NotImplemented

        return RegexPattern(self.regex + other)