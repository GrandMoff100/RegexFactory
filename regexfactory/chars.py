r"""Module for regex characters like `\w` or `\D` or `.`"""

from .pattern import RegexPattern


class RegexChar(RegexPattern):
    regex: str = ''


class Whitespace(RegexChar):
    regex = r'\s'


class NotWhitespace(RegexChar):
    regex = r'\S'


class Any(RegexChar):
    regex = r'.'


class Word(RegexChar):
    regex = r'\w'


class NotWord(RegexChar):
    regex = r'\W'


class Digit(RegexChar):
    regex = r'\d'


class NotDigit(RegexChar):
    regex = r'\D'
