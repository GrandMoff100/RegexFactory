from typing import Optional

from hypothesis import strategies as st

from regexfactory import Amount
from regexfactory.pattern import ESCAPED_CHARACTERS, ValidPatternType

# Strategy to generate text that avoids escaped characters
non_escaped_text = st.text(
    min_size=1,
    alphabet=st.characters(
        blacklist_characters=list(ESCAPED_CHARACTERS)
    )
)

# Strategy to produce either None or a positive integer
optional_step = st.one_of(
    st.none(),
    st.integers(min_value=1)
)


def build_bounds(lower_bound, step) -> range:
    """
    Function to generate a tuple of (lower, upper) in which lower < upper
    """
    upper_bound = lower_bound + step
    return range(lower_bound, upper_bound + 1)


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

