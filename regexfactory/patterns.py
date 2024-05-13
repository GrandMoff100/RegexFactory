"""
Regex Pattern Subclasses
************************

Module for Regex pattern classes like :code:`[^abc]` or :code:`(abc)` or :code:`a|b`

"""

import typing as t

from regexfactory.pattern import RegexPattern, ValidPatternType


class Concat(RegexPattern):
    def __init__(self, *patterns: ValidPatternType) -> None:
        super().__init__(
            "".join(map(self._ensure_precedence_fn(0), patterns)),
            _precedence=0,
        )


class Or(RegexPattern):
    """
    For matching multiple patterns.
    This pattern `or` that pattern `or` that other pattern.

    .. exec_code::

        from regexfactory import Or

        patt = Or("Bob", "Alice", "Sally")

        print(patt.match("Alice"))
        print(patt.match("Bob"))
        print(patt.match("Sally"))

    """

    def __init__(self, *patterns: ValidPatternType) -> None:
        super().__init__(
            "|".join(map(self._ensure_precedence_fn(-2), patterns)), _precedence=-2
        )


class Amount(RegexPattern):
    """
    For matching multiple occurences of a :class:`ValidPatternType`.
    You can match a specific amount of occurences only.
    You can match with a lower bound on the number of occurences of a pattern.
    Or with a lower and upper bound on the number occurences.
    You can also pass a :code:`greedy=False` keyword-argument  to :class:`Amount`,
    (default is True)
    which tells the regex compiler match as few characters as possible rather than
    the default behavior which is to match as many characters as possible.

    Best explained with an example.

    .. exec_code::

        from regexfactory import Amount, Set

        # We are using the same Pattern with different amounts.

        content = "acbccbaabbccaaca"

        specific_amount = Amount(Set(*"abc"), 2)

        lower_and_upper_bound = Amount(Set(*"abc"), 3, 5, greedy=False)

        lower_and_upper_bound_greedy = Amount(Set(*"abc"), 3, 5)

        lower_bound_only = Amount(Set(*"abc"), 5, or_more=True, greedy=False)

        print(specific_amount.findall(content))
        print(lower_and_upper_bound_greedy.findall(content))
        print(lower_and_upper_bound.findall(content))
        print(lower_bound_only.findall(content))

    """

    def __init__(
        self,
        pattern: ValidPatternType,
        i: int,
        j: t.Optional[int] = None,
        or_more: bool = False,
        greedy: bool = True,
    ) -> None:
        if j is not None:
            assert not or_more
            amount = f"{i},{j}"
        elif or_more:
            amount = f"{i},"
        else:
            amount = f"{i}"
        regex = (
            # TODO: should this be 1?
            self._ensure_precedence(pattern, 2).regex
            + "{"
            + amount
            + "}"
            + ("" if greedy else "?")
        )
        super().__init__(regex, _precedence=1)


class Multi(RegexPattern):
    """
    Matches one or more occurences of the given :class:`ValidPatternType`.
    If given :code:`match_zero=True` to the init method it matches zero or more occurences.
    """

    def __init__(
        self,
        pattern: ValidPatternType,
        match_zero: bool = False,
        greedy: bool = True,
    ):
        suffix = "*" if match_zero else "+"
        if greedy is False:
            suffix += "?"
        # TODO: should this be 1?
        regex = self._ensure_precedence(pattern, 2).regex
        super().__init__(regex + suffix, _precedence=1)


class Optional(RegexPattern):
    """
    Matches the passed :class:`ValidPatternType` between zero and one times.
    Functions the same as :code:`Amount(pattern, 0, 1)`.
    """

    def __init__(self, pattern: ValidPatternType, greedy: bool = True):
        regex = (
            self._ensure_precedence(pattern, 2).regex + "?" + ("" if greedy else "?")
        )
        super().__init__(regex, _precedence=1)


class Extension(RegexPattern):
    """Base class for extension pattern classes."""

    def __init__(self, prefix: str, pattern: ValidPatternType):
        regex = self.create(pattern).regex
        super().__init__(f"(?{prefix}{regex})", _precedence=2)


class NamedGroup(Extension):
    """
    Lets you sepparate your regex into named groups that you can extract from :meth:`re.Match.groupdict`.

    .. exec_code::

        from regexfactory import NamedGroup, WORD, Multi

        stuff = "George Washington"

        patt = NamedGroup("first_name", Multi(WORD)) + " " + NamedGroup("last_name", Multi(WORD))

        print(match := patt.match(stuff))
        print(match.groupdict())

    """

    def __init__(self, name: str, pattern: ValidPatternType):
        self.name = name
        super().__init__(f"P<{self.name}>", pattern)


class NamedReference(Extension):
    """
    Lets you reference :class:`NamedGroup`'s that you've already created, by name, or by passing the :class:`NamedGroup` itself.

    .. exec_code::

        from regexfactory import NamedReference, NamedGroup, DIGIT, RegexPattern

        timestamp = NamedGroup("time_at", f"{DIGIT * 2}:{DIGIT * 2}am")

        patt = RegexPattern(f"Created at {timestamp}, and then updated at {NamedReference(timestamp)}")
        patt2 = RegexPattern(f"Created at {timestamp}, and then updated at {NamedReference('time_at')}")
        print(repr(patt))
        print(repr(patt2))
    """

    def __init__(self, group_name: t.Union[str, NamedGroup]):
        if isinstance(group_name, NamedGroup):
            name = group_name.name
        else:
            name = group_name
        super().__init__("P=", name)


