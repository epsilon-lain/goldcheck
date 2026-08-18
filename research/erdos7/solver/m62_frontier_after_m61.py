"""M62: exact minimal exponent frontier after closing P32222 in M61.

M59 left four minimal sorted six-prime exponent profiles.  M61 closes
P32222=(3,2,2,2,2,1).  Adding its down-set replaces that branch by the single
immediate successor P322222=(3,2,2,2,2,2); the other three M59 branches stay
unchanged.
"""
from __future__ import annotations

from m26_minimal_frontier import sorted_profile
from m59_frontier_after_p332 import (
    P422, P333, P3322, P32222, profile_closed_after_m58,
)

P322222 = (3, 2, 2, 2, 2, 2)
MINIMAL_FRONTIER = (P422, P333, P3322, P322222)


def profile_closed_after_m61(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m58(p):
        return True
    return all(a <= b for a, b in zip(p, P32222))


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m61(p):
        return None

    assert sum(a >= 2 for a in p) >= 3
    assert p[0] >= 3

    if p[0] >= 4:
        out = P422
    else:
        assert p[0] == 3
        if p[1] >= 3:
            if p[2] >= 3:
                out = P333
            else:
                assert p[2] == 2
                assert p[3] >= 2
                out = P3322
        else:
            assert p[1] == p[2] == 2
            # M61 closes every profile below (3,2,2,2,2,1).  Hence an open
            # profile in this branch must repeat the sixth coordinate as well.
            assert p[3] == p[4] == p[5] == 2
            out = P322222

    assert all(a <= b for a, b in zip(out, p))
    return out


def frontier_audit() -> dict:
    assert profile_closed_after_m61(P32222)
    assert not profile_closed_after_m61(P322222)
    assert all(not profile_closed_after_m61(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))
    assert minimal_frontier_dominator((9,2,2,1,1,1)) == P422
    assert minimal_frontier_dominator((3,3,3,2,1,1)) == P333
    assert minimal_frontier_dominator((3,3,2,2,2,1)) == P3322
    assert minimal_frontier_dominator((3,2,2,2,2,2)) == P322222
    return {"minimal_frontier": MINIMAL_FRONTIER, "frontier_size": 4, "verified": True}


__all__ = [
    "MINIMAL_FRONTIER", "P322222", "P3322", "P333", "P422",
    "frontier_audit", "minimal_frontier_dominator", "profile_closed_after_m61",
]
