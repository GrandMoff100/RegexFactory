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

_enable_debug: bool = False
_enable_desc: bool = False


class RegexPattern:
    """
    The main object that represents Regular Expression Pattern strings for this library.
    """

    regex: str
    _reference_regex: Optional[str] = None
    _desc: Optional[str] = None

    #: The precedence of the pattern. Higher precedence patterns are evaluated first.
    # Precedence modified from here (https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html#tag_09_04_08)

    # 3 Bracket expression []
    # 2 Grouping ()
    # 1 Single-character-ERE duplication * + ? {m,n}
    # 0 Concatenation, Anchoring ^ $
    # -2 Alternation |
    _precedence: int

    def __init__(self, regex: str, *, _precedence: int = -10) -> None:
        self.regex = regex
        self._precedence = _precedence

    @property
    def _get_ref(self):
        if self._reference_regex is not None:
            ans = self._reference_regex
        else:
            ans = self.regex
        return f"(?:{ans})"

    @property
    def _get_desc(self):
        if self._desc is not None:
            return self._desc
        return repr(self.regex)

    @staticmethod
    def from_regex_str(regex: str) -> "RegexPattern":
        """create a RegexPattern from a regex. raises ValueError if regex is invalid."""
        if regex == re.escape(regex):
            return escape(regex)

        # https://stackoverflow.com/questions/19630994/how-to-check-if-a-string-is-a-valid-regex-in-python
        try:
            re.compile(regex)
        except re.error:
            raise ValueError(f"invalid regex {regex}")
        ans = RegexPattern(regex, _precedence=-10)
        if _enable_debug:
            ans._reference_regex = regex
        if _enable_desc:
            ans._desc = f"RegexPattern.from_regex_str({regex!r})"
        return ans

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
        if self._desc is not None:
            return f"RegexPattern({self._desc}, {raw_regex}, {self._reference_regex})"
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

    def __or__(self, other: ValidPatternType):
        return or_(self, other)

    def __ror__(self, other):
        return or_(other, self)

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


def join(*patterns: ValidPatternType) -> RegexPattern:
    """Umbrella function for combining :class:`ValidPatternType`'s into a :class:`RegexPattern`."""
    from .patterns import Concat  # pylint: disable=import-outside-toplevel

    ps = [RegexPattern.create(p) for p in patterns]
    ans = Concat(*ps)
    if _enable_debug:
        ans._reference_regex = "".join(x._get_ref for x in ps)
    if _enable_desc:
        ans._desc = "+".join(x._get_desc for x in ps)
    return ans


def escape(string: str) -> RegexPattern:
    """Escapes special characters in a string to use them without their special meanings."""
    ans = _escape(string)

    if _enable_debug:
        ans._reference_regex = re.escape(string)
    if _enable_desc:
        if re.escape(string) == string:
            ans._desc = repr(string)
        else:
            ans._desc = f"escape({repr(string)})"
    return ans


def _escape(string: str) -> RegexPattern:
    if len(string) == 0:
        return RegexPattern("", _precedence=0)
    if len(string) == 1:
        from .sets import CharLiteral  # pylint: disable=import-outside-toplevel

        return CharLiteral(re.escape(string))
    return RegexPattern(re.escape(string), _precedence=0)


def or_(*args: ValidPatternType) -> RegexPattern:
    """equivalent to Set"""
    from .patterns import Or
    from .sets import NEVER, Set, _is_charset

    args_rx = [RegexPattern.create(x) for x in args]

    if len(args_rx) == 1:
        ans = args_rx[0]
    else:
        all_cs = all(map(_is_charset, args_rx))

        if all_cs:
            ans = Set(*args_rx)  # type: ignore
        else:
            ans = Or(*args_rx)

    if _enable_debug:
        if len(args_rx) > 0:
            ans._reference_regex = "|".join(x._get_ref for x in args_rx)
        else:
            ans._reference_regex = NEVER.regex
    if _enable_desc:
        desc = ",".join(x._get_desc for x in args_rx)
        ans._desc = f"or_({desc})"
    return ans


def amount(
    pattern: ValidPatternType,
    i: int,
    j: Optional[int] = None,
    or_more: bool = False,
    greedy: bool = True,
) -> RegexPattern:

    from .patterns import Amount

    pt = RegexPattern.create(pattern)

    ans = _amount(pt, i, j, or_more, greedy)
    if _enable_debug:
        ans._reference_regex = Amount(
            RegexPattern(pt._get_ref, _precedence=2).regex, i, j, or_more, greedy
        ).regex
    if _enable_desc:
        pieces = [pt._get_desc, str(i)]
        if j is not None:
            pieces.append(str(j))
        if or_more:
            pieces.append("or_more=True")
        if not greedy:
            pieces.append("greedy=False")
        ans._desc = f"Amount({','.join(pieces)})"
    return ans


def _amount(
    pattern: RegexPattern, i: int, j: Optional[int], or_more: bool, greedy: bool
) -> RegexPattern:
    from .patterns import Amount, Multi, Optional

    if i == 1 and j == 1:
        return pattern

    if i == 0 and j == 1:
        return Optional(pattern, greedy)

    if i == 0 and j is None and or_more:
        return Multi(pattern, True, greedy)

    if i == 1 and j is None and or_more:
        return Multi(pattern, False, greedy)

    return Amount(pattern, i, j, or_more, greedy)


def multi(
    pattern: ValidPatternType,
    match_zero: bool = False,
    greedy: bool = True,
):
    if match_zero:
        return amount(pattern, 0, or_more=True, greedy=greedy)
    return amount(pattern, 1, or_more=True, greedy=greedy)


def optional(pattern: ValidPatternType, greedy: bool = True):
    return amount(pattern, 0, 1, greedy=greedy)
