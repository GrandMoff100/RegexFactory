"""
Base Pattern Module
*******************

Module for the :class:`RegexPattern` class.
"""

# pylint: disable=cyclic-import

import re
import sys
from typing import Any, Iterator, List, Optional, Tuple, Union

#:
ValidPatternType = Union[re.Pattern, str, "RegexPattern"]

#: Special characters that need to be escaped to be used without their special meanings.
ESCAPED_CHARACTERS = "()[]{}?*+-|^$\\.&~#"


def join(*patterns: ValidPatternType) -> "RegexPattern":
    """Umbrella function for combining :class:`ValidPatternType`'s into a :class:`RegexPattern`."""
    from .patterns import Concat  # pylint: disable=import-outside-toplevel

    return Concat(*patterns)


def escape(string: str) -> "RegexPattern":
    """Escapes special characters in a string to use them without their special meanings."""

    if len(string) == 0:
        return RegexPattern("", _precedence=0)
    if len(string) == 1:
        return RegexPattern(re.escape(string), _precedence=10)
    return RegexPattern(re.escape(string), _precedence=0)


class RegexPattern:
    """
    The main object that represents Regular Expression Pattern strings for this library.
    """

    regex: str

    #: The precedence of the pattern. Higher precedence patterns are evaluated first.
    # Precedence order here (https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html#tag_09_04_08)

    # 5 Collation-related bracket symbols [==] [::] [..]
    # 4 Escaped characters \<special character>
    # 3 Bracket expression []
    # 2 Grouping ()
    # 1 Single-character-ERE duplication * + ? {m,n}
    # 0 Concatenation
    # -1 Anchoring ^ $
    # -2 Alternation |

    def __init__(self, regex: str, *, _precedence: int = -10) -> None:
        self.regex = regex
        self._precedence = _precedence

    @staticmethod
    def from_regex_str(regex: str) -> "RegexPattern":
        # if regex is self escaping, then it just matches a literal string
        if regex == re.escape(regex):
            if len(regex) == 0:
                return RegexPattern("", _precedence=0)
            if len(regex) == 1:
                return RegexPattern(regex, _precedence=10)
            return RegexPattern(regex, _precedence=0)

        # https://stackoverflow.com/questions/19630994/how-to-check-if-a-string-is-a-valid-regex-in-python
        try:
            re.compile(regex)
        except re.error:
            raise ValueError(f"invalid regex {regex}")
        return RegexPattern(regex, _precedence=-10)

    @staticmethod
    def create(obj: ValidPatternType) -> "RegexPattern":
        if isinstance(obj, RegexPattern):
            return obj
        if isinstance(obj, str):
            return RegexPattern.from_regex_str(obj)
        if isinstance(obj, re.Pattern):
            return RegexPattern.from_regex_str(obj.pattern)
        raise TypeError(f"Can't get regex from {obj.__class__.__qualname__} object.")

    @staticmethod
    def _ensure_precedence(
        pattern: ValidPatternType, precedence: int
    ) -> "RegexPattern":
        from .patterns import Group  # pylint: disable=import-outside-toplevel

        p = RegexPattern.create(pattern)

        if p._precedence >= precedence:
            return p

        assert precedence <= 2
        return Group(pattern, capturing=False)

    @staticmethod
    def _ensure_precedence_fn(precedence: int):
        def inner(pattern: ValidPatternType):
            return RegexPattern._ensure_precedence(pattern, precedence).regex

        return inner

    def __repr__(self) -> str:
        raw_regex = f"{self.regex!r}".replace("\\\\", "\\")
        return f"<RegexPattern {raw_regex}>"

    def __str__(self) -> str:
        return self.regex

    def __add__(self, other: ValidPatternType) -> "RegexPattern":
        """Adds two :class:`ValidPatternType`'s together, into a :class:`RegexPattern`"""
        return join(self, other)

    def __radd__(self, other: ValidPatternType) -> "RegexPattern":
        """Adds two :class:`ValidPatternType`'s together, into a :class:`RegexPattern`"""
        return join(other, self)

    def __mul__(self, coefficient: int) -> "RegexPattern":
        """matches exactly coefficient counts of self"""
        from .patterns import Amount

        return Amount(self, coefficient)

    def __or__(self, other) -> "RegexPattern":
        """matches exactly coefficient counts of self"""
        from .sets import Set

        return Set(self, other)  # type: ignore

    def __eq__(self, other: Any) -> bool:
        """
        Returns whether or not two :class:`ValidPatternType`'s have the same regex.
        Otherwise return false.
        """
        if isinstance(other, (str, re.Pattern, RegexPattern)):
            return self.regex == self.create(other).regex
        return super().__eq__(other)

    def __hash__(self) -> int:
        """Hashes the regex string."""
        return hash(self.regex)

    def compile(
        self,
        *,
        flags: int = 0,
    ) -> re.Pattern:
        """See :func:`re.compile`."""
        return re.compile(self.regex, flags=flags)

    def match(
        self,
        content: str,
        /,
        *,
        flags: int = 0,
    ) -> Optional[re.Match]:
        """See :meth:`re.Pattern.match`."""
        return self.compile(flags=flags).match(content)

    def fullmatch(
        self,
        content: str,
        /,
        *,
        flags: int = 0,
    ) -> Optional[re.Match]:
        """See :meth:`re.Pattern.fullmatch`."""
        return self.compile(flags=flags).fullmatch(content)

    def findall(
        self,
        content: str,
        /,
        *,
        flags: int = 0,
    ) -> List[Tuple[str, ...]]:
        """See :meth:`re.Pattern.findall`."""
        return self.compile(flags=flags).findall(content)

    def finditer(
        self,
        content: str,
        /,
        *,
        flags: int = 0,
    ) -> Iterator[re.Match]:
        """See :meth:`re.Pattern.finditer`."""
        return self.compile(flags=flags).finditer(content)

    def split(
        self,
        content: str,
        /,
        maxsplit: int = 0,
        *,
        flags: int = 0,
    ) -> List[Any]:
        """See :meth:`re.Pattern.split`."""
        return self.compile(flags=flags).split(content, maxsplit=maxsplit)

    def sub(
        self,
        replacement: str,
        content: str,
        /,
        count: int = 0,
        *,
        flags: int = 0,
    ) -> str:
        """See :meth:`re.Pattern.sub`."""
        return self.compile(flags=flags).sub(replacement, content, count=count)

    def subn(
        self,
        replacement: str,
        content: str,
        /,
        count: int = 0,
        *,
        flags: int = 0,
    ) -> Tuple[str, int]:
        """See :meth:`re.Pattern.subn`."""
        return self.compile(flags=flags).subn(replacement, content, count=count)

    def search(
        self,
        content: str,
        /,
        pos: int = 0,
        endpos: int = sys.maxsize,
        *,
        flags: int = 0,
    ) -> Optional[re.Match]:
        """See :meth:`re.Pattern.search`."""
        return self.compile(flags=flags).search(content, pos, endpos)
