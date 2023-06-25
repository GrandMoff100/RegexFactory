from regexfactory import Amount
from regexfactory.pattern import ESCAPED_CHARACTERS
from string import printable

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
