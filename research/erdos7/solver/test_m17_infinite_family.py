"""Regression tests for the M17 infinite six-prime family bridge."""

from fractions import Fraction

from m17_infinite_family import (
    DIRECT_A,
    DIRECT_B,
    DIRECT_R29,
    DIRECT_REAL_THRESHOLD,
    direct_bound_closed,
    direct_bound_from_definition,
    family_number,
    infinite_family_audit,
    proof_branch,
)


def test_m17_closed_full_divisor_formula_is_exact():
    assert DIRECT_A == Fraction(220676, 225225)
    assert DIRECT_B == Fraction(17833, 31185)
    for P in (17, 19, 23, 29, 31, 101):
        assert direct_bound_from_definition(P) == direct_bound_closed(P)


def test_m17_direct_threshold_starts_at_29():
    assert DIRECT_REAL_THRESHOLD == Fraction(1159145, 40941)
    assert 28 < DIRECT_REAL_THRESHOLD < 29
    assert DIRECT_R29 == Fraction(58755581, 58783725)
    assert 1 - DIRECT_R29 == Fraction(28144, 58783725)
    assert direct_bound_closed(29) < 1
    assert direct_bound_closed(31) < direct_bound_closed(29)


def test_m17_bridge_covers_every_prime_from_17():
    result = infinite_family_audit()
    assert result["finite_quadratic_primes"] == (17, 19, 23)
    assert result["direct_first_integer"] == 29
    assert result["all_primes_P_ge_17_noncovering"] is True
    assert proof_branch(17) == "M16-quadratic"
    assert proof_branch(23) == "M16-quadratic"
    assert proof_branch(29) == "McNew-Setty-full-divisor"
    assert proof_branch(101) == "McNew-Setty-full-divisor"


def test_m17_family_numbers_recover_frontier():
    assert family_number(17) == 34459425
    assert family_number(19) == 38513475
    assert family_number(23) == 46621575
