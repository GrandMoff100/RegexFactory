import re

from hypothesis import given
from hypothesis import strategies as st
from strategies import pat_generic
from utils import check_one

from regexfactory import RegexPattern, escape


@given(pat_generic, st.data())
def test_from_regex_str(x, data):
    check_one(x, RegexPattern.from_regex_str(x.regex), data)


@given(st.text(), st.data())
def test_escape_str(x, data):
    check_one(escape(x), re.escape(x), data)
