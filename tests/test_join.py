import pytest
from hypothesis import example, given
from hypothesis import strategies as st
from strategies import non_escaped_text

from regexfactory.pattern import join


@pytest.mark.pattern
@given(
    st.lists(
        elements=non_escaped_text,
        min_size=1,
        max_size=10,
        unique=True
    )
)
@example(words=["0", "1"])
def test_join(words: list):
    """
    Tests to capture that the join function concatenates the expressions and
        each word in the list is found in the larger regex.
    """
    joined_regex = join(*words)
    assert joined_regex.regex == "".join(words)