class NumberedReference(RegexPattern):
    """
    Lets you reference the literal match to :class:`Group`'s that you've already created, by its group index.

    .. exec_code::

        from regexfactory import NumberedReference, Group, DIGIT, RegexPattern

        timestamp = Group(f"{DIGIT * 2}:{DIGIT * 2}am")

        patt = RegexPattern(f"{timestamp},{NumberedReference(1)},{NumberedReference(1)}")
        print(patt.match("09:59am,09:59am,09:59am"))
        print(patt.match("09:59am,13:00am,09:50am"))

    """

    def __init__(self, group_number: int):
        super().__init__(f"\\{group_number}")


class Comment(Extension):
    """
    Lets you include comment strings that are ignored by regex compilers to document your regex's.

    .. exec_code::

        from regexfactory import Comment, DIGIT, WORD, Or

        patt = Or(DIGIT, WORD)
        patt_with_comment = patt + Comment("I love comments in regex!")

        print("Pattern without comment:", patt)
        print("Pattern with comment", patt_with_comment)
        print(patt.match("1"))
        print(patt.match("a"))

    """

    def __init__(self, content: str):
        super().__init__("#", content)


class IfAhead(Extension):
    """
    A mini if-statement in regex.
    It does not consume any string content.
    Makes the whole pattern match only if followed by the given pattern
    at this position in the whole pattern.

    .. exec_code::

        from regexfactory import IfAhead, escape, WORD, Multi, Or

        name = Multi(WORD) + IfAhead(
            Or(
                escape(" Jr."),
                escape(" Sr."),
            )
        )

        print(name.findall("Bob Jr. and John Sr. love hanging out with each other."))

    """

    def __init__(self, pattern: ValidPatternType):
        super().__init__("=", pattern)


class IfNotAhead(Extension):
    """
    A mini if-statement in regex.
    It does not consume any string content.
    Makes the whole pattern match only if **NOT** followed by the given pattern
    at this position in the whole pattern.

    .. exec_code::

        from regexfactory import IfNotAhead, RegexPattern

        patt = RegexPattern("Foo") + IfNotAhead("bar")

        print(patt.match("Foo"))
        print(patt.match("Foobar"))
        print(patt.match("Fooba"))

    """

    def __init__(self, pattern: ValidPatternType):
        super().__init__("!", pattern)


class IfBehind(Extension):
    """
    A mini if-statement in regex.
    It does not consume any string content.
    Makes the whole pattern match only if preceded by the given pattern
    at this position in the whole pattern.

    .. exec_code::

        from regexfactory import IfBehind, DIGIT, Multi, Optional

        rank = IfBehind("Rank: ") + Multi(DIGIT)

        print(rank.findall("Rank: 27, Score: 30, Power: 123"))

    """

    def __init__(self, pattern: ValidPatternType):
        super().__init__("<=", pattern)


class IfNotBehind(Extension):
    """
    A mini if-statement in regex.
    It does not consume any string content.
    Makes the whole pattern match only if **NOT** preceded by the given pattern
    at this position in the whole pattern.

    .. exec_code::

        from regexfactory import IfNotBehind, WORD, Multi, DIGIT

        patt = IfNotBehind(WORD) + Multi(DIGIT)

        print(patt.match("b64"))
        print(patt.match("64"))

    """

    def __init__(self, pattern: ValidPatternType):
        super().__init__("<!", pattern)


class Group(Extension):
    """
    For separating your Patterns into fields for extraction.
    Basically you use Group to reference regex inside of it later with :class:`NumberedReference`.
    Passing :code:`capturing=False` unifies the regex inside the group into a single token
    but does not capture the group. Seen below.

    .. exec_code::

        from regexfactory import Group, WORD, Multi

        name = Group(Multi(WORD)) + " " + Group(Multi(WORD), capturing=False)

        print(name.match("Nate Larsen").groups())

    """

    def __init__(self, pattern: ValidPatternType, capturing: bool = True) -> None:
        if capturing is False:
            Extension.__init__(self, ":", pattern)
        else:
            RegexPattern.__init__(  # pylint: disable=non-parent-init-called
                self,
                f"({pattern})",
                _precedence=2,
            )


class IfGroup(Extension):
    """
    Matches with :code:`yes_pattern` if the given group name or group index succeeds in matching and exists,
    otherwise matches with :code:`no_pattern`

    .. exec_code::

        from regexfactory import IfGroup, NamedGroup, Optional, escape

        patt = (
            Optional(NamedGroup("title", escape("Mr. "))) +
            IfGroup("title", "Dillon", NamedGroup("first_name", "Bob")) +
            Optional(IfGroup("first_name", " Dillon", ""))
        )
        # If NamedGroup "title" matches then use the last name pattern
        # else use the first name pattern

        print(patt.match("Mr. Dillon"))
        print(patt.match("Mr. Bob"))
        print(patt.match("Mr Dillon"))
        print(patt.match("Bob"))
        print(patt.match("Bob Dillon"))
    """

    def __init__(
        self,
        name_or_id: t.Union[str, int],
        yes_pattern: ValidPatternType,
        no_pattern: ValidPatternType,
    ):
        super().__init__(str(Group(str(name_or_id))), Or(yes_pattern, no_pattern))
