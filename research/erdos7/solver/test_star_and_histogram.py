"""Tests for the star-collision certificate and the lcm-bin histogram state."""

from fractions import Fraction

from profile_histogram import (
    brute_force_joint_count,
    crt_combine,
    histogram,
    joint_intersection_count,
    top_lifts_joint_count,
)
from star_collision import (
    disjoint_pair_sum,
    star_insufficient_bound,
    star_values,
    verify_star,
    z_values,
)


def test_star_values_exact():
    vals = star_values()
    assert vals[1] == Fraction(1, 105)
    assert vals[2] == Fraction(307, 6720)
    assert vals[3] == Fraction(1, 560)
    assert vals[4] == Fraction(0)
    assert vals[5] == Fraction(0)
    assert vals[6] == Fraction(0)


def test_star_certificates_verify():
    for i in range(1, 7):
        r = verify_star(i)
        assert r["primal_ok"]
        assert r["dual_ok"]
        assert r["strong_duality"]


def test_disjoint_pair_sum_is_3e4():
    z = z_values()
    assert disjoint_pair_sum(z) == Fraction(323, 4480)


def test_star_insufficient_bound():
    r = star_insufficient_bound()
    assert r["disjoint_pair_sum"] == Fraction(323, 4480)
    assert r["star_sum"] == Fraction(383, 6720)
    assert r["F_ub"] == Fraction(347, 2688)
    assert r["g_lb"] == Fraction(2821, 1344)
    assert r["g_lb_gt_2"]
    assert r["residual_gap_lb"] == Fraction(133, 1344)


def test_histogram():
    U = [0, 3, 6, 9, 12]
    h = histogram(U, 3)
    assert h == {0: 5}
    h2 = histogram(U, 4)
    assert h2[0] == 2 and h2[1] == 1 and h2[2] == 1 and h2[3] == 1


def test_crt_combine():
    # u == 1 mod 3 and u == 3 mod 4  ->  u == 7 mod 12.
    assert crt_combine([(3, 1), (4, 3)]) == (12, 7)
    # incompatible: u == 0 mod 2 and u == 1 mod 4.
    assert crt_combine([(2, 0), (4, 1)]) is None


def test_joint_intersection_formula_bruteforce():
    U = list(range(30))
    cases = [
        [(3, 1), (4, 3)],
        [(3, 1), (4, 3), (5, 2)],
        [(2, 0), (4, 1)],
        [(6, 2), (10, 4)],
        [(6, 2), (10, 5)],
    ]
    for residues in cases:
        assert joint_intersection_count(U, residues) == brute_force_joint_count(
            U, residues
        )


def test_top_lifts_joint_count_matches_profile():
    # A top class mod p^a e meets at most one lift of each compatible base.
    U = [0, 1, 2, 3, 4, 5]
    p, a, lower_period = 3, 2, 9
    # projections mod p^{a-1}e = 3 for a single top modulus e=1.
    count = top_lifts_joint_count(U, p, a, lower_period, [(3, 0)])
    # bases u with u ≡ 0 mod 3, each contributes exactly one lift.
    assert count == len([u for u in U if u % 3 == 0])
