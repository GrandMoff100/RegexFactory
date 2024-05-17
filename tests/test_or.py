import pytest
from hypothesis import given
from hypothesis import strategies as st
from strategies import pat_generic
from utils import check_one, check_regex

from regexfactory import RegexPattern, escape, or_


@given(pat_generic, pat_generic, st.data())
def test_operator_or(x, y, data):
    check_one(x | y, or_(x, y), data)


@given(pat_generic, pat_generic, pat_generic, st.data())
def test_or_assoc(x, y, z, data):
    check_one(x | (y | z), (x | y) | z, data)


@given(pat_generic, pat_generic, pat_generic, st.data())
def test_join_or1(x, y, z, data):
    check_one(
        (x | y) + z,
        (x + z) | (y + z),
        data,
    )


def test_join_or2b():
    # above does not pass the other way. ex:
    with pytest.raises(RuntimeError):
        x = or_("ax", "a")
        y = escape("xb")
        z = escape("bc")

        check_regex(x + (y | z), (x + y) | (x + z), "axbc")


@given(pat_generic, pat_generic, pat_generic, st.data())
def test_join_or2a(x: RegexPattern, y, z, data):
    # should work if x is only allowed to match one thing
    x = RegexPattern(f"(?>{x.regex})")
    check_one(
        x + (y | z),
        (x + y) | (x + z),
        data,
    )
