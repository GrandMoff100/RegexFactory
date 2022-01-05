"""Module for Regex pattern classes like `[^abc]` or (abc) a|b"""

import inspect
import typing as t
from typing import overload

from .pattern import RegexPattern, ValidPatternType


class Group(RegexPattern):
    def __init__(self, pattern: ValidPatternType) -> None:
        regex = self.get_regex(pattern)
        super().__init__(f"({regex})")


class Or(RegexPattern):
    def __init__(
        self, pattern: ValidPatternType, other_pattern: ValidPatternType
    ) -> None:
        regex = self.get_regex(pattern) + "|" + self.get_regex(other_pattern)
        super().__init__(Group(regex))


class Range(RegexPattern):
    def __init__(self, start: str, stop: str) -> None:
        self.start = start
        self.stop = stop
        regex = f"[{start}-{stop}]"
        super().__init__(regex)


class Set(RegexPattern):
    def __init__(self, *patterns: ValidPatternType) -> None:
        regex = ""
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.start}-{p.stop}"
            else:
                regex += str(p)
        super().__init__(f"[{regex}]")


class NotSet(RegexPattern):
    def __init__(self, *patterns: ValidPatternType) -> None:
        regex = ""
        for p in patterns:
            if isinstance(p, Range):
                regex += f"{p.start}-{p.stop}"
            else:
                regex += str(p)
        super().__init__(f"[^{regex}]")


class Amount(RegexPattern):
    @overload
    def __init__(
        self, pattern: ValidPatternType, repetitions: int, or_more: bool = False
    ) -> None:
        ...

    @overload
    def __init__(self, pattern: ValidPatternType, minimum: int, maximum: int) -> None:
        ...

    def __init__(self, pattern: ValidPatternType, *args, **kwargs) -> None:
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
                inspect.Parameter(
                    "repetitions", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
                ),
                inspect.Parameter(
                    "or_more",
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    default=False,
                ),
            )
        )
        s2 = inspect.Signature(
            parameters=(
                inspect.Parameter(
                    "minimum", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
                ),
                inspect.Parameter(
                    "maximum", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
                ),
            )
        )
        try:
            bound = s1.bind(*args, **kwargs)
            bound.apply_defaults()
            i = bound.arguments["repetitions"]
            j = None
            or_more = bound.arguments["or_more"]
        except TypeError:
            bound = s2.bind(*args, **kwargs)
            bound.apply_defaults()
            i = bound.arguments["minimum"]
            j = bound.arguments["maximum"]
            or_more = False

        return i, j, or_more


class Optional(RegexPattern):
    def __init__(self, pattern: ValidPatternType) -> None:
        regex = self.get_regex(pattern) + "?"
        super().__init__(regex)


class Extension(RegexPattern):
    def __init__(self, pre: str, pattern: ValidPatternType):
        super().__init__(f"(?{pre}{str(pattern)})")


class NamedGroup(Extension):
    def __init__(self, name: str, pattern: ValidPatternType):
        super().__init__(f"P<{name}>", pattern)


class Reference(Extension):
    def __init__(self, name: str):
        super().__init__("P=", name)


class Comment(Extension):
    def __init__(self, content: str):
        super().__init__("#", content)


class Lookahead(Extension):
    def __init__(self, pattern: ValidPatternType):
        super().__init__("=", pattern)


class NegLookahead(Extension):
    def __init__(self, pattern: ValidPatternType):
        super().__init__("!", pattern)
