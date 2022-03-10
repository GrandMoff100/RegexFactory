"""
Base Pattern Module
*******************

Module for the RegexPattern class.
"""

from re import Pattern
from typing import Union

ValidPatternType = Union[Pattern, str, "RegexPattern"]

#: Special characters that need to be escaped to be used without their special meanings.
escaped_characters = {
    "*",
    "^",
    "$",
    ".",
    "\\",
    "?",
    "+",
    "|",
    "(",
    ")",
    "{",
    "}",
}


def join(*patterns: ValidPatternType) -> "RegexPattern":
    """lol"""
    joined = ""
    for pattern in patterns:
        joined += str(pattern)
    return RegexPattern(joined)


def escape(character: str) -> "RegexPattern":
    """lol"""
    if character in escaped_characters:
        character = "\\" + character
    return RegexPattern(character)


class RegexPattern:
    """An object"""

    regex: str

    def __init__(self, pattern: ValidPatternType) -> None:
        self.regex = self.get_regex(pattern)

    def __repr__(self) -> str:
        raw_regex = repr(self.regex).replace("\\\\", "\\")
        return f"<RegexPattern {raw_regex}>"

    def __str__(self) -> str:
        return self.regex

    def __add__(self, other: ValidPatternType) -> "RegexPattern":
        try:
            other = self.get_regex(other)
        except TypeError:
            return NotImplemented

        return RegexPattern(self.regex + other)

    def __mul__(self, coefficient: int) -> "RegexPattern":
        return RegexPattern(self.regex * coefficient)

    def __eq__(self, pattern: ValidPatternType) -> bool:
        return self.regex == self.get_regex(pattern)

    @staticmethod
    def get_regex(obj: ValidPatternType) -> str:
        """Extracts the regex content from RegexPattern or Pattern objects else return the input."""
        if isinstance(obj, RegexPattern):
            return obj.regex
        if isinstance(obj, str):
            return obj
        if isinstance(obj, Pattern):
            return obj.pattern
        raise TypeError(f"Can't get regex from {obj.__class__.__qualname__} object.")
