"""Regression tests for the M19 four-parameter six-prime family."""

from fractions import Fraction

from m19_four_parameter_family import (
    DIRECT_ANCHOR,
    MONOTONICITY_DERIVATIVE_GAP,
    direct_bound_four_primes,
    family_number,
    four_parameter_family_audit,
    monotonicity_derivative_lower_bound,
    proof_branch,
)


def test_m19_direct_anchor_is_exact():
    assert direct_bound_four_primes(11, 13, 17, 19) == DIRECT_ANCHOR
    assert DIRECT_ANCHOR == Fraction(276127, 289575)
    assert 1 - DIRECT_ANCHOR == Fraction(13448, 289575)


def test_m19_monotonicity_gap_is_exact():
    assert monotonicity_derivative_lower_bound() == MONOTONICITY_DERIVATIVE_GAP
    assert MONOTONICITY_DERIVATIVE_GAP == Fraction(94259, 231525)
    assert MONOTONICITY_DERIVATIVE_GAP > 0


def test_m19_proof_branches_cover_both_regions():
    assert proof_branch(7, 11, 13, 17) == "M18-three-parameter"
    assert proof_branch(7, 17, 19, 23) == "M18-three-parameter"
    assert proof_branch(11, 13, 17, 19) == "McNew-Setty-full-divisor"
    assert proof_branch(13, 17, 19, 23) == "McNew-Setty-full-divisor"


def test_m19_family_number_recovers_first_frontier():
    assert family_number(7, 11, 13, 17) == 34459425


def test_m19_four_parameter_family_audit():
    result = four_parameter_family_audit()
    assert result["variable_prime_lower_bound"] == 7
    assert result["all_distinct_primes_p_q_r_s_ge_7_noncovering"] is True
