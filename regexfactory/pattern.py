"""Module for the RegexPattern class"""


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


def join(*patterns):
    joined = ''
    for pattern in patterns:
        joined += str(pattern)
    return joined


def escape(character: str):
    if character in escaped_characters:
        character = "\\" + character
    return character


class RegexPattern:
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
