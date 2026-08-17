"""Regression tests for the independent Milestone 14 Shearer audit."""

from fractions import Fraction

from m14_shearer_audit import shearer_audit


def test_m14_non5_shearer_box_and_split_are_exact():
    result = shearer_audit()
    assert result["non5_coordinate_count"] == 16
    assert result["non5_box_min"] == Fraction(941, 17017)
    assert result["all_non5_coordinates_positive"] is True
    assert result["five_coordinate_split_exact"] is True
