r"""Module for regex characters like `\w` or `\D` or `.`"""

from .pattern import RegexPattern, escape


class RegexChar(RegexPattern):
    regex: str = ''

    def __init__(self, character: str = None):
        if character:
            self.regex = escape(character)


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


ANY = Any()
WHITESPACE = Whitespace()
NOTWHITESPACE = NotWhitespace()
WORD = Word()
NOTWORD = NotWord()
DIGIT = Digit()
NOTDIGIT = NotDigit()
