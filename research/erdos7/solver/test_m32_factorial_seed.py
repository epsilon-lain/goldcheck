"""Regression tests for the exact M32 repeated-support seed certificate."""
from fractions import Fraction

from m32_factorial_seed import (
    C,
    EXPECTED_GLOBAL_MARGIN,
    completion_audit,
    factorial_global_cost,
    pointwise_floor_certificate,
    seed_certificate,
)


def test_m32_pointwise_eight_million_state_certificate():
    out = pointwise_floor_certificate()
    assert out["state_count"] == 8_000_000
    assert out["floor_min"] > C
    assert out["floor_slack_scaled"] == 994_349
    assert out["verified"] is True


def test_m32_completion_audit():
    out = completion_audit()
    assert out["proper_non5_min"] == Fraction(1, 91) > 0
    assert out["full_non5_min"] == Fraction(-258, 17017)
    assert out["completion_upper_max"] == Fraction(-1062, 125125) < 0
    assert out["verified"] is True


def test_m32_summed_margin_and_seed_closure():
    assert factorial_global_cost() == Fraction(837687, 250000)
    out = seed_certificate()
    assert out["summed_margin"] == EXPECTED_GLOBAL_MARGIN > 0
    assert out["noncovering_certified"] is True
