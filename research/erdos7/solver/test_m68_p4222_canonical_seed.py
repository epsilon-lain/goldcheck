from fractions import Fraction

from m68_p4222_canonical_seed import (
    C,
    EXPECTED_ETA,
    EXPECTED_FLOOR_MIN,
    EXPECTED_STATE_COUNT,
    N,
    certificate_audit,
    pointwise_exact,
)


def test_m68_constants_and_exact_argmin():
    assert N == 2_653_375_725
    assert EXPECTED_STATE_COUNT == 32_000_000
    assert EXPECTED_FLOOR_MIN == 348_498_368
    assert C == Fraction(69699, 200000)
    assert pointwise_exact((0,0,0,0,1,1,1024)) > C


def test_m68_summed_goodness_margin_positive():
    audit = certificate_audit()
    assert audit["floor_slack_scaled"] == 3368
    assert audit["summed_goodness_margin"] == EXPECTED_ETA > 0
    assert audit["noncovering_certified"]
