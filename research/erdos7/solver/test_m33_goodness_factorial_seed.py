"""Regression tests for the exact M33 asymmetric (4,4) seed certificate."""
from fractions import Fraction

from m33_goodness_factorial_seed import (
    C,
    EXPECTED_GLOBAL_MARGIN,
    factorial_global_cost,
    pointwise_goodness_certificate,
    seed_certificate,
    special_global_cost,
    special_point_min,
)


def test_m33_exact_special_costs():
    assert special_point_min() == Fraction(45778312503188, 851714903064025)
    assert special_global_cost() == Fraction(5019735697491668, 851714903064025)
    assert factorial_global_cost() == Fraction(2600707, 500000)


def test_m33_pointwise_goodness_eight_million_states():
    out = pointwise_goodness_certificate()
    assert out["state_count"] == 8_000_000
    assert out["floor_min"] > C
    assert out["floor_slack_scaled"] == 3_809_359_581
    assert out["verified"] is True


def test_m33_positive_summed_goodness_and_seed_closure():
    out = seed_certificate()
    assert out["summed_goodness_margin"] == EXPECTED_GLOBAL_MARGIN > 0
    assert out["noncovering_certified"] is True
