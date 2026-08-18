"""M34: exact minimal six-prime exponent frontier after M33.

M33 closes the whole (4,4,1,1,1,1) profile.  Together with M22's two broad
regions, the componentwise-minimal sorted six-prime profiles still outside the
current exclusion down-set are now exactly

    (5,2,1,1,1,1),
    (3,2,2,1,1,1).

M26 already reduced those two infinite prime families to 7 and 12 explicit
McNew--Setty survivor seeds respectively, so the finite direct-bound frontier
drops from 30 seeds to 19.
"""
from __future__ import annotations

from m26_minimal_frontier import P52, P322, SEEDS, sorted_profile

M33_PROFILE_MAJORANT = (4, 4, 1, 1, 1, 1)
MINIMAL_FRONTIER = (P52, P322)


def profile_closed_after_m33(profile) -> bool:
    p = sorted_profile(profile)
    if p[0] <= 2:
        return True
    if p[1] == 1:
        return True
    return all(a <= b for a, b in zip(p, M33_PROFILE_MAJORANT))


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m33(p):
        return None
    assert p[1] >= 2
    if p[0] >= 5:
        out = P52
    else:
        # Here p_1,p_2 <=4.  Failure of the M33 down-set forces p_3>=2;
        # failure of the all-<=2 M22 region then forces p_1>=3.
        assert p[2] >= 2 and p[0] >= 3
        out = P322
    assert all(a <= b for a, b in zip(out, p))
    return out


def frontier_audit() -> dict:
    assert all(not profile_closed_after_m33(p) for p in MINIMAL_FRONTIER)
    assert not all(a <= b for a, b in zip(P52, P322))
    assert not all(a <= b for a, b in zip(P322, P52))

    # Representative boundary checks in every way to leave the closed region.
    assert minimal_frontier_dominator((5, 2, 1, 1, 1, 1)) == P52
    assert minimal_frontier_dominator((9, 4, 1, 1, 1, 1)) == P52
    assert minimal_frontier_dominator((4, 3, 2, 1, 1, 1)) == P322
    assert minimal_frontier_dominator((3, 2, 2, 2, 1, 1)) == P322
    assert profile_closed_after_m33((4, 4, 1, 1, 1, 1))
    assert profile_closed_after_m33((2, 2, 2, 2, 2, 2))
    assert profile_closed_after_m33((20, 1, 1, 1, 1, 1))

    seed_counts = {p: len(SEEDS[p]) for p in MINIMAL_FRONTIER}
    assert seed_counts == {P52: 7, P322: 12}
    assert sum(seed_counts.values()) == 19
    return {
        "minimal_frontier": MINIMAL_FRONTIER,
        "seed_counts": seed_counts,
        "total_direct_bound_seeds": 19,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER",
    "M33_PROFILE_MAJORANT",
    "frontier_audit",
    "minimal_frontier_dominator",
    "profile_closed_after_m33",
]
