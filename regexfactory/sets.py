import itertools
import re
import typing as t

from regexfactory import pattern as p
from regexfactory.pattern import RegexPattern
from regexfactory.patterns import IfNotAhead

CharSet = t.Union[str, "Set", "CharLiteral", "CharClass", "Range"]

ALWAYS = RegexPattern.from_regex_str("")
ALWAYS._desc = "ALWAYS"
NEVER = IfNotAhead(ALWAYS)
NEVER._desc = "NEVER"


def _is_charset(c: RegexPattern) -> t.TypeGuard[CharSet]:
    return isinstance(c, (Set, CharLiteral, CharClass, Range))


def _charset_normalize(c: CharSet) -> list[str]:
    if isinstance(c, str):
        return [re.escape(x) for x in c]
    if isinstance(c, Range):
        return [c._regex_inner]
    if isinstance(c, Set):
        return c.members
    if isinstance(c, CharLiteral):
        return [c.regex]
    if isinstance(c, CharClass):
        return [c.regex]

    raise TypeError(f"invalid charset: {c!r}")


class CharLiteral(RegexPattern):
    """
    matches a single char literal like "A"
    """

    def __init__(self, c: str, _precedence=10):
        super().__init__(c, _precedence=_precedence)


class CharClass(RegexPattern):
    """
    base class for patterns that matches exactly one from a set of characters,
    for example DIGIT or WORD
    """

    def __init__(self, c: str, _precedence=10):
        super().__init__(c, _precedence=_precedence)


class Range(RegexPattern):
    """
    For matching characters between two character indices
    (using the Unicode numbers of the input characters.)
    You can find use :func:`chr` and :func:`ord`
    to translate characters their Unicode numbers and back again.
    For example, :code:`chr(97)` returns the string :code:`'a'`,
    while :code:`chr(8364)` returns the string :code:`'€'`
    Thus, matching characters between :code:`'a'` and :code:`'z'`
    is really checking whether a characters unicode number
    is between :code:`ord('a')` and :code:`ord('z')`

    .. exec_code::

        from regexfactory import Range, Or

        patt = Or("Bob", Range("a", "z"))

        print(patt.findall("my job is working for Bob"))

    """

    def __init__(self, start: str, stop: str) -> None:
        if len(start) != 1:
            raise ValueError(f"invalid start: {start!r}")
        if len(stop) != 1:
            raise ValueError(f"invalid stop: {stop!r}")
        if ord(stop) < ord(start):
            raise ValueError(f"invalid range: {start!r} to {stop!r}")

        self.start = start
        self.stop = stop

        self._regex_inner = f"{re.escape(start)}-{re.escape(stop)}"
        super().__init__(f"[{self._regex_inner}]", _precedence=3)


class Set(RegexPattern):
    """
    For matching a single character from a list of characters.
    Keep in mind special characters like :code:`+` and :code:`.`
    lose their meanings inside a set/list,
    so need to escape them here to use them.

    In practice, :code:`Set("a", ".", "z")`
    functions the same as :code:`Or("a", ".", "z")`
    The difference being that :class:`Or` accepts :class:`RegexPattern` 's
    and :class:`Set` accepts characters only.
    Special characters do **NOT** lose their special meaings inside an :class:`Or` though.
    The other big difference is performance,
    :class:`Or` is a lot slower than :class:`Set`.

    .. exec_code::

        import time
        from regexfactory import Or, Set

        start_set = time.time()
        print(patt := Set(*"a.z").compile())
        print("Set took", time.time() - start_set, "seconds to compile")
        print("And the resulting match is", patt.match("b"))

        print()

        start_or = time.time()
        print(patt := Or(*"a.z").compile())
        print("Or took", time.time() - start_or, "seconds to compile")
        print("And the resulting match is", patt.match("b"))

    """

    members: list[str] = []

    def __init__(self, *charsets: CharSet) -> None:
        self.members = list(
            itertools.chain(*(_charset_normalize(arg) for arg in charsets))
        )
        if len(self.members) == 0:
            regex = NEVER.regex
            prec = NEVER._precedence
        else:
            regex = "[" + "".join(self.members) + "]"
            prec = 3

        super().__init__(regex, _precedence=prec)


class NotSet(RegexPattern):
    """
    For matching a character that is **NOT** in a list of characters.
    Keep in mind special characters lose their special meanings inside :class:`NotSet`'s as well.

    .. exec_code::

        from regexfactory import NotSet, Set

        not_abc = NotSet(*"abc")

        is_abc = Set(*"abc")

        print(not_abc.match("x"))
        print(is_abc.match("x"))

    """

    members: list[str] = []

    def __init__(self, *charsets: CharSet):
        self.members = list(
            itertools.chain(*(_charset_normalize(arg) for arg in charsets))
        )
        if len(self.members) == 0:
            from .chars import NOTWHITESPACE, WHITESPACE

            regex = (WHITESPACE | NOTWHITESPACE).regex
            prec = 3
        else:
            regex = "[^" + "".join(self.members) + "]"
            prec = 3

        super().__init__(regex, _precedence=prec)
