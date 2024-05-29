from hypothesis import given
from hypothesis import strategies as st

from regexfactory import escape, optional


def check(a, b: bool):
    assert (a is not None) == b


@given(st.text(), st.text())
def test_anchor_start(a: str, b: str):
    check(("^" + escape(a)).search(b), b.startswith(a))


@given(st.text(), st.text())
def test_anchor_end(a: str, b: str):
    check((escape(a) + "$").search(b), b.endswith(a))


@given(st.text(), st.text())
def test_optional(a: str, b: str):
    x = optional(escape(a)).search(a + b)
    assert x is not None
    assert x.group() == a

    x = optional(escape(a), greedy=False).search(a + b)
    assert x is not None
    assert x.group() == ""
