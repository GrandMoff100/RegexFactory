"""Module for testing miscellaneous functions."""

from regexfactory import escape, RegexPattern


def test_escape():
    """Test escape function."""
    characters = {
        ".": "\\.",
        "^": "\\^",
        "$": "\\$",
        "*": "\\*",
        "+": "\\+",
        "?": "\\?",
        "{": "\\{",
        "}": "\\}",
        "(": "\\(",
        ")": "\\)",
        "[": "\\[",
        "]": "\\]",
        "|": "\\|",
        "\\": "\\\\",
        "a": "a",
        "b": "b",
        "c": "c",
        "1": "1",
        "2": "2",
        "3": "3",
        " ": "\\ ",
        "": "",
    }
    for key, value in characters.items():
        assert escape(key) == RegexPattern(value)


def test_join():
    patterns = [
        RegexPattern("a"),
        "b",
        re.compile
    ]