import re

from hypothesis import given
from hypothesis import strategies as st
from utils import check_one

import regexfactory as r
from regexfactory import IfNotAhead, NotSet, Range, Set, or_, pattern

pattern._enable_desc = True


@given(st.data())
def test_range(data):
    check_one(
        Range("a", "e"),
        Set("abcde"),
        data,
    )


@given(st.text(), st.data())
def test_set(chars, data):
    check_one(
        Set(*chars),
        or_(*(re.escape(x) for x in chars)),
        data,
    )


@given(st.text(), st.data())
def test_notset(chars, data):
    check_one(
        NotSet(*chars),
        IfNotAhead(Set(*chars)) + NotSet(),
        data,
    )


@given(st.data())
def test_any(data):
    check_one(
        or_(r.ANY, r.WHITESPACE),
        NotSet(),
        data,
    )
