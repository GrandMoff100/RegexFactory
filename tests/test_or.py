from regexfactory import Or
import pytest
from hypothesis import (
    example,
    given,
    strategies as st
)
import re
from strategies import non_escape_printable


@pytest.mark.patterns
@given(
    st.lists(
        st.text(alphabet=non_escape_printable, min_size=1),
        min_size=2,
        max_size=10,
        unique=True
    )
)
@example(arr=["0", "0"])
def test_matching_or(arr: list):
    actual = Or(*arr)
    for value in arr:
        assert (
            isinstance(actual.match(value), re.Match)
        )


