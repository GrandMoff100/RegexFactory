import re

import pytest
from hypothesis import given
from hypothesis import strategies as st
from strategies import non_escape_char

from regexfactory import Set


@pytest.mark.patterns
@given(
    st.lists(
        elements=non_escape_char,
        min_size=1
    )
)
def test_set(chars: list):
    actual = Set(*chars)
    for value in chars:
        assert (
            isinstance(actual.match(value), re.Match)
        )
