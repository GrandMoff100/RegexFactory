"""The module for the RegexPattern class and other functions"""


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


def join(*patterns):
    """a"""
    joined = ''
    for pattern in patterns:
        joined += str(pattern)
    return joined


def escape(character: str):
    """a"""
    if character in escaped_characters:
        character = "\\" + character
    return character


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
