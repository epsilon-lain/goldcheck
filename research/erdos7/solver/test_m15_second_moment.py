"""Regression tests for the exact M15 second-moment constraints."""

from fractions import Fraction

from m15_second_moment import (
    a4_old_dual_second_moments,
    second_moment_constant,
    support_pair_budget,
)


def test_second_moment_constants_are_exact():
    assert second_moment_constant(1) == 5
    assert second_moment_constant(2) == 19
    assert second_moment_constant(3) == 63
    assert second_moment_constant(4) == 197


def test_support_pair_budget_scales_by_baselines():
    assert support_pair_budget(4, 1, 1) == Fraction(197 * 36, 625)
    assert support_pair_budget(4, 2, 4) == Fraction(197, 7 * 11)


def test_old_affine_dual_is_cut_on_every_diagonal():
    result = a4_old_dual_second_moments()
    assert result["actual_second_moment_cap"] == Fraction(197)
    assert result["dual_diagonal_second_moment"] == Fraction(281)
    assert result["violating_support_count"] == 31
    assert result["all_31_diagonals_cut"] is True
