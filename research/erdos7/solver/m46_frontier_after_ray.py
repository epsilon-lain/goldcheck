"""M46: exact minimal exponent frontier after the M45 infinite-ray closure.

M42 left five minimal directions.  M45 removes not just P62 but every profile
(A,2,1,1,1,1) with A>=6.  Therefore the entire a2=2,a3=1 branch disappears.
The exact remaining minimal antichain is

    (5,3,1,1,1,1),
    (4,2,2,1,1,1),
    (3,3,2,1,1,1),
    (3,2,2,2,1,1).
"""
from __future__ import annotations

from m26_minimal_frontier import sorted_profile
from m42_p322_profile_closure import P332, P3222, P422, profile_closed_after_m41
from m45_infinite_pA2_ray import ray_audit

P53 = (5, 3, 1, 1, 1, 1)
MINIMAL_FRONTIER = (P53, P422, P332, P3222)


def profile_closed_after_m45(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m41(p):
        return True
    # M45 closes the complete branch with exactly one exponent above 2 and
    # second exponent 2; downward closure then covers every (A,2,1,1,1,1)
    # with A>=6 (and the smaller A were already closed).
    if p[1:] == (2, 1, 1, 1, 1):
        return True
    return False


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m45(p):
        return None

    assert p[1] >= 2
    if p[2] == 1:
        # The a2=2 branch is now entirely closed, so necessarily a2>=3.
        assert p[1] >= 3
        # Failure of the P44 down-set forces a1>=5.
        assert p[0] >= 5
        out = P53
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
    assert all(not profile_closed_after_m45(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))

    assert minimal_frontier_dominator(P53) == P53
    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P332) == P332
    assert minimal_frontier_dominator(P3222) == P3222

    # The former P62 branch, including arbitrarily large first exponents, is closed.
    for A in (6, 7, 20, 100):
        assert profile_closed_after_m45((A, 2, 1, 1, 1, 1))
    assert minimal_frontier_dominator((8, 5, 1, 1, 1, 1)) == P53
    assert minimal_frontier_dominator((7, 2, 2, 1, 1, 1)) == P422
    assert minimal_frontier_dominator((5, 4, 2, 1, 1, 1)) == P332
    assert minimal_frontier_dominator((4, 3, 2, 2, 1, 1)) == P3222

    return {
        "minimal_frontier": MINIMAL_FRONTIER,
        "frontier_size": len(MINIMAL_FRONTIER),
        "former_A2_branch_closed": True,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER",
    "P53",
    "frontier_audit",
    "minimal_frontier_dominator",
    "profile_closed_after_m45",
]
