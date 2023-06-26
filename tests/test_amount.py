import pytest
from hypothesis import given, strategies as st

from regexfactory import Amount, ValidPatternType
from strategies import build_bounds, optional_step


def build_amount(pattern: ValidPatternType, start: int, or_more: bool, greedy: bool, step: Optional[int]):
    """
    General Amount builder. Note that the `j` parameter is constructed as
        the step plus start when step is defined. When step is None we assume
        that no upper bound is present.
    """
    stop_value = None
    if step is not None:
        stop_value = start + step
    return Amount(
        pattern=pattern,
        i=start,
        j=stop_value,
        or_more=or_more,
        greedy=greedy
    )


@pytest.mark.patterns
@given(st.text(min_size=1), st.integers(min_value=1))
def test_amount_single_count(word, count):
    """
    Test to ensure that when `or_more=False` and no upper bound is
        provided the regex will be of the form word{count}.
    """
    actual = Amount(word, i=count, or_more=False)
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
    """
    Test to ensure that if a lower and upper bound are provided then the
        regex of the resulting `Amount` will be of the form {word}{lower,upper}.
    """
    actual = Amount(word, bound.start, bound.stop)
    expected = "{word}{{{lower},{upper}}}".format(word=word, lower=str(bound.start), upper=str(bound.stop))
    assert actual.regex == expected


@pytest.mark.patterns
@given(st.text(min_size=1), st.integers(min_value=1))
def test_amount_or_more(word, count):
    """
    Test to ensure that when `or_more=True` and no upper bound is
        provided the regex will be of the form word{count,}.
    """
    actual = Amount(word, count, or_more=True)
    assert actual.regex == "{word}{{{count},}}".format(word=word, count=str(count))


@pytest.mark.patterns
@given(st.builds(
    build_amount,
    pattern=st.text(min_size=1),
    start=st.integers(min_value=1),
    or_more=st.booleans(),
    greedy=st.just(False),
    step=optional_step
))
def test_amount_non_greedy(amt):
    """
    Test to ensure that instances of Amount with greedy as False will end with "?"
    """
    assert amt.regex.endswith("?")
