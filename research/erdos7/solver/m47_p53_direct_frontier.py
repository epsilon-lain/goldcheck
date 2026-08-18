"""M47: exact McNew--Setty reduction for profile (5,3,1,1,1,1).

The M46 frontier exposes P53.  At the minimal odd primes only three exponent
placements survive.  Universal coordinate monotonicity then reduces the whole
infinite prime family to sixteen explicit seeds, with exact R<1 boundary
anchors covering every other prime tuple.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import permutations

from m22_universal_direct_zones import universal_monotonicity_gap
from m26_minimal_frontier import direct_bound, family_number

MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
P53 = (5, 3, 1, 1, 1, 1)
P35 = (3, 5, 1, 1, 1, 1)
P513 = (5, 1, 3, 1, 1, 1)
SURVIVING_PLACEMENTS = (P35, P513, P53)

EXPECTED_MINIMAL_VALUES = {
    P35: Fraction(28445708, 28153125),
    P513: Fraction(338863268, 337702365),
    P53: Fraction(3455656, 3378375),
}

SEEDS = (
    *((primes, P35) for primes in (
        (3, 5, 7, 11, 13, 17),
        (3, 5, 7, 11, 13, 19),
        (3, 5, 7, 11, 13, 23),
    )),
    ((3, 5, 7, 11, 13, 17), P513),
    *((primes, P53) for primes in (
        (3, 5, 7, 11, 13, 17),
        (3, 5, 7, 11, 13, 19),
        (3, 5, 7, 11, 13, 23),
        (3, 5, 7, 11, 13, 29),
        (3, 5, 7, 11, 13, 31),
        (3, 5, 7, 11, 13, 37),
        (3, 5, 7, 11, 13, 41),
        (3, 5, 7, 11, 13, 43),
        (3, 5, 7, 11, 13, 47),
        (3, 5, 7, 11, 13, 53),
        (3, 5, 7, 11, 17, 19),
        (3, 5, 7, 11, 17, 23),
    )),
)

KILL_ANCHORS = {
    P35: {
        (3, 5, 7, 11, 13, 29): Fraction(90398852, 90715625),
        (3, 5, 7, 11, 17, 19): Fraction(696710992, 699496875),
    },
    P513: {
        (3, 5, 7, 11, 13, 19): Fraction(226419880, 226459233),
    },
    P53: {
        (3, 5, 7, 11, 13, 59): Fraction(597589624, 597972375),
        (3, 5, 7, 11, 17, 29): Fraction(383632952, 384355125),
        (3, 5, 7, 11, 19, 23): Fraction(340574284, 340696125),
        (3, 5, 7, 13, 17, 19): Fraction(52514648, 52518375),
    },
}


def placement_scan() -> dict:
    assignments = tuple(sorted(set(permutations(P53))))
    assert len(assignments) == 30
    values = {a: direct_bound(MINIMAL_ODD_PRIMES, a) for a in assignments}
    survivors = {a: v for a, v in values.items() if v >= 1}
    assert survivors == EXPECTED_MINIMAL_VALUES
    killed = {a: v for a, v in values.items() if a not in survivors}
    vmax = max(killed.values())
    assert vmax < 1
    return {
        "assignment_count": 30,
        "surviving_placements": survivors,
        "max_directly_killed_R": vmax,
        "verified": True,
    }


def direct_reduction_branch(primes: tuple[int, ...], exponents: tuple[int, ...]) -> str:
    if len(primes) != 6 or tuple(sorted(primes)) != primes or len(set(primes)) != 6:
        raise ValueError("need six increasing distinct primes")
    if tuple(sorted(exponents, reverse=True)) != P53:
        raise ValueError("wrong exponent profile")
    assert universal_monotonicity_gap() > 0

    exp = tuple(exponents)
    if exp not in SURVIVING_PLACEMENTS:
        base = direct_bound(MINIMAL_ODD_PRIMES, exp)
        assert base < 1
        assert direct_bound(primes, exp) <= base
        return "McNew-Setty-placement"

    item = (primes, exp)
    if item in SEEDS:
        assert direct_bound(primes, exp) >= 1
        return "seed"

    dominating = [
        anchor for anchor in KILL_ANCHORS[exp]
        if all(p >= a for p, a in zip(primes, anchor))
    ]
    assert dominating
    anchor = min(dominating)
    assert direct_bound(anchor, exp) == KILL_ANCHORS[exp][anchor] < 1
    assert direct_bound(primes, exp) <= direct_bound(anchor, exp)
    return "McNew-Setty-anchor"


def frontier_audit() -> dict:
    scan = placement_scan()
    assert len(SEEDS) == 16
    counts = {exp: sum(1 for _, e in SEEDS if e == exp) for exp in SURVIVING_PLACEMENTS}
    assert counts == {P35: 3, P513: 1, P53: 12}
    for exp, anchors in KILL_ANCHORS.items():
        for anchor, expected in anchors.items():
            assert direct_bound(anchor, exp) == expected < 1
    for primes, exp in SEEDS:
        assert direct_reduction_branch(primes, exp) == "seed"
    return {
        "profile": P53,
        "placement_scan": scan,
        "seed_count": 16,
        "seed_counts_by_placement": counts,
        "seed_numbers": tuple(family_number(primes, exp) for primes, exp in SEEDS),
        "verified": True,
    }


__all__ = [
    "KILL_ANCHORS",
    "P35",
    "P513",
    "P53",
    "SEEDS",
    "direct_reduction_branch",
    "frontier_audit",
    "placement_scan",
]
