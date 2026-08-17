"""Regression tests for the M18 three-parameter six-prime family."""

from fractions import Fraction

from m18_three_parameter_family import (
    MONOTONICITY_DERIVATIVE_GAP,
    R_11_13_29,
    R_11_17_19,
    direct_bound_three_primes,
    family_number,
    monotonicity_derivative_lower_bound,
    proof_branch,
    three_parameter_family_audit,
)


def test_m18_direct_anchor_values_are_exact():
    assert direct_bound_three_primes(11, 13, 29) == R_11_13_29
    assert R_11_13_29 == Fraction(58755581, 58783725)
    assert 1 - R_11_13_29 == Fraction(28144, 58783725)

    assert direct_bound_three_primes(11, 17, 19) == R_11_17_19
    assert R_11_17_19 == Fraction(7187843, 7194825)
    assert 1 - R_11_17_19 == Fraction(6982, 7194825)


def test_m18_coordinate_monotonicity_gap_is_exact_and_positive():
    assert monotonicity_derivative_lower_bound() == MONOTONICITY_DERIVATIVE_GAP
    assert MONOTONICITY_DERIVATIVE_GAP == Fraction(133343, 245025)
    assert MONOTONICITY_DERIVATIVE_GAP > 0


def test_m18_only_three_minimal_triples_need_quadratic_branch():
    assert proof_branch(11, 13, 17) == "M16-quadratic"
    assert proof_branch(11, 13, 19) == "M16-quadratic"
    assert proof_branch(11, 13, 23) == "M16-quadratic"

    assert proof_branch(11, 13, 29) == "McNew-Setty-full-divisor"
    assert proof_branch(11, 17, 19) == "McNew-Setty-full-divisor"
    assert proof_branch(13, 17, 19) == "McNew-Setty-full-divisor"
    assert proof_branch(17, 19, 23) == "McNew-Setty-full-divisor"


def test_m18_family_numbers_include_m16_frontier():
    assert family_number(11, 13, 17) == 34459425
    assert family_number(11, 13, 19) == 38513475
    assert family_number(11, 13, 23) == 46621575


def test_m18_three_parameter_family_audit():
    result = three_parameter_family_audit()
    assert result["variable_prime_lower_bound"] == 11
    assert result["exceptional_quadratic_triples"] == (
        (11, 13, 17),
        (11, 13, 19),
        (11, 13, 23),
    )
    assert result["all_distinct_primes_p_q_r_ge_11_noncovering"] is True
