from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from strategies import gencase, pat_generic
from utils import check_regex

from regexfactory import RegexPattern, pattern

pattern._enable_debug = True


# checks that ._reference_regex behaves the same as .regex
@given(pat_generic, st.data())
@settings(
    max_examples=10000, suppress_health_check=[HealthCheck.too_slow], deadline=None
)
def test_reference(pat: RegexPattern, data: st.DataObject):
    assume(pat._reference_regex is not None)
    assert pat._reference_regex is not None
    assume(pat.regex != pat._reference_regex)
    check_regex(
        pat.regex,
        pat._reference_regex,
        data.draw(gencase(pat.regex, pat._reference_regex)),
    )
