"""M42: close profile (3,2,2,1,1,1) and recompute the minimal frontier.

M26 reduced P322 to twelve explicit seeds.  M40 excludes the six exceptional
placements and M41 excludes the six canonical placements, so the whole profile
is noncovering by the M26 direct-bound/monotonicity reduction.

Adding the P322 down-set to the previously closed M22/M33/P52 regions exposes
five new componentwise-minimal sorted exponent directions:

    (6,2,1,1,1,1),
    (5,3,1,1,1,1),
    (4,2,2,1,1,1),
    (3,3,2,1,1,1),
    (3,2,2,2,1,1).
"""
from __future__ import annotations

from m26_minimal_frontier import P322, SEEDS, family_number, sorted_profile
from m38_p52_profile_closure import P53, P62, profile_closed_after_m37
from m40_p322_exceptional_lifts import exceptional_seed_numbers
from m41_p322_canonical_weighted import canonical_seed_numbers

P422 = (4, 2, 2, 1, 1, 1)
P332 = (3, 3, 2, 1, 1, 1)
P3222 = (3, 2, 2, 2, 1, 1)
MINIMAL_FRONTIER = (P62, P53, P422, P332, P3222)


def profile_closed_after_m41(profile) -> bool:
    p = sorted_profile(profile)
    if profile_closed_after_m37(p):
        return True
    return all(a <= b for a, b in zip(p, P322))


def minimal_frontier_dominator(profile):
    p = sorted_profile(profile)
    if profile_closed_after_m41(p):
        return None

    assert p[1] >= 2
    if p[2] == 1:
        # Same two branches already exposed after P52 closure.
        if p[1] >= 3:
            assert p[0] >= 5
            out = P53
        else:
            assert p[1] == 2 and p[0] >= 6
            out = P62
    else:
        # Here a3>=2.  Failure of the all-<=2 M22 region forces a1>=3.
        assert p[0] >= 3
        if p[3] >= 2:
            out = P3222
        elif p[1] >= 3:
            out = P332
        else:
            # a2=a3=2 and a4=1.  Failure of the newly closed P322 down-set
            # forces a1>=4.
            assert p[1] == 2 and p[2] == 2 and p[0] >= 4
            out = P422

    assert all(a <= b for a, b in zip(out, p))
    return out


def p322_seed_closure_audit() -> dict:
    seed_numbers = {family_number(primes, exponents) for primes, exponents in SEEDS[P322]}
    exceptional = set(exceptional_seed_numbers())
    canonical = set(canonical_seed_numbers())
    assert len(seed_numbers) == 12
    assert len(exceptional) == 6
    assert len(canonical) == 6
    assert exceptional.isdisjoint(canonical)
    assert seed_numbers == exceptional | canonical
    return {
        "profile": P322,
        "m26_seed_count": 12,
        "m40_exceptional_count": 6,
        "m41_canonical_count": 6,
        "all_m26_seeds_excluded": True,
    }


def frontier_audit() -> dict:
    closure = p322_seed_closure_audit()
    assert all(not profile_closed_after_m41(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p != q:
                assert not all(a <= b for a, b in zip(p, q))

    assert minimal_frontier_dominator(P62) == P62
    assert minimal_frontier_dominator(P53) == P53
    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P332) == P332
    assert minimal_frontier_dominator(P3222) == P3222

    assert minimal_frontier_dominator((9, 2, 1, 1, 1, 1)) == P62
    assert minimal_frontier_dominator((8, 5, 1, 1, 1, 1)) == P53
    assert minimal_frontier_dominator((7, 2, 2, 1, 1, 1)) == P422
    assert minimal_frontier_dominator((5, 4, 2, 1, 1, 1)) == P332
    assert minimal_frontier_dominator((4, 3, 2, 2, 1, 1)) == P3222

    assert profile_closed_after_m41(P322)
    assert profile_closed_after_m41((5, 2, 1, 1, 1, 1))
    assert profile_closed_after_m41((4, 4, 1, 1, 1, 1))
    return {
        "p322_closure": closure,
        "minimal_frontier": MINIMAL_FRONTIER,
        "verified": True,
    }


__all__ = [
    "MINIMAL_FRONTIER",
    "P332",
    "P3222",
    "P422",
    "frontier_audit",
    "minimal_frontier_dominator",
    "p322_seed_closure_audit",
    "profile_closed_after_m41",
]
