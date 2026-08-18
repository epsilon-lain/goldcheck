"""M67: exact minimal six-prime exponent frontier after closing P422 in M66."""
from __future__ import annotations

from m26_minimal_frontier import sorted_profile

P3222=(3,2,2,2,1,1)
P332=(3,3,2,1,1,1)
P32222=(3,2,2,2,2,1)
P322222=(3,2,2,2,2,2)
P422=(4,2,2,1,1,1)

P522=(5,2,2,1,1,1)
P432=(4,3,2,1,1,1)
P4222=(4,2,2,2,1,1)
P333=(3,3,3,1,1,1)
P3322=(3,3,2,2,1,1)
MINIMAL_FRONTIER=(P522,P432,P4222,P333,P3322)

CLOSED_MAJORANTS=(P3222,P332,P32222,P322222,P422)


def profile_closed_after_m66(profile)->bool:
    p=sorted_profile(profile)
    repeated_count=sum(a>=2 for a in p)
    if repeated_count<=2:  # M53
        return True
    if p[0]<=2:  # M22
        return True
    return any(all(a<=b for a,b in zip(p,m)) for m in CLOSED_MAJORANTS)


def minimal_frontier_dominator(profile):
    p=sorted_profile(profile)
    if profile_closed_after_m66(p):
        return None
    assert sum(a>=2 for a in p)>=3 and p[0]>=3

    if p[0]>=5:
        out=P522
    elif p[0]==4:
        assert p[2]>=2
        if p[1]>=3:
            out=P432
        else:
            assert p[1]==2
            # If a4=1 then p <= P422, which M66 closed.
            assert p[3]>=2
            out=P4222
    else:
        assert p[0]==3
        # The entire (3,2,2,2,2,2) box is closed by M64, so an open
        # profile with leading exponent 3 must have a2>=3.
        assert p[1]>=3
        if p[2]>=3:
            out=P333
        else:
            assert p[2]==2
            # If a4=1 then p <= P332, which M58 closed.
            assert p[3]>=2
            out=P3322

    assert all(a<=b for a,b in zip(out,p))
    return out


def frontier_audit()->dict:
    for m in CLOSED_MAJORANTS:
        assert profile_closed_after_m66(m)
    assert profile_closed_after_m66((2,2,2,2,2,2))
    assert all(not profile_closed_after_m66(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p)==p
        for q in MINIMAL_FRONTIER:
            if p!=q:
                assert not all(a<=b for a,b in zip(p,q))

    assert minimal_frontier_dominator((9,2,2,1,1,1))==P522
    assert minimal_frontier_dominator((4,7,2,1,1,1))==P522
    assert minimal_frontier_dominator((4,3,2,1,1,1))==P432
    assert minimal_frontier_dominator((4,2,2,3,1,1))==P432
    assert minimal_frontier_dominator((4,2,2,2,1,1))==P4222
    assert minimal_frontier_dominator((3,3,3,2,1,1))==P333
    assert minimal_frontier_dominator((3,3,2,2,2,1))==P3322
    assert profile_closed_after_m66(P422)
    assert profile_closed_after_m66(P322222)
    return {"minimal_frontier":MINIMAL_FRONTIER,"frontier_size":5,"verified":True}


__all__=[
    "MINIMAL_FRONTIER","P522","P432","P4222","P333","P3322",
    "frontier_audit","minimal_frontier_dominator","profile_closed_after_m66",
]
