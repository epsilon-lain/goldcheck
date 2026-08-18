"""M59: corrected minimal six-prime exponent frontier after M58.

Use the exact profile-level closed regions that matter here:

* M53: every profile with at most two repeated coordinates is closed;
* M22: every profile with all exponents <=2 is closed;
* M55: the down-set of (3,2,2,2,1,1) is closed;
* M58: the down-set of (3,3,2,1,1,1) is closed.

The componentwise-minimal sorted profiles outside their union are exactly

    (4,2,2,1,1,1),
    (3,3,3,1,1,1),
    (3,3,2,2,1,1),
    (3,2,2,2,2,1).

This module deliberately includes M22's all-exponents-<=2 zone explicitly;
an older frontier helper omitted that branch from its predicate even though the
mathematical theorem itself was already present.
"""
from __future__ import annotations

from m26_minimal_frontier import sorted_profile

P3222 = (3, 2, 2, 2, 1, 1)
P332 = (3, 3, 2, 1, 1, 1)
P422 = (4, 2, 2, 1, 1, 1)
P333 = (3, 3, 3, 1, 1, 1)
P3322 = (3, 3, 2, 2, 1, 1)
P32222 = (3, 2, 2, 2, 2, 1)
MINIMAL_FRONTIER = (P422, P333, P3322, P32222)


def profile_closed_after_m58(profile) -> bool:
    p = sorted_profile(profile)
    repeated_count = sum(a >= 2 for a in p)
    if repeated_count <= 2:  # M53 (and M22 for zero/one repeats)
        return True
    if p[0] <= 2:  # M22 all-exponents-at-most-two zone
        return True
    if all(a <= b for a, b in zip(p, P3222)):  # M55 down-set
        return True
    if all(a <= b for a, b in zip(p, P332)):  # M58 down-set
        return True
    return False


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m58(p):
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
                # If a4=1 the profile lies below the closed P332 majorant.
                assert p[3] >= 2
                out = P3322
        else:
            assert p[1] == 2 and p[2] == 2
            # If a5=1 the profile lies below the closed P3222 majorant.
            assert p[4] >= 2
            out = P32222

    assert all(a <= b for a, b in zip(out, p))
    return out


def frontier_audit() -> dict:
    assert profile_closed_after_m58((2,2,2,2,2,2))  # explicit M22 regression
    assert profile_closed_after_m58(P3222)
    assert profile_closed_after_m58(P332)

    assert all(not profile_closed_after_m58(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p

    assert minimal_frontier_dominator((9,2,2,1,1,1)) == P422
    assert minimal_frontier_dominator((3,3,3,2,1,1)) == P333
    assert minimal_frontier_dominator((3,3,2,2,2,1)) == P3322
    assert minimal_frontier_dominator((3,2,2,2,2,2)) == P32222
    return {
        "minimal_frontier": MINIMAL_FRONTIER,
        "frontier_size": 4,
        "m22_all_le2_regression_checked": True,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER", "P32222", "P3322", "P333", "P422",
    "frontier_audit", "minimal_frontier_dominator", "profile_closed_after_m58",
]
