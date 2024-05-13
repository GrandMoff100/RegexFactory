import re

from hypothesis import strategies as st

from regexfactory import RegexPattern, ValidPatternType


def check_regex(p1: ValidPatternType, p2: ValidPatternType, v: str):
    r1 = p1 if isinstance(p1, str) else RegexPattern.create(p1).regex
    r2 = p2 if isinstance(p2, str) else RegexPattern.create(p2).regex

    """checks that r1 and r2 does the same on v"""
    if r1 == r2:
        return

    x = re.compile(r1).search(v)
    y = re.compile(r2).search(v)

    try:
        assert (x is None) == (y is None)

        if x is not None:
            assert y is not None
            assert x.start() == y.start()
            assert x.end() == y.end()
    except Exception as e:
        raise RuntimeError(
            f"string {v!r} results in:\n"
            f"r1: {r1!r}\n"
            f"=> {x!r}\n"
            f"r2: {r2!r}\n"
            f"=> {y!r}\n"
        ) from e


def check_one(v1: ValidPatternType, v2: ValidPatternType, data: st.DataObject):
    from strategies import gencase

    r1 = RegexPattern.create(v1).regex
    r2 = RegexPattern.create(v2).regex
    if r1 == r2:
        return
    check_regex(r1, r2, data.draw(gencase(r1, r2)))
