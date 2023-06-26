from regexfactory import Amount
import pytest
from hypothesis import given, settings, strategies as st
from tests.strategies import build_amount_greedy, build_bounds, build_amount


@pytest.mark.patterns
@given(st.text(min_size=1), st.integers(min_value=1))
def test_amount_single_count(word, count):
    actual = Amount(word, i=count)
    assert actual.regex == "{word}{{{count}}}".format(word=word, count=str(count))



@pytest.mark.patterns
@given(
    st.text(min_size=1),
    st.builds(
        build_bounds,
        lower_bound=st.integers(min_value=1),
        step=st.integers(min_value=1)
    )
)
def test_amount_lower_upper(word, bound: range):
    actual = Amount(word, bound.start, bound.stop)
    expected = "{word}{{{lower},{upper}}}".format(word=word, lower=str(bound.start), upper=str(bound.stop))
    assert actual.regex == expected


@pytest.mark.patterns
@given(st.text(min_size=1), st.integers(min_value=1))
def test_amount_or_more(word, count):
    actual = Amount(word, count, or_more=True)
    assert actual.regex == "{word}{{{count},}}".format(word=word, count=str(count))


@pytest.mark.patterns
@given(st.builds(
    lambda pattern, start, or_more, step: build_amount(pattern=pattern, start=start, or_more=or_more, greedy=False, step=step),
    st.text(min_size=1),
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1),
    st.booleans()
))
@settings(max_examples=500)
def test_amount_non_greedy(amt):
    """
    Test to ensure that instances of Amount with greedy as False will end with "?"
    """
    assert amt.regex.endswith("?")


@given(st.builds(
    build_amount_greedy,
    words=st.text(min_size=1),
    count=st.integers(min_value=1),
    greedy=st.booleans()
))
def test_amount_greedy(amtTuple: tuple[Amount, bool]):
    amt = amtTuple[0]
    greedy = amtTuple[1]
    ## if greedy = false then regex ends with ?
    assert greedy != amt.regex.endswith("?")
