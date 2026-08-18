"""M50: close the six-prime exponent ray (A,3,1,1,1,1), A>=6.

Use the McNew--Setty bound with the large exponent sent to infinity.  At the
minimal odd primes only three placements survive:

    A on 3, cube on 5;
    A on 3, cube on 7;
    cube on 3, A on 5.

M48 kills the third placement directly because its special prime-5 exponent is
already allowed to be arbitrary.  For the first two placements, M48 gives
quantitative a=5 precursor margins with the cube coordinate treated below its
infinite special-coordinate baseline.  The deficiency recurrence propagates
those margins from exponent 5 on prime 3 to every A>=6.
"""
from __future__ import annotations

from fractions import Fraction

from m17_infinite_family import elementary_symmetric
from m22_universal_direct_zones import universal_monotonicity_gap
from m48_special_coordinate_limits import (
    A3_EXPECTED_ETA,
    A5_FIVE_EXPECTED_ETA,
    A5_SEVEN_EXPECTED_ETA,
)

MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
EXPECTED_LIMIT_SURVIVORS = {
    (0, 1): Fraction(333, 325),
    (0, 2): Fraction(4190826, 4169165),
    (1, 0): Fraction(54619, 54054),
}
EXPECTED_LIMIT_KILLED_MAX = ((0, 3), Fraction(931068, 935935))

TEMPLATES_05 = (
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
    (3, 5, 7, 11, 13, 59),
    (3, 5, 7, 11, 13, 61),
    (3, 5, 7, 11, 13, 67),
    (3, 5, 7, 11, 17, 19),
    (3, 5, 7, 11, 17, 23),
    (3, 5, 7, 11, 19, 23),
    (3, 5, 7, 13, 17, 19),
)
TEMPLATES_07 = (
    (3, 5, 7, 11, 13, 17),
    (3, 5, 7, 11, 13, 19),
)
TEMPLATES_35 = (
    (3, 5, 7, 11, 13, 17),
    (3, 5, 7, 11, 13, 19),
    (3, 5, 7, 11, 13, 23),
)

KILL_ANCHORS = {
    (0, 1): {
        (3, 5, 7, 11, 13, 71): Fraction(8879886, 8883875),
        (3, 5, 7, 11, 17, 29): Fraction(189789, 189805),
        (3, 5, 7, 13, 17, 23): Fraction(340839, 342125),
        (3, 5, 11, 13, 17, 19): Fraction(5575203, 5773625),
    },
    (0, 2): {
        (3, 5, 7, 11, 13, 23): Fraction(244329, 245245),
        (3, 5, 7, 11, 17, 19): Fraction(317673, 320705),
    },
    (1, 0): {
        (3, 5, 7, 11, 13, 29): Fraction(1562189, 1567566),
        (3, 5, 7, 11, 17, 19): Fraction(668884, 671517),
    },
}

REFERENCE_SIGMA_5_CUBE = Fraction(41472, 23375)
REFERENCE_SIGMA_7_CUBE = Fraction(207360, 119119)
EXPECTED_G6_5_CUBE = Fraction(616267788538593, 289578289000000)
EXPECTED_G6_7_CUBE = Fraction(2999179924493339, 868734867000000)


def _direct_from_x(xs: tuple[Fraction, ...]) -> Fraction:
    return (
        elementary_symmetric(xs, 1)
        - elementary_symmetric(xs, 3)
        - elementary_symmetric(xs, 4)
        + 2 * elementary_symmetric(xs, 5)
        + 9 * elementary_symmetric(xs, 6)
    )


def infinite_large_bound(
    primes: tuple[int, ...], large_position: int, cube_position: int
) -> Fraction:
    if len(primes) != 6 or large_position == cube_position:
        raise ValueError("need six primes and distinct large/cube positions")
    xs = []
    for i, p in enumerate(primes):
        if i == large_position:
            xs.append(Fraction(1, p - 1))
        elif i == cube_position:
            xs.append(Fraction(1, p) + Fraction(1, p**2) + Fraction(1, p**3))
        else:
            xs.append(Fraction(1, p))
    return _direct_from_x(tuple(xs))


def limit_placement_scan() -> dict:
    assert universal_monotonicity_gap() > 0
    values = {
        (i, j): infinite_large_bound(MINIMAL_ODD_PRIMES, i, j)
        for i in range(6) for j in range(6) if i != j
    }
    survivors = {k: v for k, v in values.items() if v >= 1}
    assert survivors == EXPECTED_LIMIT_SURVIVORS
    killed = {k: v for k, v in values.items() if v < 1}
    pmax = max(killed, key=killed.get)
    assert (pmax, killed[pmax]) == EXPECTED_LIMIT_KILLED_MAX
    return {
        "placement_count": 30,
        "limit_survivors": survivors,
        "max_killed_placement": pmax,
        "max_killed_R": killed[pmax],
        "verified": True,
    }


