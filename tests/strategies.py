from hypothesis import event
from hypothesis import strategies as st

import regexfactory as r
from regexfactory import NotSet, Range, RegexPattern, amount, escape, or_


@st.composite
def pat_base(draw: st.DrawFn) -> RegexPattern:
    v = draw(st.integers(0, 99))
    v = 99 - v

    def case(weight: int):
        nonlocal v
        v -= weight
        return v < 0

    if case(10):
        charsets = [
            r.ANY,
            r.ANCHOR_START,
            r.ANCHOR_END,
            r.WHITESPACE,
            r.NOTWHITESPACE,
            r.WORD,
            r.NOTWORD,
            r.DIGIT,
            r.NOTDIGIT,
        ]
        return draw(st.sampled_from(charsets))

    if case(10):
        chars = draw(st.lists(elements=st.characters(codec="utf-8")))
        return or_(*(escape(x) for x in chars))

    if case(5):
        chars = draw(st.lists(elements=st.characters(codec="utf-8")))
        return NotSet(*chars)

    if case(5):
        x = draw(st.characters(codec="utf-8"))
        y = draw(st.characters(codec="utf-8"))
        if x > y:
            x, y = y, x
        return Range(x, y)

    return escape(draw(st.text()))


@st.composite
def _pat_extend(draw: st.DrawFn, children: st.SearchStrategy[RegexPattern]):
    if not draw(st.booleans()):
        return draw(children) + draw(children)

    if not draw(st.booleans()):
        return draw(children) | draw(children)

    c = draw(children)

    if draw(st.booleans()):
        return amount(
            c, draw(st.integers(0, 4)), None, draw(st.booleans()), draw(st.booleans())
        )

    a = draw(st.integers(0, 2))
    b = draw(st.integers(0, 2))
    return amount(c, a, a + b, False, draw(st.booleans()))


pat_generic: st.SearchStrategy[RegexPattern] = st.recursive(pat_base(), _pat_extend)


always_case = ["", "a", "ab", "aa", ".", " ", "\t", "\n"]


@st.composite
def _gencase_random(draw: st.DrawFn, r1: str, r2: str):
    # use_true_random prevent shrinks
    x = draw(st.randoms(use_true_random=True)).randint(0, 9)

    # use st.text() most of the time since its much faster
    if x < 8:
        return draw(st.text())

    event("generating test case using st.from_regex")
    if x < 9:
        ans = draw(st.from_regex(r1))
    else:
        ans = draw(st.from_regex(r2))

    event("st.from_regex succeeded")
    return ans


def gencase(r1: str, r2: str) -> st.SearchStrategy[str]:
    """generate a str suitable for checking if r1 and r2 behave the same on that str"""
    # allow shrinking towards always or text()
    return st.sampled_from(always_case) | st.text() | _gencase_random(r1, r2)
