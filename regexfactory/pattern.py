"""Module for the RegexPattern class"""

import dataclasses
from typing import Union


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

    @staticmethod
    def join(*patterns):
        joined = ''
        for pattern in patterns:
            joined += str(pattern)
        return joined