def anchor_audit() -> dict:
    for placement, anchors in KILL_ANCHORS.items():
        for anchor, expected in anchors.items():
            assert infinite_large_bound(anchor, *placement) == expected < 1
    return {"anchor_count": sum(len(v) for v in KILL_ANCHORS.values()), "verified": True}


def propagated_gap(A: int, cube_on_7: bool = False) -> Fraction:
    """Uniform normalized deficiency lower bound for the two A-on-3 branches."""
    if A < 6:
        raise ValueError("ray begins at A=6")
    if cube_on_7:
        eta = A5_SEVEN_EXPECTED_ETA
        s = REFERENCE_SIGMA_7_CUBE
        g6 = EXPECTED_G6_7_CUBE
    else:
        eta = A5_FIVE_EXPECTED_ETA
        s = REFERENCE_SIGMA_5_CUBE
        g6 = EXPECTED_G6_5_CUBE
    assert 3 * eta - s == g6 > 0
    assert g6 > s / 2
    k = A - 6
    out = 3**k * g6 - s * Fraction(3**k - 1, 2)
    assert out >= g6 > 0
    return out


def _templates(placement: tuple[int, int]) -> tuple[tuple[int, ...], ...]:
    if placement == (0, 1):
        return TEMPLATES_05
    if placement == (0, 2):
        return TEMPLATES_07
    if placement == (1, 0):
        return TEMPLATES_35
    raise ValueError("not a surviving placement")


def proof_branch(primes: tuple[int, ...], exponents: tuple[int, ...]) -> str:
    if len(primes) != 6 or tuple(sorted(primes)) != primes or len(set(primes)) != 6:
        raise ValueError("need six increasing distinct primes")
    profile = tuple(sorted(exponents, reverse=True))
    A = profile[0]
    if A < 6 or profile[1:] != (3, 1, 1, 1, 1):
        raise ValueError("wrong exponent ray")
    if exponents.count(A) != 1 or exponents.count(3) != 1:
        raise ValueError("ray requires unique large and cube coordinates")
    large_position = exponents.index(A)
    cube_position = exponents.index(3)
    placement = (large_position, cube_position)

    if placement not in EXPECTED_LIMIT_SURVIVORS:
        limit = infinite_large_bound(MINIMAL_ODD_PRIMES, *placement)
        assert limit <= EXPECTED_LIMIT_KILLED_MAX[1] < 1
        return "McNew-Setty-limit-placement"

    if primes in _templates(placement):
        if placement == (1, 0):
            # Stage directly on the cube 3^3; M48 permits arbitrary finite
            # exponent on the special prime 5.
            assert A3_EXPECTED_ETA > 0
            return "M48-a3-five-limit"
        if placement == (0, 1):
            assert propagated_gap(A, cube_on_7=False) > 0
            return "M48-a5-five-limit-recurrence"
        assert placement == (0, 2)
        assert propagated_gap(A, cube_on_7=True) > 0
        return "M48-a5-seven-limit-recurrence"

    dominating = [
        anchor for anchor in KILL_ANCHORS[placement]
        if all(p >= a for p, a in zip(primes, anchor))
    ]
    assert dominating
    anchor = min(dominating)
    assert infinite_large_bound(anchor, *placement) < 1
    return "McNew-Setty-limit-anchor"


def ray_audit() -> dict:
    scan = limit_placement_scan()
    anchors = anchor_audit()
    assert len(TEMPLATES_05) + len(TEMPLATES_07) + len(TEMPLATES_35) == 22
    assert propagated_gap(6) == EXPECTED_G6_5_CUBE
    assert propagated_gap(6, cube_on_7=True) == EXPECTED_G6_7_CUBE
    assert propagated_gap(20) > propagated_gap(6)
    assert propagated_gap(20, cube_on_7=True) > propagated_gap(6, cube_on_7=True)

    for A in (6, 7, 10):
        for placement in EXPECTED_LIMIT_SURVIVORS:
            for primes in _templates(placement):
                exp = [1] * 6
                exp[placement[0]] = A
                exp[placement[1]] = 3
                assert "M48" in proof_branch(primes, tuple(exp))

    return {
        "profile_ray": "(A,3,1,1,1,1), A>=6",
        "limit_scan": scan,
        "anchors": anchors,
        "universal_seed_template_count": 22,
        "all_ray_numbers_noncovering": True,
        "verified": True,
    }


__all__ = [
    "EXPECTED_LIMIT_SURVIVORS",
    "TEMPLATES_05",
    "TEMPLATES_07",
    "TEMPLATES_35",
    "anchor_audit",
    "infinite_large_bound",
    "limit_placement_scan",
    "proof_branch",
    "propagated_gap",
    "ray_audit",
]
