"""Tests for the exact SAT model and verifier in ``covering.py``."""

from covering import (
    CoverProblem,
    deficiency,
    divisors,
    factor,
    sigma,
    solve_cover,
    tau,
    verify_cover,
)


def test_arithmetic_helpers():
    assert divisors(12) == [1, 2, 3, 4, 6, 12]
    assert factor(10395) == [(3, 3), (5, 1), (7, 1), (11, 1)]
    assert sigma(35) == 48
    assert tau(10395) == 32


def test_least_covering_number_is_12():
    sat, cover = solve_cover(12, solver="cadical153")
    assert sat
    assert cover is not None and verify_cover(12, cover)


def test_small_non_covering_numbers():
    for N in (2, 3, 4, 6, 10, 11):
        sat, cover = solve_cover(N, solver="cadical153")
        assert not sat
        assert cover is None


def test_verify_cover_rejects_invalid_inputs():
    # Duplicate modulus.
    assert not verify_cover(12, [(2, 0), (2, 1), (3, 0), (4, 1), (6, 1), (12, 11)])
    # Modulus not dividing N.
    assert not verify_cover(12, [(5, 0)])
    # Residue out of range.
    assert not verify_cover(12, [(2, 2)])


def test_cover_problem_has_distinct_moduli_constraints():
    prob = CoverProblem(6)
    prob.build_cover()
    # Each divisor has at-most-one-residue clauses; just check the var count.
    assert set(prob.var.keys()) == {
        (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)
    }
