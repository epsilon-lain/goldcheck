"""M51: exact minimal exponent frontier after M50.

M49 exposed P63=(6,3,1,1,1,1) and P54=(5,4,1,1,1,1) on the a3=1
branch.  M50 closes every (A,3,1,1,1,1) with A>=6, while smaller A on that
branch were already closed.  Thus the entire a2=3,a3=1 branch disappears.
The remaining minimal antichain has four profiles:

    (5,4,1,1,1,1),
    (4,2,2,1,1,1),
    (3,3,2,1,1,1),
    (3,2,2,2,1,1).
"""
from __future__ import annotations

from m26_minimal_frontier import sorted_profile
from m42_p322_profile_closure import P332, P3222, P422
from m49_p53_profile_closure import P54, profile_closed_after_m49
from m50_infinite_pA3_ray import ray_audit

MINIMAL_FRONTIER = (P54, P422, P332, P3222)


def profile_closed_after_m50(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m49(p):
        return True
    # M50 closes the whole a2=3,a3=1 ray above A=6; P53 and older downsets
    # already cover the smaller first exponents.
    if p[1:] == (3, 1, 1, 1, 1):
        return True
    return False


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m50(p):
        return None

    assert p[1] >= 2
    if p[2] == 1:
        # a2=2 and a2=3 branches are both completely closed.
        assert p[1] >= 4
        # P44 closes a1<=4, so an outside profile has a1>=5.
        assert p[0] >= 5
        out = P54
    else:
        assert p[2] >= 2 and p[0] >= 3
        if p[3] >= 2:
            out = P3222
        elif p[1] >= 3:
            out = P332
        else:
            assert p[1] == 2 and p[2] == 2 and p[0] >= 4
            out = P422

    assert all(a <= b for a, b in zip(out, p))
    return out


def frontier_audit() -> dict:
    ray = ray_audit()
    assert ray["all_ray_numbers_noncovering"]
    assert all(not profile_closed_after_m50(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))

    assert minimal_frontier_dominator(P54) == P54
    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P332) == P332
    assert minimal_frontier_dominator(P3222) == P3222

    for A in (4, 5, 6, 10, 100):
        assert profile_closed_after_m50((A, 3, 1, 1, 1, 1))
    assert minimal_frontier_dominator((9, 7, 1, 1, 1, 1)) == P54
    assert minimal_frontier_dominator((7, 2, 2, 1, 1, 1)) == P422
    assert minimal_frontier_dominator((5, 4, 2, 1, 1, 1)) == P332
    assert minimal_frontier_dominator((4, 3, 2, 2, 1, 1)) == P3222

    return {
        "minimal_frontier": MINIMAL_FRONTIER,
        "frontier_size": 4,
        "former_A3_branch_closed": True,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER",
    "frontier_audit",
    "minimal_frontier_dominator",
    "profile_closed_after_m50",
]
