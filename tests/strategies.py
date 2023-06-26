from regexfactory import Amount
from regexfactory.pattern import ESCAPED_CHARACTERS, ValidPatternType
from string import printable
from typing import Optional


## Variable that defines all characters that are not used in escapes.
non_escape_printable = "".join(
    list(filter(lambda z: z not in list(ESCAPED_CHARACTERS), list(printable)))
)


def build_bounds(lower_bound, step) -> range:
    """
    Function to generate a tuple of (lower, upper) in which lower < upper
    """
    upper_bound = lower_bound + step
    return range(lower_bound, upper_bound + 1)


def build_amount(pattern: ValidPatternType, start: int, or_more: bool, greedy: bool, step: Optional[int]):
    """
    General Amount builder. This function will be repurposed with hard-coded
    values for a parameter when used with more specific use cases.
    Note that the `j` parameter is constructed as the step plus start
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




def build_amount_greedy(words, count, greedy):
    """
    Function to build a greedy instance of `Amount` .
    """
    return (
        Amount(
            words,
            count,
            or_more=False,
            greedy=greedy
        ),
        greedy
    )
