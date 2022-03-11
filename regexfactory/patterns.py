"""
Regex Pattern Classes
***********************

Module for Regex pattern classes like :code:`[^abc]` or :code:`(abc)` or :code:`a|b`
"""

from typing import Optional

from .pattern import RegexPattern, ValidPatternType


class Or(RegexPattern):
    """
    For matching multiple patterns.
    This pattern `or` that pattern `or` that other pattern.

    .. execute_code::
        :hide_headers:

        from regexfactory import Or

        patt = Or("Bob", "Alice", "Sally")

        print(patt.match("Alice"))
        print(patt.match("Bob"))
        print(patt.match("Sally"))

    """

    def __init__(
        self,
        *patterns: ValidPatternType,
    ) -> None:
        regex = "|".join(map(self.get_regex, patterns))
        super().__init__((regex))


class Range(RegexPattern):
    """
    For matching characters between two character indices (using the Unicode numbers of the input characters.)
    You can find use :func:`chr` and :func:`ord` to translate characters their Unicode numbers and back again.
    For example, :code:`chr(97)` returns the string :code:`'a'`, while :code:`chr(8364)` returns the string :code:`'€'`
    Thus, matching characters between :code:`'a'` and :code:`'z'` is really checking whether a characters unicode number 
    is between :code:`ord('a')` and :code:`ord('z')`

    .. execute_code::
        :hide_headers:

        from regexfactory import Range, Or

        patt = Or("Bob", Range("a", "z"))
        
        print(patt.findall("my job"))

    """

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
        self,
        pattern: ValidPatternType,
        i: int,
        j: Optional[int] = None,
        or_more: bool = False,
    ) -> None:
        if j is not None:
            amount = f"{i},{j}"
        elif or_more:
            amount = f"{i},"
        else:
            amount = f"{i}"

        regex = self.get_regex(pattern) + "{" + amount + "}"
        super().__init__(regex)


class Multi(RegexPattern):
    def __init__(
        self,
        pattern: ValidPatternType,
        accept_empty: bool = False,
        greedy: bool = True,
    ):
        suffix = "*" if accept_empty else "+"
        if greedy is False:
            suffix += "?"
        regex = self.get_regex(pattern)
        super().__init__(regex + suffix)


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
            Extension.__init__(self, ":", pattern)
        else:
            RegexPattern.__init__(self, pattern)  # pylint: disable=bad-super-call
