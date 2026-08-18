"""M45: close the entire six-prime exponent ray (A,2,1,1,1,1), A>=6.

M44 closes A=6 with quantitative deficiency margins.  Those margins are much
stronger than mere positivity, so the deficiency recurrence propagates them to
all higher powers of 3.  Separately, the McNew--Setty direct bound is increasing
in each charge coordinate x_p(a).  Replacing the large exponent A by infinity,

    x_p(infinity)=1/(p-1),

therefore gives a uniform upper bound valid for every finite A.  At the minimal
odd primes only two exponent placements survive even in this infinite-exponent
limit, and the same eight prime tuples as M43 are the only direct survivors.
Thus the M44 seed certificates plus recurrence close the whole infinite ray.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations

from m17_infinite_family import elementary_symmetric
from m22_universal_direct_zones import universal_monotonicity_gap
from m26_minimal_frontier import family_number
from m43_p62_direct_frontier import KILL_ANCHORS, P612, P62, SEEDS
from m44_p62_profile_closure import (
    EXPECTED_CANONICAL_LIFT_GAP,
    EXPECTED_EXCEPTIONAL_LIFT_GAP,
    EXPECTED_EXCEPTIONAL_SIGMA_OVER_M,
    EXPECTED_SIGMA_OVER_M,
)

MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
EXPECTED_LIMIT_SURVIVORS = {
    (0, 1): Fraction(927, 910),
    (0, 2): Fraction(1194969, 1191190),
}
EXPECTED_LIMIT_KILLED_MAX = ((0, 3), Fraction(169203, 170170))

EXPECTED_CANONICAL_ANCHOR_LIMITS = {
    (5, 7, 11, 13, 17, 19): Fraction(6032517, 9053044),
    (3, 7, 11, 13, 17, 19): Fraction(4057479, 4526522),
    (3, 5, 11, 13, 17, 19): Fraction(130293, 135850),
    (3, 5, 7, 13, 17, 19): Fraction(1463041, 1469650),
    (3, 5, 7, 11, 13, 41): Fraction(186387, 186550),
    (3, 5, 7, 11, 17, 23): Fraction(300759, 301070),
    (3, 5, 7, 11, 19, 23): Fraction(1674381, 1682450),
}
EXPECTED_EXCEPTIONAL_ANCHOR_LIMITS = {
    (5, 7, 11, 13, 17, 19): Fraction(490647, 748748),
    (3, 7, 11, 13, 17, 19): Fraction(573005, 646646),
    (3, 5, 11, 13, 17, 19): Fraction(4737597, 5080790),
    (3, 5, 7, 13, 17, 19): Fraction(2015073, 2057510),
    (3, 5, 7, 11, 17, 19): Fraction(1720863, 1740970),
    (3, 5, 7, 11, 13, 19): Fraction(1330731, 1331330),
}


def _direct_from_x(xs: tuple[Fraction, ...]) -> Fraction:
    return (
        elementary_symmetric(xs, 1)
        - elementary_symmetric(xs, 3)
        - elementary_symmetric(xs, 4)
        + 2 * elementary_symmetric(xs, 5)
        + 9 * elementary_symmetric(xs, 6)
    )


def infinite_exponent_bound(
    primes: tuple[int, ...],
    large_position: int,
    square_position: int,
) -> Fraction:
    """Direct R with exponent infinity at one coordinate and exponent 2 at another."""
    if len(primes) != 6 or not 0 <= large_position < 6 or not 0 <= square_position < 6:
        raise ValueError("need six primes and two valid coordinate positions")
    if large_position == square_position:
        raise ValueError("large and square positions must differ")
    xs = []
    for i, p in enumerate(primes):
        if i == large_position:
            xs.append(Fraction(1, p - 1))
        elif i == square_position:
            xs.append(Fraction(1, p) + Fraction(1, p * p))
        else:
            xs.append(Fraction(1, p))
    return _direct_from_x(tuple(xs))


def limit_placement_scan() -> dict:
    assert universal_monotonicity_gap() > 0
    values = {
        (i, j): infinite_exponent_bound(MINIMAL_ODD_PRIMES, i, j)
        for i in range(6) for j in range(6) if i != j
    }
    survivors = {placement: value for placement, value in values.items() if value >= 1}
    assert survivors == EXPECTED_LIMIT_SURVIVORS
    killed = {placement: value for placement, value in values.items() if value < 1}
    pmax = max(killed, key=killed.get)
    vmax = killed[pmax]
    assert (pmax, vmax) == EXPECTED_LIMIT_KILLED_MAX
    assert vmax < 1
    return {
        "placement_count": len(values),
        "limit_survivors": survivors,
        "max_killed_placement": pmax,
        "max_killed_R": vmax,
        "verified": True,
    }


def anchor_audit() -> dict:
    canonical = {
        anchor: infinite_exponent_bound(anchor, 0, 1)
        for anchor in KILL_ANCHORS[P62]
    }
    exceptional = {
        anchor: infinite_exponent_bound(anchor, 0, 2)
        for anchor in KILL_ANCHORS[P612]
    }
    assert canonical == EXPECTED_CANONICAL_ANCHOR_LIMITS
    assert exceptional == EXPECTED_EXCEPTIONAL_ANCHOR_LIMITS
    assert all(v < 1 for v in canonical.values())
    assert all(v < 1 for v in exceptional.values())
    return {"canonical": canonical, "exceptional": exceptional, "verified": True}


def propagated_gap(A: int, exceptional: bool = False) -> Fraction:
    """Uniform normalized deficiency lower bound at exponent A>=6.

    If delta(3^a M)>=M*g_a then the deficiency recurrence gives
        g_{a+1} >= 3*g_a - sigma(M)/M.
    M44 supplies uniform base values g_6 for the canonical and exceptional
    direct-survivor branches.
    """
    if A < 6:
        raise ValueError("M45 starts at exponent six")
    if exceptional:
        g6 = EXPECTED_EXCEPTIONAL_LIFT_GAP
        s = EXPECTED_EXCEPTIONAL_SIGMA_OVER_M
    else:
        g6 = EXPECTED_CANONICAL_LIFT_GAP
        s = EXPECTED_SIGMA_OVER_M
    k = A - 6
    out = 3**k * g6 - s * Fraction(3**k - 1, 2)
    assert g6 > s / 2
    assert out >= g6 > 0
    return out


def universal_seed_templates() -> tuple[tuple[tuple[int, ...], int], ...]:
    """Return the eight prime tuples with square-position 1 or 2."""
    out = []
    for primes, exp in SEEDS:
        square_position = 1 if exp == P62 else 2
        out.append((primes, square_position))
    assert len(out) == 8
    return tuple(out)


def proof_branch(primes: tuple[int, ...], exponents: tuple[int, ...]) -> str:
    """Classify any member of the ray into direct or propagated-cert branch."""
    if len(primes) != 6 or tuple(sorted(primes)) != primes or len(set(primes)) != 6:
        raise ValueError("need six increasing distinct primes")
    if len(exponents) != 6:
        raise ValueError("need six exponents")
    profile = tuple(sorted(exponents, reverse=True))
    A = profile[0]
    if A < 6 or profile[1:] != (2, 1, 1, 1, 1):
        raise ValueError("wrong exponent ray")
    if exponents.count(A) != 1 or exponents.count(2) != 1:
        raise ValueError("ray requires unique large and square coordinates")

    large_position = exponents.index(A)
    square_position = exponents.index(2)
    limit_at_min = infinite_exponent_bound(
        MINIMAL_ODD_PRIMES, large_position, square_position
    )
    if (large_position, square_position) not in EXPECTED_LIMIT_SURVIVORS:
        assert limit_at_min <= EXPECTED_LIMIT_KILLED_MAX[1] < 1
        return "McNew-Setty-limit-placement"

    exceptional = square_position == 2
    templates = universal_seed_templates()
    if (primes, square_position) in templates:
        assert large_position == 0
        assert propagated_gap(A, exceptional=exceptional) > 0
        return "M44-recurrence-ray"

    anchors = KILL_ANCHORS[P612 if exceptional else P62]
    dominating = [
        anchor for anchor in anchors
        if all(p >= a for p, a in zip(primes, anchor))
    ]
    assert dominating
    anchor = min(dominating)
    limit = infinite_exponent_bound(anchor, 0, square_position)
    assert limit < 1
    return "McNew-Setty-limit-anchor"


def ray_audit() -> dict:
    scan = limit_placement_scan()
    anchors = anchor_audit()
    templates = universal_seed_templates()
    assert len(templates) == 8
    assert propagated_gap(6) == EXPECTED_CANONICAL_LIFT_GAP
    assert propagated_gap(6, exceptional=True) == EXPECTED_EXCEPTIONAL_LIFT_GAP
    assert propagated_gap(7) > propagated_gap(6) > 0
    assert propagated_gap(7, exceptional=True) > propagated_gap(6, exceptional=True) > 0

    # Exercise all eight templates at several exponents.
    for A in (6, 7, 10):
        for primes, square_position in templates:
            exponents = [1] * 6
            exponents[0] = A
            exponents[square_position] = 2
            assert proof_branch(primes, tuple(exponents)) == "M44-recurrence-ray"

    return {
        "profile_ray": "(A,2,1,1,1,1), A>=6",
        "limit_scan": scan,
        "anchors": anchors,
        "universal_seed_template_count": len(templates),
        "all_ray_numbers_noncovering": True,
        "verified": True,
    }


__all__ = [
    "EXPECTED_LIMIT_SURVIVORS",
    "anchor_audit",
    "infinite_exponent_bound",
    "limit_placement_scan",
    "proof_branch",
    "propagated_gap",
    "ray_audit",
    "universal_seed_templates",
]
