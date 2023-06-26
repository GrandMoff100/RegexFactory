import pytest

from regexfactory import Range


@pytest.mark.patterns
def test_numeric_range_simple():
    start = "0"
    end = "9"
    assert Range(start, end).regex == "[0-9]"


@pytest.mark.patterns
@pytest.mark.parametrize(
    "start, stop, expected",
    [
        ("0", "9", "[0-9]"),
        ("a", "f", "[a-f]"),
        ("r", "q", "[r-q]"),
        ("A", "Z", "[A-Z]"),
    ],
)
def test_numeric_range_parameters(start, stop, expected):
    actual = Range(start=start, stop=stop)
    assert actual.regex == expected
