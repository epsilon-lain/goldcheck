"""Regression tests for M29 fixed-five all-orders moment no-go."""

from fractions import Fraction

from m29_all_orders_no_go import (
    DEN,
    DUAL_WEIGHTS,
    EXPECTED_DUAL_GAP,
    N,
    dual_audit,
    fixed_five_cost,
    normalized_moment_numerator,
)
from m28_moment_hierarchy import moment_constant


def test_m29_dual_mass_and_support():
    assert N == 861485625
    assert DEN == 100_000
    assert len(DUAL_WEIGHTS) == 103
    assert sum(DUAL_WEIGHTS.values()) == 41 * DEN


def test_m29_all_non5_moment_constraints():
    for monomial in range(1, 1 << 15):
        order = monomial.bit_count()
        assert normalized_moment_numerator(monomial) <= DEN * moment_constant(4, order)


def test_m29_exact_negative_dual_gap():
    result = dual_audit()
    assert result["total_mass"] == Fraction(41)
    assert result["tightest_moment_slack_numerator"] == 60
    assert result["tightest_moment_mask"] == 4
    assert result["dual_gap"] == EXPECTED_DUAL_GAP < 0
    assert result["all_orders_checked"] == 15
    assert result["method_class_excluded"] is True
    assert fixed_five_cost() == Fraction(807151395889143, 83666064453125)
