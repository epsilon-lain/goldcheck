"""M38: close profile (5,2,1,1,1,1) and recompute the minimal exponent frontier.

M26 reduces the entire profile to seven explicit direct-bound seeds.  M35
eliminates five canonical seeds, M36 eliminates the exceptional placement with
7^2, and M37 eliminates the last canonical p=17 seed.  Hence every member of
the profile is noncovering.

Adding the resulting P52 down-set to the already closed M22/M33 regions does
*not* leave only P322: two immediate successor directions appear.  The exact
componentwise-minimal sorted six-prime exponent profiles still outside the
current exclusion down-set are

    (6,2,1,1,1,1),
    (5,3,1,1,1,1),
    (3,2,2,1,1,1).

This module records that structural correction explicitly.
"""
from __future__ import annotations

from m26_minimal_frontier import P52, P322, SEEDS, family_number, sorted_profile
from m34_frontier_after_m33 import profile_closed_after_m33
from m35_quantitative_lifting import UNRESOLVED_CANONICAL, lifted_seed_audit
from m36_a5_exceptional_goodness import N as M36_EXCEPTIONAL
from m37_p17_factorial_lift import N5 as M37_FINAL_CANONICAL

P62 = (6, 2, 1, 1, 1, 1)
P53 = (5, 3, 1, 1, 1, 1)
MINIMAL_FRONTIER = (P62, P53, P322)


def profile_closed_after_m37(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m33(p):
        return True
    return all(a <= b for a, b in zip(p, P52))


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m37(p):
        return None

    # Outside M22/M33/P52, we still have a_2>=2.
    assert p[1] >= 2
    if p[2] >= 2:
        # Failure of the all-<=2 M22 zone forces a_1>=3.
        assert p[0] >= 3
        out = P322
    elif p[1] >= 3:
        # Here a_3=1.  If a_1<=4, the profile lies below the closed P44
        # majorant, so an outside profile must have a_1>=5.
        assert p[0] >= 5
        out = P53
    else:
        # Here a_2=2 and a_3=1.  Failure of the newly closed P52 down-set
        # forces a_1>=6.
        assert p[1] == 2 and p[2] == 1 and p[0] >= 6
        out = P62

    assert all(a <= b for a, b in zip(out, p))
    return out


def p52_seed_closure_audit() -> dict:
    m35 = lifted_seed_audit()
    lifted = set(m35["lifted_numbers"])
    final_canonical = M37_FINAL_CANONICAL
    exceptional = M36_EXCEPTIONAL

    seed_numbers = {family_number(primes, exponents) for primes, exponents in SEEDS[P52]}
    killed = lifted | {final_canonical, exceptional}
    assert len(SEEDS[P52]) == 7
    assert len(lifted) == 5
    assert UNRESOLVED_CANONICAL == final_canonical
    assert seed_numbers == killed
    return {
        "profile": P52,
        "m26_seed_count": len(seed_numbers),
        "m35_lifted_count": len(lifted),
        "m36_exceptional": exceptional,
        "m37_final_canonical": final_canonical,
        "all_m26_seeds_excluded": True,
    }


def frontier_audit() -> dict:
    closure = p52_seed_closure_audit()
    assert all(not profile_closed_after_m37(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))

    assert minimal_frontier_dominator(P62) == P62
    assert minimal_frontier_dominator(P53) == P53
    assert minimal_frontier_dominator(P322) == P322
    assert minimal_frontier_dominator((9, 2, 1, 1, 1, 1)) == P62
    assert minimal_frontier_dominator((8, 5, 1, 1, 1, 1)) == P53
    assert minimal_frontier_dominator((4, 3, 2, 1, 1, 1)) == P322
    assert profile_closed_after_m37(P52)
    assert profile_closed_after_m37((4, 4, 1, 1, 1, 1))

    return {
        "p52_closure": closure,
        "minimal_frontier": MINIMAL_FRONTIER,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER",
    "P53",
    "P62",
    "frontier_audit",
    "minimal_frontier_dominator",
    "p52_seed_closure_audit",
    "profile_closed_after_m37",
]
