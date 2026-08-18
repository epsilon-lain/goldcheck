"""M43: exact McNew--Setty reduction for profile (6,2,1,1,1,1).

The M42 frontier exposes P62=(6,2,1,1,1,1).  Universal coordinate
monotonicity from M22 reduces this whole infinite prime family to eight exact
survivor seeds: seven canonical placements with the square on prime 5 and one
exceptional placement with the square on prime 7.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import permutations

from m22_universal_direct_zones import universal_monotonicity_gap
from m26_minimal_frontier import direct_bound, family_number

MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
P62 = (6, 2, 1, 1, 1, 1)
P612 = (6, 1, 2, 1, 1, 1)
EXCEPTIONAL_PLACEMENTS = (P62, P612)

EXPECTED_MINIMAL_VALUES = {
    P62: Fraction(18573409, 18243225),
    P612: Fraction(8535517, 8513505),
}
EXPECTED_MAX_DIRECTLY_KILLED = (
    (6, 1, 1, 2, 1, 1),
    Fraction(678016499, 682296615),
)

SEEDS = (
    *((primes, P62) for primes in (
        (3, 5, 7, 11, 13, 17),
        (3, 5, 7, 11, 13, 19),
        (3, 5, 7, 11, 13, 23),
        (3, 5, 7, 11, 13, 29),
        (3, 5, 7, 11, 13, 31),
        (3, 5, 7, 11, 13, 37),
        (3, 5, 7, 11, 17, 19),
    )),
    ((3, 5, 7, 11, 13, 17), P612),
)

KILL_ANCHORS = {
    P62: (
        (5, 7, 11, 13, 17, 19),
        (3, 7, 11, 13, 17, 19),
        (3, 5, 11, 13, 17, 19),
        (3, 5, 7, 13, 17, 19),
        (3, 5, 7, 11, 13, 41),
        (3, 5, 7, 11, 17, 23),
        (3, 5, 7, 11, 19, 23),
    ),
    P612: (
        (5, 7, 11, 13, 17, 19),
        (3, 7, 11, 13, 17, 19),
        (3, 5, 11, 13, 17, 19),
        (3, 5, 7, 13, 17, 19),
        (3, 5, 7, 11, 17, 19),
        (3, 5, 7, 11, 13, 19),
    ),
}


def placement_scan() -> dict:
    assignments = tuple(sorted(set(permutations(P62))))
    assert len(assignments) == 30
    values = {a: direct_bound(MINIMAL_ODD_PRIMES, a) for a in assignments}
    survivors = tuple(a for a in assignments if values[a] >= 1)
    assert set(survivors) == set(EXCEPTIONAL_PLACEMENTS)
    assert {a: values[a] for a in survivors} == EXPECTED_MINIMAL_VALUES
    killed = {a: v for a, v in values.items() if a not in survivors}
    amax = max(killed, key=killed.get)
    vmax = killed[amax]
    assert (amax, vmax) == EXPECTED_MAX_DIRECTLY_KILLED
    assert vmax < 1
    return {
        "assignment_count": len(assignments),
        "exceptional_placements": survivors,
        "max_directly_killed_assignment": amax,
        "max_directly_killed_R": vmax,
    }


def direct_reduction_branch(primes: tuple[int, ...], exponents: tuple[int, ...]) -> str:
    if len(primes) != 6 or tuple(sorted(primes)) != tuple(primes) or len(set(primes)) != 6:
        raise ValueError("need six increasing distinct primes")
    if tuple(sorted(exponents, reverse=True)) != P62:
        raise ValueError("wrong exponent profile")
    assert universal_monotonicity_gap() > 0

    exp = tuple(exponents)
    if exp not in EXCEPTIONAL_PLACEMENTS:
        base = direct_bound(MINIMAL_ODD_PRIMES, exp)
        assert base <= EXPECTED_MAX_DIRECTLY_KILLED[1] < 1
        assert direct_bound(tuple(primes), exp) <= base
        return "McNew-Setty-placement"

    item = (tuple(primes), exp)
    if item in SEEDS:
        assert direct_bound(*item) >= 1
        return "seed"

    dominating = [
        anchor for anchor in KILL_ANCHORS[exp]
        if all(p >= a for p, a in zip(primes, anchor))
    ]
    assert dominating
    anchor = min(dominating)
    assert direct_bound(anchor, exp) < 1
    assert direct_bound(tuple(primes), exp) <= direct_bound(anchor, exp)
    return "McNew-Setty-anchor"


def frontier_audit() -> dict:
    scan = placement_scan()
    assert len(SEEDS) == 8
    for primes, exp in SEEDS:
        assert direct_reduction_branch(primes, exp) == "seed"
    for exp, anchors in KILL_ANCHORS.items():
        assert all(direct_bound(anchor, exp) < 1 for anchor in anchors)
    return {
        "profile": P62,
        "placement_scan": scan,
        "seed_count": len(SEEDS),
        "seed_numbers": tuple(family_number(primes, exp) for primes, exp in SEEDS),
        "verified": True,
    }


__all__ = [
    "KILL_ANCHORS",
    "P612",
    "P62",
    "SEEDS",
    "direct_reduction_branch",
    "frontier_audit",
    "placement_scan",
]
