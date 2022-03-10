"""Module for Regex pattern classes like `[^abc]` or (abc) a|b"""

"""

from .pattern import RegexPattern, ValidPatternType


class Or(RegexPattern):
    def __init__(
        self,
        *patterns: ValidPatternType,
    ) -> None:
        regex = "|".join(map(self.get_regex, patterns))
        super().__init__((regex))


class Range(RegexPattern):
    def __init__(self, start: str, stop: str) -> None:
        self.start = start
        self.stop = stop
        regex = f"[{start}-{stop}]"
        super().__init__(regex)


class Set(RegexPattern):
    def __init__(self, *patterns: ValidPatternType) -> None:
        regex = ""
        for pattern in patterns:
            if isinstance(pattern, Range):
                regex += f"{pattern.start}-{pattern.stop}"
            else:
                regex += self.get_regex(pattern)
        super().__init__(f"[{regex}]")


class NotSet(RegexPattern):
    def __init__(self, *patterns: ValidPatternType) -> None:
        regex = ""
        for pattern in patterns:
            if isinstance(pattern, Range):
                regex += f"{pattern.start}-{pattern.stop}"
            else:
                regex += self.get_regex(pattern)
        super().__init__(f"[^{regex}]")


class Amount(RegexPattern):
    def __init__(
        self, pattern: ValidPatternType, i: int, *args: int, or_more: bool = False
    ) -> None:
        j, *_ = args + (None,)

        if j is not None:
            amount = f"{i},{j}"
        elif or_more:
            amount = f"{i},"
        else:
            amount = f"{i}"

        regex = self.get_regex(pattern) + "{" + amount + "}"
        super().__init__(regex)


class Optional(RegexPattern):
    def __init__(self, pattern: ValidPatternType) -> None:
        regex = self.get_regex(pattern) + "?"
        super().__init__(regex)


class Extension(RegexPattern):
    def __init__(self, prefix: str, pattern: ValidPatternType):
        regex = self.get_regex(pattern)
        super().__init__(f"(?{prefix}{regex})")


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


class Group(Extension):
    def __init__(self, pattern: ValidPatternType, capture: bool = True) -> None:
        if capture is False:
            super().__init__(":", pattern)
        else:
            super(Extension, self).__init__(pattern)  # pylint: disable=bad-super-call
