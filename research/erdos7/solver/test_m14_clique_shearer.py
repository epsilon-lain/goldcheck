"""Regression tests for the Milestone 14 exact Clique-Shearer seed certificate."""

from fractions import Fraction

from m14_clique_shearer import (
    C,
    affine_box_minimum,
    fourteen_fiber_margin,
    lambda_baseline_sum,
    non5_worst_coordinate_polynomials,
    seed_certificate,
)


def test_non5_worst_corner_is_inside_clique_shearer_region():
    rho = non5_worst_coordinate_polynomials()
    assert rho[30] == Fraction(941, 17017)
    assert min(rho.values()) == Fraction(941, 17017)
    assert all(value > 0 for value in rho.values())


def test_affine_certificate_and_fourteen_fiber_margin_exact():
    box = affine_box_minimum()
    assert box["minimum"] == C == Fraction(8134, 12155)
    assert box["non5_upper"] == ()
    assert box["five_upper"] == (1, 9, 17)
    assert lambda_baseline_sum() == Fraction(144411, 425425)
    assert fourteen_fiber_margin() == Fraction(86563, 425425) > 0


def test_seed_certificate_summary():
    result = seed_certificate()
    assert result["N"] == 11486475
    assert result["verified"] is True
    assert result["fourteen_fiber_margin"] > 0
