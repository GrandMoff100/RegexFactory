from regexfactory import Amount

def build_bounds(lower_bound, step) -> range:
    """
    Function to generate a tuple of (lower, upper) in which lower < upper
    """
    upper_bound = lower_bound + step
    return range(lower_bound, upper_bound + 1)

def build_amount_greedy(words, count, greedy):
    return (
        Amount(
            words,
            count,
            or_more=False,
            greedy=greedy
        ),
        greedy
    )
