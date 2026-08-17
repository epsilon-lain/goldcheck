"""Regression tests for M27 scaled M25 cone."""
from fractions import Fraction

from m27_scaled_m25_cone import (
    DOMINATED_SIMPLE_TUPLES,
    EXPECTED_MARGIN,
    REFERENCE_COORDS,
    REMAINING_SEEDS,
    coordinatewise_scaled,
    dominated_seed_audit,
    reference_certificate,
    scaling_factors,
    simple_tuple_coords,
)


def test_m27_reference_exact_certificate_is_positive():
    result = reference_certificate()
    assert REFERENCE_COORDS == (
        Fraction(156, 625), Fraction(1, 7), Fraction(1, 11),
        Fraction(1, 13), Fraction(1, 19),
    )
    assert result["summed_margin"] == EXPECTED_MARGIN > 0
    assert result["proper_non5_min"] == Fraction(1, 91) > 0
    assert result["completion_upper_max"] == Fraction(-118016, 11886875) < 0


def test_m27_nine_m26_seeds_are_reference_dominated():
    assert len(DOMINATED_SIMPLE_TUPLES) == 9
    for simple in DOMINATED_SIMPLE_TUPLES:
        actual = simple_tuple_coords(simple)
        assert coordinatewise_scaled(actual)
        assert all(gamma >= 1 for gamma in scaling_factors(actual).values())


def test_m27_leaves_exactly_two_m26_profile_seeds():
    result = dominated_seed_audit()
    assert result["scaled_seed_count"] == 9
    assert result["remaining_seeds"] == REMAINING_SEEDS
    assert REMAINING_SEEDS == (861485625, 2363916555)
    assert result["verified"] is True


def test_m27_p17_canonical_is_not_claimed_by_scaling():
    p17 = (Fraction(156, 625), Fraction(1, 7), Fraction(1, 11), Fraction(1, 13), Fraction(1, 17))
    assert coordinatewise_scaled(p17) is False
