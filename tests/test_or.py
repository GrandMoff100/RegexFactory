import re

import pytest
from hypothesis import example, given
from hypothesis import strategies as st
from strategies import non_escaped_text

from regexfactory import Or


@pytest.mark.patterns
@given(
    st.lists(
        non_escaped_text,
        min_size=1,
        max_size=10,
    )
)
@example(arr=["0", "0"])
def test_matching_or(arr: list):
    actual = Or(*arr)
    if len(arr) == 1:
        assert (
            isinstance(actual.match(arr[0]), re.Match)
        )
    else:
        for value in arr:
            assert (
                isinstance(actual.match(value), re.Match)
            )


