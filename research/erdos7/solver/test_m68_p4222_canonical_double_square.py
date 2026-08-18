from fractions import Fraction

from m68_p4222_canonical_double_square import (
    C, EXPECTED_ETA, EXPECTED_FLOOR_MIN, EXPECTED_STATE_COUNT, N,
    certificate_audit, pointwise_exact,
)


def test_m68_exact_constants():
    audit = certificate_audit()
    assert audit["N"] == 2653375725
    assert audit["state_count"] == EXPECTED_STATE_COUNT == 32_000_000
    assert audit["floor_min_scaled"] == EXPECTED_FLOOR_MIN == 347_959_679
    assert audit["floor_slack_scaled"] == 9_679
    assert audit["summed_goodness_margin"] == EXPECTED_ETA > 0
    assert audit["noncovering_certified"]


def test_m68_recorded_argmin_is_exactly_above_C():
    state = (0, 0, 0, 0, 1, 1, 0)
    value = pointwise_exact(state)
    assert value > C
    assert Fraction(EXPECTED_FLOOR_MIN, 10**9) <= value
