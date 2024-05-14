from hypothesis import given
from hypothesis import strategies as st
from strategies import pat_generic
from utils import check_one

from regexfactory import amount, join, multi, optional


@given(pat_generic, st.integers(0, 4), st.data())
def test_operator_mul(x, n, data):
    check_one(x * n, join(*(x for _ in range(n))), data)


# invariants of amount


@given(pat_generic, st.integers(0, 4), st.booleans(), st.data())
def test_amount_fixed1(x, n, greedy, data):
    check_one(
        amount(x, n, n, greedy=greedy),
        x * n,
        data,
    )


@given(pat_generic, st.integers(0, 4), st.booleans(), st.data())
def test_amount_fixed2(x, n, greedy, data):
    check_one(
        amount(x, n, greedy=greedy),
        x * n,
        data,
    )


@given(pat_generic, st.integers(0, 4), st.integers(0, 4), st.booleans(), st.data())
def test_amount_bounded(x, n, m, greedy, data):
    check_one(
        amount(x, n, n + m, greedy=greedy),
        x * n + (optional(x, greedy=greedy)) * m,
        data,
    )


@given(pat_generic, st.integers(0, 4), st.booleans(), st.data())
def test_amount_or_more1(x, n, greedy, data):
    check_one(
        amount(x, n, or_more=True, greedy=greedy),
        x * n + amount(x, 0, or_more=True, greedy=greedy),
        data,
    )


@given(pat_generic, st.booleans(), st.data())
def test_amount_or_more2(x, greedy, data):
    check_one(
        amount(x, 0, or_more=True, greedy=greedy),
        optional(x, greedy=greedy) + amount(x, 0, or_more=True, greedy=greedy),
        data,
    )


# multi is consistent with + and *


@given(pat_generic, st.data())
def test_multi1(x, data):
    check_one(
        multi(x),
        f"(?:{x.regex})+",
        data,
    )


@given(pat_generic, st.data())
def test_multi2(x, data):
    check_one(
        multi(x, match_zero=True),
        f"(?:{x.regex})*",
        data,
    )
