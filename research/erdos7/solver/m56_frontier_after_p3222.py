"""M56: exact minimal exponent frontier after M55 closes P3222.

M54 had three directions P422, P332, P3222.  Closing P3222 leaves P422 and
P332, while the four-repeated-coordinate branch advances to
P32222=(3,2,2,2,2,1).  These three are exactly the new minimal antichain.
"""
from __future__ import annotations

from m26_minimal_frontier import sorted_profile
from m54_three_repeated_frontier import P422, P332, P3222, profile_closed_after_m53

P32222 = (3, 2, 2, 2, 2, 1)
MINIMAL_FRONTIER = (P422, P332, P32222)


def profile_closed_after_m55(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m53(p):
        return True
    return all(a <= b for a, b in zip(p, P3222))


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m55(p):
        return None

    assert sum(a >= 2 for a in p) >= 3
    assert p[0] >= 3

    if p[3] == 1:
        # Exactly three repeated coordinates: the two old M54 directions.
        if p[1] >= 3:
            out = P332
        else:
            assert p[1] == 2 and p[2] == 2 and p[0] >= 4
            out = P422
    else:
        # At least four repeated coordinates.
        if p[0] >= 4:
            out = P422
        elif p[1] >= 3:
            out = P332
        else:
            assert p[0] == 3 and p[1] == p[2] == p[3] == 2
            # If a5 were 1 we would lie below the newly closed P3222 majorant.
            assert p[4] >= 2
            out = P32222

    assert all(a <= b for a, b in zip(out, p))
    return out


def frontier_audit() -> dict:
    assert all(not profile_closed_after_m55(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p

    assert profile_closed_after_m55(P3222)
    assert minimal_frontier_dominator((9,2,2,1,1,1)) == P422
    assert minimal_frontier_dominator((7,6,2,1,1,1)) == P332
    assert minimal_frontier_dominator((3,2,2,2,2,2)) == P32222
    assert minimal_frontier_dominator((4,2,2,2,2,1)) == P422
    assert minimal_frontier_dominator((3,3,2,2,2,1)) == P332
    return {
        "minimal_frontier": MINIMAL_FRONTIER,
        "frontier_size": 3,
        "new_four_repeat_direction": P32222,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER", "P32222", "frontier_audit",
    "minimal_frontier_dominator", "profile_closed_after_m55",
]
