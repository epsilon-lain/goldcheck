"""Regression tests for the M28 all-orders 3-adic moment hierarchy."""
from fractions import Fraction

from m28_moment_hierarchy import (
    a4_moment_table,
    hierarchy_audit,
    intersection_level_sum,
    moment_constant,
    selected_fibre_count,
    support_moment_budget,
)


def test_selected_fibre_counts():
    assert tuple(selected_fibre_count(a) for a in range(1, 6)) == (2, 5, 14, 41, 122)


def test_first_three_intersection_sums():
    for a in range(1, 8):
        assert intersection_level_sum(a, 1) == (3**a - 1) // 2
        assert intersection_level_sum(a, 2) == 3**a - a - 1
        assert 4 * intersection_level_sum(a, 3) == 11 * 3**a - 6*a*a - 12*a - 11


def test_a4_hierarchy_and_m15_recovery():
    assert a4_moment_table() == (81, 197, 573, 1925, 7221)
    assert moment_constant(4, 2) == 197
    assert moment_constant(4, 3) == 573


def test_grouped_support_budget_exact_fraction():
    b1 = Fraction(156, 625)
    b2 = Fraction(1, 7)
    b3 = Fraction(1, 11)
    assert support_moment_budget(4, (b1, b2)) == 197 * b1 * b2
    assert support_moment_budget(4, (b1, b2, b3)) == 573 * b1 * b2 * b3
    assert support_moment_budget(4, (b1, b1, b2)) == 573 * b1 * b1 * b2


def test_hierarchy_audit():
    result = hierarchy_audit()
    assert result["a4"] == (81, 197, 573, 1925, 7221)
    assert result["third_moment_a4"] == 573
    assert result["verified"] is True
