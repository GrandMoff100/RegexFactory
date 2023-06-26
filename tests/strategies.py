from hypothesis import strategies as st

from regexfactory.pattern import ESCAPED_CHARACTERS

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

