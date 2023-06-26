import pytest
from hypothesis import given, example, strategies as st

from regexfactory.pattern import join, ESCAPED_CHARACTERS


@pytest.mark.pattern
@given(
    st.lists(
        elements=st.text(
            min_size=1,
            alphabet=st.characters(
                blacklist_characters=list(ESCAPED_CHARACTERS)
            )
        ),
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
