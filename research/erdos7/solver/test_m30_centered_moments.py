"""Regression tests for M30 centered 3-adic moment hierarchy."""
from fractions import Fraction

from m30_centered_moments import (
    centered_moment_constant,
    centered_support_budget,
    factorial_spike_cap,
    hierarchy_audit,
    raw_from_centered,
)


def test_m30_a4_tables():
    assert tuple(centered_moment_constant(4, t) for t in range(1, 6)) == (
        40, 76, 184, 532, 1720
    )
    assert tuple(factorial_spike_cap(4, t) for t in range(1, 5)) == (
        40, 18, 6, 1
    )


def test_m30_recovers_m28_raw_constants():
    assert tuple(raw_from_centered(4, t) for t in range(1, 6)) == (
        81, 197, 573, 1925, 7221
    )
    assert raw_from_centered(3, 2) == 63
    assert raw_from_centered(5, 2) == 601


def test_m30_exact_grouped_budget():
    b1 = Fraction(1, 7)
    b2 = Fraction(1, 11)
    b3 = Fraction(1, 13)
    assert centered_support_budget(4, (b1,)) == Fraction(40, 7)
    assert centered_support_budget(4, (b1, b2)) == Fraction(76, 77)
    assert centered_support_budget(4, (b1, b2, b3)) == Fraction(184, 1001)


def test_m30_audit():
    out = hierarchy_audit()
    assert out["a4_centered"] == (40, 76, 184, 532, 1720)
    assert out["a4_factorial"] == (40, 18, 6, 1)
    assert out["raw_recovery_checked"] is True
    assert out["verified"] is True
