"""Module for Regex pattern classes like `[^abc]` or (abc) a|b"""

from .pattern import RegexPattern
from typing import Tuple, Union


class Group(RegexPattern):
    def __init__(self, pattern: Union[str, RegexPattern]):
        super().__init__("(" + str(pattern) + ")")


class Or(RegexPattern):
    def __init__(
        self,
        pattern: Union[str, RegexPattern],
        other_pattern: Union[str, RegexPattern]
    ):
        regex = str(pattern) + "|" + str(other_pattern)
        super().__init__(Group(regex))


class Range(RegexPattern):
    def __init__(self, a: str, z: str):
        self.a = a
        self.z = z
        regex = f"[{a}-{z}]"
        super().__init__(regex)


class Set(RegexPattern):
    def __init__(self, *patterns: Tuple[Union[str, Range]]):
        regex = ''
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.a}-{p.z}"
            else:
                regex += str(p)
        super().__init__(f"[{regex}]")


class NotSet(RegexPattern):
    def __init__(self, *patterns: Tuple[Union[str, Range]]):
        regex = ''
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.a}-{p.z}"
            else:
                regex += str(p)
        super().__init__(f"[^{regex}]")


class Amount(RegexPattern):
    def __init__(
        self,
        pattern: Union[str, RegexPattern],
        i: int,
        j: int = None,
        ormore: bool = False
    ):
        if j is not None:
            amount = f"{i},{j}"
        elif ormore:
            amount = f"{i},"
        else:
            amount = f"{i}"
        super().__init__(pattern + "{" + amount + "}")


class Optional(RegexPattern):
    def __init__(self, pattern: Union[str, RegexPattern]):
        super().__init__(pattern + "?")
