"""Module for Regex pattern classes like `[^abc]` or (abc) a|b"""

from .pattern import RegexPattern, ValidPatternType
import typing as t
from typing import overload
import inspect


class Group(RegexPattern):
    def __init__(self, pattern: ValidPatternType):
        regex = self.get_regex(pattern)
        super().__init__(regex)


class Or(RegexPattern):
    def __init__(self, pattern: ValidPatternType, other_pattern: ValidPatternType):
        regex = self.get_regex(pattern) + "|" + self.get_regex(other_pattern)
        super().__init__(Group(regex))


class Range(RegexPattern):
    def __init__(self, start: str, stop: str):
        self.start = start
        self.stop = stop
        regex = f"[{start}-{stop}]"
        super().__init__(regex)


class Set(RegexPattern):
    def __init__(self, *patterns: ValidPatternType):
        regex = ''
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.start}-{p.stop}"
            else:
                regex += str(p)
        super().__init__(f"[{regex}]")


class NotSet(RegexPattern):
    def __init__(self, *patterns: ValidPatternType):
        regex = ''
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.start}-{p.stop}"
            else:
                regex += str(p)
        super().__init__(f"[^{regex}]")


class Amount(RegexPattern):
    @overload
    def __init__(self, pattern: ValidPatternType, repetitions: int, or_more: bool = False):
        ...

    @overload
    def __init__(self, pattern: ValidPatternType, minimum: int, maximum: int):
        ...

    def __init__(self, pattern: ValidPatternType, *args, **kwargs):
        i, j, or_more = self.parse_init_args(*args, **kwargs)

        if j is not None:
            amount = f"{i},{j}"
        elif or_more:
            amount = f"{i},"
        else:
            amount = f"{i}"

        regex = self.get_regex(pattern) + "{" + amount + "}"
        super().__init__(regex)

    @staticmethod
    def parse_init_args(*args, **kwargs) -> t.Tuple[int, t.Optional[int], bool]:
        s1 = inspect.Signature(
            parameters=(
                inspect.Parameter("repetitions", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter("or_more", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)
            )
        )
        s2 = inspect.Signature(
            parameters=(
                inspect.Parameter("minimum", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter("maximum", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)
            )
        )
        try:
            bound = s1.bind(*args, **kwargs)
            i = bound.arguments["repetitions"]
            j = None
            or_more = bound.arguments["or_more"]
        except TypeError:
            bound = s2.bind(*args, **kwargs)
            i = bound.arguments["minimum"]
            j = bound.arguments["maximum"]
            or_more = False

        return i, j, or_more


class Optional(RegexPattern):
    def __init__(self, pattern: ValidPatternType):
        regex = self.get_regex(pattern) + "?"
        super().__init__(regex)
