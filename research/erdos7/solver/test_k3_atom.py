"""Tests for the exact K3 star-atom decoupling bound."""

from fractions import Fraction

from k3_atom import (
    k3_insufficient_bound,
    local_credits,
    verify_local,
)


def test_local_credits_exact():
    vals = local_credits()
    assert vals[1] == Fraction(1, 168)
    assert vals[2] == Fraction(59, 2380)
    assert vals[3] == Fraction(1, 664)
    assert vals[4] == Fraction(0)
    assert vals[5] == Fraction(0)
    assert vals[6] == Fraction(0)


def test_local_certificates_verify():
    for i in range(1, 7):
        r = verify_local(i)
        assert r["primal_feasible"]
        assert r["dual_feasible"]
        assert r["strong_duality"]


def test_k3_decoupling_bound_is_insufficient():
    r = k3_insufficient_bound()
    assert r["disjoint_pairs"] == Fraction(323, 4480)
    assert r["perfect_matchings"] == Fraction(1, 896)
    assert r["star_sum"] == Fraction(19111, 592620)
    assert r["F_K3_ub"] == Fraction(249997, 2370480)
    assert r["g_K3_lb"] == Fraction(13417473, 6321280)
    assert r["g_gt_2"]
    assert r["residual_gap_lb"] == Fraction(774913, 6321280)
