from hypothesis import given
from hypothesis import strategies as st
from strategies import pat_generic
from utils import check_one

from regexfactory import escape, join


@given(pat_generic, pat_generic, st.data())
def test_operator_add(x, y, data):
    check_one(x + y, join(x, y), data)


@given(pat_generic, pat_generic, pat_generic, st.data())
def test_join_assoc(x, y, z, data):
    check_one(x + (y + z), (x + y) + z, data)


@given(st.text(), st.text(), st.data())
def test_sum_escape(x, y, data):
    check_one(escape(x + y), escape(x) + escape(y), data)
