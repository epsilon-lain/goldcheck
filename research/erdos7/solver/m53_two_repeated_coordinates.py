"""M53: every six-prime profile with exactly two repeated coordinates is noncovering.

Consider an odd six-prime number whose exponent vector has exactly four ones
and two entries at least two.  Send both repeated-coordinate McNew--Setty
charges to their geometric-series limits.  At the minimal odd primes only the
repeated-prime pairs (3,5) and (3,7) survive.  Exact monotone kill anchors then
reduce the two infinite prime families to 22 and 2 universal prime templates.

For each template, let u be the exponent on prime 3 and v the exponent on the
other repeated prime (5 or 7).  Earlier profile/ray closures handle u<=3;
M52 handles u=4 with the special coordinate already at infinite exponent;
M48 handles u=5; and the quantitative M48 margins propagate to every u>=6 by
the deficiency recurrence, uniformly in the arbitrary finite exponent v.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations

from m17_infinite_family import elementary_symmetric
from m22_universal_direct_zones import universal_monotonicity_gap
from m48_special_coordinate_limits import (
    A5_FIVE_EXPECTED_ETA,
    A5_SEVEN_EXPECTED_ETA,
)
from m51_frontier_after_A3_ray import profile_closed_after_m50
from m52_a4_special_coordinate_limits import (
    A4_FIVE_EXPECTED_ETA,
    A4_SEVEN_EXPECTED_ETA,
)

MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
SURVIVING_PAIRS = ((0, 1), (0, 2))
EXPECTED_PAIR_LIMITS = {
    (0, 1): Fraction(747, 728),
    (0, 2): Fraction(48889, 48620),
}
EXPECTED_MAX_KILLED_PAIR = ((0, 3), Fraction(153903, 154700))

TEMPLATES_35 = (
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
    (3, 5, 7, 11, 13, 71),
    (3, 5, 7, 11, 13, 73),
    (3, 5, 7, 11, 13, 79),
    (3, 5, 7, 11, 17, 19),
    (3, 5, 7, 11, 17, 23),
    (3, 5, 7, 11, 17, 29),
    (3, 5, 7, 11, 17, 31),
    (3, 5, 7, 11, 19, 23),
    (3, 5, 7, 13, 17, 19),
)
TEMPLATES_37 = (
    (3, 5, 7, 11, 13, 17),
    (3, 5, 7, 11, 13, 19),
)

KILL_ANCHORS = {
    (0, 1): {
        (5, 7, 11, 13, 17, 19): Fraction(39055, 58344),
        (3, 7, 11, 13, 17, 19): Fraction(166125, 184756),
        (3, 5, 11, 13, 17, 19): Fraction(357417, 369512),
        (3, 5, 7, 11, 13, 83): Fraction(60423, 60424),
        (3, 5, 7, 11, 17, 37): Fraction(386361, 387464),
        (3, 5, 7, 11, 19, 29): Fraction(17823, 17864),
        (3, 5, 7, 13, 17, 23): Fraction(40575, 40664),
    },
    (0, 2): {
        (5, 7, 11, 13, 17, 19): Fraction(110183, 167960),
        (3, 7, 11, 13, 17, 19): Fraction(521291, 587860),
        (3, 5, 11, 13, 17, 19): Fraction(391791, 419900),
        (3, 5, 7, 11, 13, 23): Fraction(65557, 65780),
        (3, 5, 7, 11, 17, 19): Fraction(70413, 71060),
    },
}

SIGMA_LIMIT_5 = Fraction(4320, 2431)
SIGMA_LIMIT_7 = Fraction(21168, 12155)
EXPECTED_G6_5 = Fraction(615444438010593, 289578289000000)
EXPECTED_G6_7 = Fraction(61194894067211, 17729283000000)


def _direct_from_x(xs: tuple[Fraction, ...]) -> Fraction:
    return (
        elementary_symmetric(xs, 1)
        - elementary_symmetric(xs, 3)
        - elementary_symmetric(xs, 4)
        + 2 * elementary_symmetric(xs, 5)
        + 9 * elementary_symmetric(xs, 6)
    )


def double_infinite_bound(primes: tuple[int, ...], pair: tuple[int, int]) -> Fraction:
    """McNew--Setty R after sending exactly two coordinates to infinite exponent."""
    if len(primes) != 6 or len(pair) != 2 or pair[0] >= pair[1]:
        raise ValueError("need six primes and an increasing coordinate pair")
    xs = tuple(
        Fraction(1, p - 1) if i in pair else Fraction(1, p)
        for i, p in enumerate(primes)
    )
    return _direct_from_x(xs)


def pair_limit_scan() -> dict:
    assert universal_monotonicity_gap() > 0
    values = {
        pair: double_infinite_bound(MINIMAL_ODD_PRIMES, pair)
        for pair in combinations(range(6), 2)
    }
    survivors = {pair: value for pair, value in values.items() if value >= 1}
    assert survivors == EXPECTED_PAIR_LIMITS
    killed = {pair: value for pair, value in values.items() if value < 1}
    pmax = max(killed, key=killed.get)
    vmax = killed[pmax]
    assert (pmax, vmax) == EXPECTED_MAX_KILLED_PAIR
    return {
        "pair_count": len(values),
        "surviving_pairs": survivors,
        "max_killed_pair": pmax,
        "max_killed_R": vmax,
        "verified": True,
    }


def anchor_audit() -> dict:
    for pair, anchors in KILL_ANCHORS.items():
        for anchor, expected in anchors.items():
            assert double_infinite_bound(anchor, pair) == expected < 1
    return {
        "pair_35_anchor_count": len(KILL_ANCHORS[(0, 1)]),
        "pair_37_anchor_count": len(KILL_ANCHORS[(0, 2)]),
        "verified": True,
    }


def _templates(pair: tuple[int, int]) -> tuple[tuple[int, ...], ...]:
    if pair == (0, 1):
        return TEMPLATES_35
    if pair == (0, 2):
        return TEMPLATES_37
    raise ValueError("pair is not a direct survivor")


def propagated_gap(u: int, special_prime: int) -> Fraction:
    """Uniform normalized deficiency lower bound for exponent u>=6 on prime 3.

    The post-stage special-prime exponent is arbitrary but finite.  We charge
    sigma(M)/M by its geometric-series divisor-sum limit, so the recurrence is
    uniform in that exponent as well as in all coordinatewise larger simple
    primes.
    """
    if u < 6 or special_prime not in (5, 7):
        raise ValueError("need u>=6 and special prime 5 or 7")
    if special_prime == 5:
        eta = A5_FIVE_EXPECTED_ETA
        s = SIGMA_LIMIT_5
        g6 = EXPECTED_G6_5
    else:
        eta = A5_SEVEN_EXPECTED_ETA
        s = SIGMA_LIMIT_7
        g6 = EXPECTED_G6_7
    assert 3 * eta - s == g6 > 0
    assert g6 > s / 2
    k = u - 6
    out = 3**k * g6 - s * Fraction(3**k - 1, 2)
    assert out >= g6 > 0
    return out


def _validate_exactly_two_repeated(exponents: tuple[int, ...]) -> tuple[int, int]:
    if len(exponents) != 6 or any(a < 1 for a in exponents):
        raise ValueError("need six positive exponents")
    repeated = tuple(i for i, a in enumerate(exponents) if a >= 2)
    if len(repeated) != 2 or sum(a == 1 for a in exponents) != 4:
        raise ValueError("need exactly two repeated prime coordinates")
    return repeated


def proof_branch(primes: tuple[int, ...], exponents: tuple[int, ...]) -> str:
    """Classify any exactly-two-repeated six-prime number into a proof branch."""
    if len(primes) != 6 or tuple(sorted(primes)) != primes or len(set(primes)) != 6:
        raise ValueError("need six increasing distinct primes")
    pair = _validate_exactly_two_repeated(exponents)
    assert universal_monotonicity_gap() > 0

    if pair not in SURVIVING_PAIRS:
        limit = double_infinite_bound(MINIMAL_ODD_PRIMES, pair)
        assert limit <= EXPECTED_MAX_KILLED_PAIR[1] < 1
        return "McNew-Setty-double-limit-placement"

    if primes not in _templates(pair):
        dominating = [
            anchor for anchor in KILL_ANCHORS[pair]
            if all(p >= a for p, a in zip(primes, anchor))
        ]
        assert dominating
        anchor = min(dominating)
        assert double_infinite_bound(anchor, pair) < 1
        return "McNew-Setty-double-limit-anchor"

    u = exponents[0]
    special_prime = 5 if pair == (0, 1) else 7

    if u <= 3:
        # The complete A2/A3 rays and the earlier downsets already cover these
        # sorted profiles, regardless of the other repeated exponent.
        assert profile_closed_after_m50(exponents)
        return "prior-A2-A3-ray-closure"
    if u == 4:
        eta = A4_FIVE_EXPECTED_ETA if special_prime == 5 else A4_SEVEN_EXPECTED_ETA
        assert eta > 0
        return "M52-a4-special-limit"
    if u == 5:
        eta = A5_FIVE_EXPECTED_ETA if special_prime == 5 else A5_SEVEN_EXPECTED_ETA
        assert eta > 0
        return "M48-a5-special-limit"

    assert u >= 6
    assert propagated_gap(u, special_prime) > 0
    return "M48-limit-recurrence"


def theorem_audit() -> dict:
    scan = pair_limit_scan()
    anchors = anchor_audit()
    assert len(TEMPLATES_35) == 22
    assert len(TEMPLATES_37) == 2
    assert propagated_gap(6, 5) == EXPECTED_G6_5
    assert propagated_gap(6, 7) == EXPECTED_G6_7
    assert propagated_gap(20, 5) > propagated_gap(6, 5) > 0
    assert propagated_gap(20, 7) > propagated_gap(6, 7) > 0

    # Exercise every universal template at each structural exponent regime.
    for pair in SURVIVING_PAIRS:
        special = pair[1]
        for primes in _templates(pair):
            for u in (2, 3, 4, 5, 6, 10):
                exp = [1] * 6
                exp[0] = u
                exp[special] = 11  # arbitrary finite repeated exponent
                branch = proof_branch(primes, tuple(exp))
                assert branch

    return {
        "direct_pair_scan": scan,
        "anchors": anchors,
        "pair_35_template_count": len(TEMPLATES_35),
        "pair_37_template_count": len(TEMPLATES_37),
        "universal_template_count": len(TEMPLATES_35) + len(TEMPLATES_37),
        "all_exactly_two_repeated_six_prime_numbers_noncovering": True,
        "verified": True,
    }


__all__ = [
    "EXPECTED_PAIR_LIMITS",
    "KILL_ANCHORS",
    "TEMPLATES_35",
    "TEMPLATES_37",
    "anchor_audit",
    "double_infinite_bound",
    "pair_limit_scan",
    "proof_branch",
    "propagated_gap",
    "theorem_audit",
]
