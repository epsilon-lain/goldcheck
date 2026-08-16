"""Tests for the full prime-power form of McNew--Setty Lemma 4.10."""

from fractions import Fraction
from itertools import product

import pytest

from certificate import squarefree_coverage_bound
from covering import factor
from full_bound import (
    OMEGA5_CORNER_BOUND,
    all_primes_condition_vec,
    deficiency_bound,
    divisor_R,
    n_from,
    odd_omega_limit,
    omega_le_4_excluded,
    omega5_large_q_excluded,
    omega5_support_excluded,
    sigma_from,
    smallest_omega5_survivor,
    support_R,
    support_R_from_xs,
    support_R_limit,
)


def _primes_exps(n):
    fs = factor(n)
    return [p for p, _ in fs], [a for _, a in fs]


def test_51975_is_excluded_by_full_bound():
    # 51975 = 3^3 * 5^2 * 7 * 11, R = 9536/10395, so delta >= 4295.
    p, e = _primes_exps(51975)
    assert support_R(p, e) == Fraction(9536, 10395)
    assert deficiency_bound(51975) == 4295


def test_former_survivors_now_excluded():
    for n, lower in ((496125, 57006), (61425, 5733), (135135, 8557)):
        assert deficiency_bound(n) >= lower
        assert deficiency_bound(n) > 0


@pytest.mark.parametrize("n", [51975, 496125, 61425, 135135, 945, 10395, 12285, 17325, 1155, 1365, 105, 385, 12, 90, 210])
def test_support_form_matches_direct_divisor_sum(n):
    p, e = _primes_exps(n)
    assert support_R(p, e) == divisor_R(n)


def test_squarefree_cross_check():
    for n in (15, 105, 1155, 1365, 385, 455, 231, 165):
        assert deficiency_bound(n) == n - squarefree_coverage_bound(n)


def test_omega_limits():
    assert odd_omega_limit(1) == Fraction(1, 2)
    assert odd_omega_limit(2) == Fraction(3, 4)
    assert odd_omega_limit(3) == Fraction(43, 48)
    assert odd_omega_limit(4) == Fraction(31, 32)
    assert odd_omega_limit(5) > 1


def test_omega_le_4_is_always_excluded():
    # Every odd n with omega(n) <= 4 has R(n) < 1 (proved in NOTES.md); spot
    # check a grid of exponent vectors.
    primes_sets = [[3], [3, 5], [3, 5, 7], [3, 5, 7, 11]]
    for primes in primes_sets:
        for exps in product(range(1, 7), repeat=len(primes)):
            n = n_from(primes, list(exps))
            assert support_R(primes, list(exps)) < 1
            assert omega_le_4_excluded(n)


def test_smallest_omega5_survivor():
    n, exps, R = smallest_omega5_survivor()
    assert n == 70945875
    assert exps == {3: 4, 5: 3, 7: 2, 11: 1, 13: 1}
    assert R > 1
    # The survivor passes the primitive necessary condition and abundance.
    assert all_primes_condition_vec([3, 5, 7, 11, 13], [4, 3, 2, 1, 1])
    assert sigma_from([3, 5, 7, 11, 13], [4, 3, 2, 1, 1]) > 2 * n


def test_omega5_corner_bound_is_exact():
    # R(1/2, 1/4, 1/6, 1/10, 1/22) = 5263/5280 < 1.
    xs = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 6), Fraction(1, 10), Fraction(1, 22)]
    assert support_R_from_xs(xs) == OMEGA5_CORNER_BOUND
    assert OMEGA5_CORNER_BOUND < 1


def test_support_R_limit_dominates_finite_exponents():
    # R is coordinatewise nondecreasing in each x_i, so finite exponents can
    # only decrease R relative to the infinite-exponent limit.
    for primes in ([3, 5, 7, 11, 13], [3, 5, 7, 11, 23], [3, 5, 7, 13, 19]):
        limit = support_R_limit(primes)
        for exps in ([1, 1, 1, 1, 1], [2, 1, 1, 1, 1], [1, 2, 2, 1, 1], [4, 3, 2, 1, 1]):
            assert support_R(primes, exps) <= limit


def test_omega5_large_q_excluded():
    # Largest prime >= 23 is uniformly excluded by the corner bound.
    ok, lower = omega5_large_q_excluded([3, 5, 7, 11, 23], [4, 3, 2, 1, 1])
    assert ok and lower >= 1
    # The bound also holds for the exact corner-defect lower bound.
    n = n_from([3, 5, 7, 11, 23], [4, 3, 2, 1, 1])
    assert lower == (n * 17 + 5279) // 5280
    # A largest prime below the threshold is not covered by this family.
    ok, _ = omega5_large_q_excluded([3, 5, 7, 11, 19], [4, 3, 2, 1, 1])
    assert not ok


def test_omega5_support_excluded_threshold():
    assert omega5_support_excluded([3, 5, 7, 11, 23])
    assert not omega5_support_excluded([3, 5, 7, 11, 13])
    assert not omega5_support_excluded([3, 5, 7, 11, 19])


def test_deficiency_bound_integer_for_random_small_odd():
    # n*(1-R) is an exact integer for every n.
    for p, e in [([3, 5, 7], [2, 2, 2]), ([3, 5, 7, 11], [3, 2, 1, 1]), ([3, 5, 7, 11, 13], [2, 2, 2, 1, 1])]:
        n = n_from(p, e)
        assert n * support_R(p, e) == int(n * support_R(p, e))
