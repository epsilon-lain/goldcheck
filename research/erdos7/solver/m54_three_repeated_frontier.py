"""M54: exact exponent frontier after M53.

M53 closes every six-prime exponent vector with exactly two repeated prime
coordinates.  Earlier M22 regions already close zero or one repeated coordinate.
Therefore every remaining six-prime candidate has at least three exponents >=2.
Combining this with the closed P322 down-set gives exactly three componentwise-
minimal sorted directions:

    (4,2,2,1,1,1),
    (3,3,2,1,1,1),
    (3,2,2,2,1,1).
"""
from __future__ import annotations

from m26_minimal_frontier import P322, sorted_profile

P422 = (4, 2, 2, 1, 1, 1)
P332 = (3, 3, 2, 1, 1, 1)
P3222 = (3, 2, 2, 2, 1, 1)
MINIMAL_FRONTIER = (P422, P332, P3222)


def profile_closed_after_m53(profile) -> bool:
    p = sorted_profile(profile)
    repeated_count = sum(a >= 2 for a in p)
    if repeated_count <= 2:
        # zero/one repeated coordinates are in M22's direct/downward region;
        # exactly two are M53.
        return True
    # M42 closes P322, so every profile componentwise below it is closed.
    if all(a <= b for a, b in zip(p, P322)):
        return True
    return False


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m53(p):
        return None

    assert p[2] >= 2  # at least three repeated coordinates
    assert p[0] >= 3  # otherwise all exponents <=2, already closed by M22

    if p[3] >= 2:
        out = P3222
    elif p[1] >= 3:
        out = P332
    else:
        # Exactly three repeated coordinates with second and third equal 2.
        # Failure of the closed P322 down-set forces the first exponent >=4.
        assert p[1] == 2 and p[2] == 2 and p[0] >= 4
        out = P422

    assert all(a <= b for a, b in zip(out, p))
    return out


def frontier_audit() -> dict:
    assert all(not profile_closed_after_m53(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))

    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P332) == P332
    assert minimal_frontier_dominator(P3222) == P3222

    # Any number with at most two repeated prime coordinates is now closed.
    assert profile_closed_after_m53((100, 100, 1, 1, 1, 1))
    assert profile_closed_after_m53((100, 1, 1, 1, 1, 1))
    assert profile_closed_after_m53((1, 1, 1, 1, 1, 1))

    # Representative ways to leave the closed region.
    assert minimal_frontier_dominator((9, 2, 2, 1, 1, 1)) == P422
    assert minimal_frontier_dominator((7, 6, 2, 1, 1, 1)) == P332
    assert minimal_frontier_dominator((5, 4, 3, 2, 1, 1)) == P3222

    return {
        "minimal_frontier": MINIMAL_FRONTIER,
        "frontier_size": 3,
        "every_remaining_profile_has_at_least_three_repeated_coordinates": True,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER",
    "P332",
    "P3222",
    "P422",
    "frontier_audit",
    "minimal_frontier_dominator",
    "profile_closed_after_m53",
]
