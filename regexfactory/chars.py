r"""Module for common regex characters, such as `\d`, `.`, ..."""

from .patterns import RegexPattern

ANY = RegexPattern(r".")
WHITESPACE = RegexPattern(r"\s")
NOTWHITESPACE = RegexPattern(r"\S")
WORD = RegexPattern(r"\w")
NOTWORD = RegexPattern(r"\W")
DIGIT = RegexPattern(r"\d")
NOTDIGIT = RegexPattern(r"\D")
