import re

import pytest
from hypothesis import given, strategies as st

from regexfactory import Set
from regexfactory.pattern import ESCAPED_CHARACTERS


@pytest.mark.patterns
@given(
    st.lists(
        elements=st.characters(blacklist_characters=list(ESCAPED_CHARACTERS)),
    )
)
def test_set(chars: list):
    actual = Set(*chars)
    for value in chars:
        assert (
            isinstance(actual.match(value), re.Match)
        )

