"""Regression tests for the exact M31 centered-multilinear no-go."""
from fractions import Fraction

from m31_centered_multilinear_no_go import (
    DEN,
    DUAL_WEIGHTS,
    EXPECTED_DUAL_GAP,
    centered_monomial_numerator,
    dual_audit,
    repeated_square_moment,
)
from m30_centered_moments import centered_moment_constant


def test_m31_dual_mass_and_all_centered_constraints():
    assert len(DUAL_WEIGHTS) == 124
    assert sum(DUAL_WEIGHTS.values()) == 41 * DEN
    for mask in range(1, 1 << 15):
        order = mask.bit_count()
        assert centered_monomial_numerator(mask) <= (
            DEN * centered_moment_constant(4, order)
        )


def test_m31_exact_negative_gap():
    out = dual_audit()
    assert out["dual_gap"] == EXPECTED_DUAL_GAP < 0
    assert out["method_class_excluded"] is True
    assert out["tightest_centered_slack"] == 0
    assert out["tightest_centered_mask"] == 1


def test_m31_pinpoints_repeated_support_escape():
    assert centered_moment_constant(4, 2) == 76
    for i in range(15):
        assert repeated_square_moment(i) == Fraction(160)
        assert repeated_square_moment(i) - 76 == 84
