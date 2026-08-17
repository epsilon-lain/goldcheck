"""Tests for the six-prime profile-seed computation (Milestone 9, M9.2)."""

from fractions import Fraction

from omega6_seed import (
    omega6_support_pool,
    omega6_survivors,
    smallest_omega6_survivor,
)


def test_omega6_support_pool_is_exact_and_contains_the_corner():
    pool = omega6_support_pool()
    assert len(pool) == 37
    assert pool[0] == (3, 5, 7, 11, 13, 17)
    assert (3, 5, 7, 13, 17, 19) in pool
    assert all(a < b for support in pool for a, b in zip(support, support[1:]))


def test_first_six_prime_seed():
    n, support, exps, R = smallest_omega6_survivor()
    assert n == 11_486_475
    assert support == (3, 5, 7, 11, 13, 17)
    assert exps == (3, 2, 1, 1, 1, 1)
    assert R == Fraction(677674, 675675)


def test_first_few_survivors_are_ordered():
    rows = omega6_survivors(50_000_000)
    ns = [row[0] for row in rows]
    assert ns == sorted(ns)
    assert ns[0] == 11_486_475
    assert ns[1] == 34_459_425
    assert ns[2] == 38_513_475
    assert ns[3] == 46_621_575
