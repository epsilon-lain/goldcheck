"""Regression tests for the M25 cross-support seed certificate."""
from fractions import Fraction

from m25_cross_support_seed import (
    CROSS,
    DIAGONAL,
    EXPECTED_C,
    EXPECTED_MARGIN,
    N,
    baseline,
    seed_certificate,
)


def test_m25_seed_and_baseline_are_exact():
    assert N == 172297125
    assert baseline(1) == Fraction(31, 125)
    assert baseline(2) == Fraction(1, 7)
    assert baseline(31) == Fraction(31, 2127125)


def test_m25_uses_genuine_cross_support_second_moments():
    assert len(CROSS) == 46
    assert all(s % 2 == 0 and t % 2 == 0 and s < t for s, t in CROSS)
    assert len(DIAGONAL) == 16
    assert all(mask & 1 for mask in DIAGONAL)


def test_m25_exact_pointwise_and_summed_certificate():
    result = seed_certificate()
    assert result["C"] == EXPECTED_C
    assert EXPECTED_C == Fraction(
        8062944017330066479969,
        19768351476874000000000,
    )
    assert result["summed_margin"] == EXPECTED_MARGIN
    assert EXPECTED_MARGIN == Fraction(
        148743273991746196533,
        3953670295374800000000,
    )
    assert result["summed_margin"] > 0
    assert result["cross_term_count"] == 46
    assert result["diagonal_term_count"] == 16


def test_m25_completion_audit_is_strict():
    result = seed_certificate()
    assert result["proper_non5_min"] == Fraction(1, 91) > 0
    assert result["full_non5_min"] == Fraction(-258, 17017) < 0
    assert result["completion_upper_max"] == Fraction(-3629, 425425) < 0
    assert result["noncovering_certified"] is True
