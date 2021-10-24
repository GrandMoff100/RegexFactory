"""Module for Regex pattern classes like `[^abc]` or (abc) a|b"""

from .pattern import RegexPattern, join
from typing import Tuple, Union


class Group(RegexPattern):
    def __init__(self, pattern: Union[str, RegexPattern]):
        super().__init__("(" + str(pattern) + ")")


class AnyOf(RegexPattern):
    def __init__(
        self,
        *characters: Tuple[Union[str, RegexPattern]]
    ):
        self.characters = join(characters)
        regex = "[" + self.characters + "]"
        super().__init__(regex)


class NotAnyOf(RegexPattern):
    def __init__(
        self,
        *characters: Tuple[Union[str, RegexPattern]]
    ):
        self.characters = RegexPattern.join(characters)
        regex = "[^" + self.characters + "]"
        super().__init__(regex)


class Or(RegexPattern):
    def __init__(
        self,
        pattern: Union[str, RegexPattern],
        other_pattern: Union[str, RegexPattern]
    ):
        regex = str(pattern) + "|" + str(other_pattern)
        super().__init__(Group(regex))
