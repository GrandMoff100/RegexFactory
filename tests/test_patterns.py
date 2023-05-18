"""Module for testing regex construction."""

from regexfactory import (
    Range,
    Or,
    Set,
    NotSet,
    Amount,
    Multi,
    Optional,
    Extension,
    NamedGroup,
    NamedReference,
    NumberedReference,
    Comment,
    IfAhead,
    IfNotAhead,
    IfBehind,
    IfNotBehind,
    Group,
    IfGroup,
)


def test_RANGE():
    """Test Range class."""
    assert Range("a", "z").match("m")


def test_OR():
    """Test Or class."""
    patt = Or("Bob", "work")
    assert ["work", "Bob"] == patt.findall("i work for Bob")


def test_SET():
    """Test Set class."""
    patt = Set("?!.,")
    assert ["!", "?", "."] == patt.findall("Hello! How are you? I am well.")


def test_NOTSET():
    """Test NotSet class."""
    patt = NotSet("?!.,")
    assert patt.findall("Hi there!") == ["H", "i", " ", "t", "h", "e", "r", "e"]


def test_AMOUNT():
    """Test Amount class."""
    patt = Amount("Foo|Bar", 2)
    print(patt.regex)
    assert patt.findall("Foo Bar FooBar aa aaa aaaa") == ["FooBar"]


def test_MULTI():
    """Test Multi class."""
    patt = Multi("b", 1, 3)
    assert patt.findall("Foo Bar FooBar aa aaa aaaa") == ["Foo", "Foo", "Foo"]

def test_NOTSET():
    pass


def test_AMOUNT():
    pass


def test_MULTI():
    pass


def test_OPTIONAL():
    pass


def test_EXTENSION():
    pass


def test_NAMEDGROUP():
    pass


def test_NAMEDREFERENCE():
    pass


def test_NUMBEREDREFERENCE():
    pass


def test_COMMENT():
    pass


def test_IFAHEAD():
    pass


def test_IFNOTAHEAD():
    pass


def test_IFBEHIND():
    pass


def test_IFNOTBEHIND():
    pass


def test_GROUP():
    pass


def test_IFGROUP():
    pass
