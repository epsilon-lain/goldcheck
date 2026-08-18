"""M65: minimal exponent frontier after closing P322222 in M64.

M62 had four minimal directions.  Since M64 closes (3,2,2,2,2,2), that whole
branch disappears rather than spawning a new incomparable successor: increasing
the leading 3 reaches the P422 branch, while increasing any other exponent to
3 reaches P3322 or P333.  The exact frontier therefore has only three members.
"""
from __future__ import annotations

from m26_minimal_frontier import sorted_profile
from m59_frontier_after_p332 import P422, P333, P3322
from m62_frontier_after_m61 import P322222, profile_closed_after_m61

MINIMAL_FRONTIER = (P422, P333, P3322)


def profile_closed_after_m64(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m61(p):
        return True
    return all(a <= b for a,b in zip(p,P322222))


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m64(p):
        return None
    assert p[0] >= 3
    if p[0] >= 4:
        out = P422
    else:
        assert p[0] == 3
        # If p2=2 then the entire profile lies below the newly closed
        # (3,2,2,2,2,2), so an open profile must have p2>=3.
        assert p[1] >= 3
        if p[2] >= 3:
            out = P333
        else:
            assert p[2] == 2
            # If p4=1 this lies below the already closed P332 majorant.
            assert p[3] >= 2
            out = P3322
    assert all(a <= b for a,b in zip(out,p))
    return out


def frontier_audit() -> dict:
    assert profile_closed_after_m64(P322222)
    assert all(not profile_closed_after_m64(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a,b in zip(p,q))
    assert minimal_frontier_dominator((9,2,2,1,1,1)) == P422
    assert minimal_frontier_dominator((3,3,3,2,2,1)) == P333
    assert minimal_frontier_dominator((3,3,2,2,2,2)) == P3322
    assert profile_closed_after_m64((3,2,2,2,2,2))
    return {"minimal_frontier":MINIMAL_FRONTIER,"frontier_size":3,"verified":True}


__all__ = [
    "MINIMAL_FRONTIER","P3322","P333","P422","frontier_audit",
    "minimal_frontier_dominator","profile_closed_after_m64",
]
