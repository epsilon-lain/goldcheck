"""Regression tests for the M16 quadratic frontier certificates."""

from fractions import Fraction

from m16_quadratic_frontier import certified_frontier, frontier_certificate


def test_m16_first_a4_frontier_is_excluded_exactly():
    result = frontier_certificate(17)
    assert result["N"] == 34459425
    assert result["C"] == Fraction(27401186093, 53178125000)
    assert result["summed_margin"] == Fraction(2804670823, 13294531250)
    assert result["proper_non5_min"] == Fraction(1, 91)
    assert result["completion_upper_max"] == Fraction(-744, 85085)
    assert result["noncovering_certified"] is True


def test_m16_next_two_frontier_seeds_are_excluded_exactly():
    results = certified_frontier()
    assert results[19]["N"] == 38513475
    assert results[23]["N"] == 46621575
    assert results[19]["summed_margin"] == Fraction(
        704120180922703, 1918675352343750
    )
    assert results[23]["summed_margin"] == Fraction(
        49732740695329, 83861791406250
    )
    assert all(r["noncovering_certified"] for r in results.values())
