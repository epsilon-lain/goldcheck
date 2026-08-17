"""Tests for the exact diagonal lift-color law and top-layer cover primitive."""

from profile_optimizer import (
    brute_top_class_lifts,
    lift_color,
    scalar_profile_insufficient_witness,
    top_class_lifts,
    top_layer_lifts,
)


def test_diagonal_law_matches_brute_force():
    for p, a, M in ((3, 2, 1), (3, 3, 2), (5, 2, 2)):
        L = p ** (a - 1) * M
        U = set(range(L))
        for e in (d for d in range(1, M + 1) if M % d == 0):
            mod = p**a * e
            for r in range(mod):
                assert top_class_lifts(p, a, M, e, r, U) == brute_top_class_lifts(
                    p, a, M, e, r, U
                )


def test_lift_color_none_when_projection_mismatches():
    # p=3, a=2, M=1, e=1: projection modulus is 3, so bases 1 and 2 mod 3 are
    # never met by the class r=0 mod 9.
    assert lift_color(3, 2, 1, 1, 0, 1) is None
    assert lift_color(3, 2, 1, 1, 0, 2) is None
    assert lift_color(3, 2, 1, 1, 0, 0) == 0


def test_top_layer_lifts_union_and_diagonal_shape():
    # p=3, a=2, M=2, e=1: projection modulus d=3, period L=6, so the bin b=0
    # contains bases u=0 and u=3.  The class r=0 mod 9 meets base 0 at lift 0
    # and base 3 at lift 1 (a diagonal, not a horizontal row).
    U = {0, 3}
    assert top_layer_lifts(3, 2, 2, U, {1: 0}) == {(0, 0), (3, 1)}


def test_scalar_profile_is_insufficient():
    w = scalar_profile_insufficient_witness()
    assert w["profile_U1"] == w["profile_U2"] == (1, 1, 1)
    assert w["U1_coverable"] is True
    assert w["U2_coverable"] is False
    assert w["is_insufficient_witness"] is True
