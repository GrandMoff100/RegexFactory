from regexfactory import Amount
import pytest
from hypothesis import (
    given,
    strategies as st
)


@pytest.mark.patterns
@given(st.text(min_size=1), st.integers(min_value=1))
def test_amount(word, count):
    actual = Amount(word, count)
    assert actual.regex == "{word}{{{count}}}".format(word=word, count=str(count))


