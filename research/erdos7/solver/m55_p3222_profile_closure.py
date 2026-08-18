"""M55: exclude the complete six-prime profile (3,2,2,2,1,1).

At the minimal odd primes only six exponent placements survive the direct
McNew--Setty bound.  All six have exponent 3 on prime 3 and exponent 2 on prime
5.  For each placement, reuse the nonnegative M25 linear/diagonal/cross tensor
at an a=3 reference baseline and verify an exact positive 2^15 endpoint
certificate.

M27's supportwise scaling then transports each reference certificate to every
coordinatewise larger prime tuple with smallest prime 3.  If the smallest prime
is >3, the direct bound at the anchor (5,7,11,13,17,19) is already <1.
Thus every odd six-prime number with sorted exponent profile
(3,2,2,2,1,1) is noncovering.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import permutations

from m17_infinite_family import is_prime
from m25_cross_support_seed import CROSS, DIAGONAL, LAMBDA
from m26_minimal_frontier import direct_bound, sorted_profile
from m28_moment_hierarchy import moment_constant
from m22_universal_direct_zones import universal_monotonicity_gap

PROFILE = (3, 2, 2, 2, 1, 1)
MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
OFF3_ANCHOR = (5, 7, 11, 13, 17, 19)
J_MASK = 0b11110
NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
FIVE_MASKS = tuple(1 | T for T in J_SUBSETS)

SURVIVING_PLACEMENTS = (
    (3,2,1,1,2,2),
    (3,2,1,2,1,2),
    (3,2,1,2,2,1),
    (3,2,2,1,1,2),
    (3,2,2,1,2,1),
    (3,2,2,2,1,1),
)

# (summed-rho margin, proper non-special rho minimum, full non-special rho minimum)
EXPECTED = {
    (3,2,1,1,2,2): (
        Fraction(274357669865656156179494630502085875969,868597347075009713831525473738120000000),
        Fraction(1305,13013), Fraction(173529,3760757)),
    (3,2,1,2,1,2): (
        Fraction(40964503188928449313903975731680900153,143514263535834558999018546639480000000),
        Fraction(1055,11011), Fraction(136415,3182179)),
    (3,2,1,2,2,1): (
        Fraction(279127301130495143367722132872534950221,1091006356360652339518490473934040000000),
        Fraction(12547,143143), Fraction(97443,2433431)),
    (3,2,2,1,1,2): (
        Fraction(1052183003300313486705733160451053399327,9821831540002032917941095741500280000000),
        Fraction(459,7007), Fraction(333,17017)),
    (3,2,2,1,2,1): (
        Fraction(3102330322158877427541224983036419481,40164771947161506113002278905160000000),
        Fraction(5295,91091), Fraction(26399,1548547)),
    (3,2,2,2,1,1): (
        Fraction(261660093197770847845124451200472947,5751405213735552946358906210088000000),
        Fraction(4177,77077), Fraction(2655,187187)),
}


def _prime_power_x(p: int, a: int) -> Fraction:
    return sum((Fraction(1, p**j) for j in range(1, a + 1)), Fraction(0))


def _coords(primes: tuple[int, ...], exponents: tuple[int, ...]) -> tuple[Fraction, ...]:
    return tuple(_prime_power_x(p, a) for p, a in zip(primes[1:], exponents[1:]))


def _baseline(coords: tuple[Fraction, ...], mask: int) -> Fraction:
    out = Fraction(1)
    for i, x in enumerate(coords):
        if mask & (1 << i):
            out *= x
    return out


def _coordinate_rhos(q: dict[int, Fraction]) -> dict[int, Fraction]:
    rho = {0: Fraction(1)}
    for size in range(1, 5):
        for Cmask in range(32):
            if Cmask & ~J_MASK or Cmask.bit_count() != size:
                continue
            pivot = Cmask & -Cmask
            rest = Cmask ^ pivot
            value = rho[rest]
            T = rest
            while True:
                S = pivot | T
                value -= q.get(S, Fraction(0)) * rho[Cmask ^ S]
                if T == 0:
                    break
                T = (T - 1) & rest
            rho[Cmask] = value
    return rho


def _quadratic_min(linear: Fraction, quadratic: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    assert quadratic > 0
    x = -linear / (2 * quadratic)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return linear * x + quadratic * x * x


@lru_cache(maxsize=None)
def reference_certificate(exponents: tuple[int, ...]) -> dict:
    exponents = tuple(exponents)
    if exponents not in SURVIVING_PLACEMENTS:
        raise ValueError("not an M55 surviving placement")
    assert exponents[0] == 3 and exponents[1] == 2
    assert moment_constant(3, 1) == 27
    assert moment_constant(3, 2) == 63

    coords = _coords(MINIMAL_ODD_PRIMES, exponents)
    b = {m: _baseline(coords, m) for m in range(1, 32)}
    best = None
    proper_min = None
    full_min = None

    for bits in range(1 << len(NON5_MASKS)):
        q0 = {
            m: b[m] * (4 if bits & (1 << i) else 1)
            for i, m in enumerate(NON5_MASKS)
        }
        rho = _coordinate_rhos(q0)
        for Cmask, value in rho.items():
            if Cmask == J_MASK:
                full_min = value if full_min is None or value < full_min else full_min
            else:
                proper_min = value if proper_min is None or value < proper_min else proper_min

        value = rho[J_MASK]
        value += sum(LAMBDA.get(m, Fraction(0)) * q0[m] for m in NON5_MASKS)
        value += sum(mu * q0[s] * q0[t] for (s, t), mu in CROSS.items())
        for T in J_SUBSETS:
            m = 1 | T
            linear = LAMBDA.get(m, Fraction(0)) - rho[J_MASK ^ T]
            value += _quadratic_min(linear, DIAGONAL[m], b[m], 4 * b[m])
        best = value if best is None or value < best else best

    assert best is not None and proper_min is not None and full_min is not None
    linear_cost = 27 * sum(LAMBDA.get(m, Fraction(0)) * b[m] for m in range(1, 32))
    diagonal_cost = 63 * sum(DIAGONAL[m] * b[m] ** 2 for m in FIVE_MASKS)
    cross_cost = 63 * sum(mu * b[s] * b[t] for (s, t), mu in CROSS.items())
    margin = 14 * best - linear_cost - diagonal_cost - cross_cost

    em, ep, ef = EXPECTED[exponents]
    assert margin == em > 0
    assert proper_min == ep > 0
    assert full_min == ef > 0
    # Reference special coordinate is always 5^2, so even its factor-4 upper
    # endpoint remains below one.
    assert 4 * coords[0] == Fraction(24, 25) < 1
    return {
        "exponents": exponents,
        "reference_coords": coords,
        "C": best,
        "summed_rho_margin": margin,
        "proper_non5_min": proper_min,
        "full_non5_min": full_min,
        "verified": True,
    }


def placement_scan() -> dict:
    assert universal_monotonicity_gap() > 0
    assignments = tuple(sorted(set(permutations(PROFILE))))
    values = {a: direct_bound(MINIMAL_ODD_PRIMES, a) for a in assignments}
    survivors = tuple(a for a in assignments if values[a] >= 1)
    assert set(survivors) == set(SURVIVING_PLACEMENTS)
    assert len(assignments) == 60 and len(survivors) == 6
    assert max(v for a, v in values.items() if a not in survivors) < 1
    for a in survivors:
        assert direct_bound(OFF3_ANCHOR, a) < 1
    return {
        "assignment_count": len(assignments),
        "surviving_placements": survivors,
        "directly_killed_placement_count": len(assignments) - len(survivors),
        "verified": True,
    }


def scaling_factors(primes: tuple[int, ...], exponents: tuple[int, ...]) -> dict[int, Fraction]:
    ref = _coords(MINIMAL_ODD_PRIMES, exponents)
    actual = _coords(primes, exponents)
    assert all(x <= y for x, y in zip(actual, ref))
    out = {}
    for m in range(1, 32):
        b = _baseline(actual, m)
        bbar = _baseline(ref, m)
        out[m] = bbar / b
        assert out[m] >= 1
    return out


def proof_branch(primes: tuple[int, ...], exponents: tuple[int, ...]) -> str:
    primes = tuple(primes)
    exponents = tuple(exponents)
    if len(primes) != 6 or tuple(sorted(primes)) != primes or len(set(primes)) != 6:
        raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p % 2 for p in primes):
        raise ValueError("need odd primes")
    if sorted_profile(exponents) != PROFILE:
        raise ValueError("wrong exponent profile")
    assert universal_monotonicity_gap() > 0

    if exponents not in SURVIVING_PLACEMENTS:
        base = direct_bound(MINIMAL_ODD_PRIMES, exponents)
        assert base < 1 and direct_bound(primes, exponents) <= base
        return "McNew-Setty-placement"

    if primes[0] != 3:
        assert all(p >= a for p, a in zip(primes, OFF3_ANCHOR))
        anchor = direct_bound(OFF3_ANCHOR, exponents)
        assert anchor < 1 and direct_bound(primes, exponents) <= anchor
        return "McNew-Setty-off3-anchor"

    cert = reference_certificate(exponents)
    factors = scaling_factors(primes, exponents)
    # M27 scaling: qbar_S=gamma_S q_S lies in the reference factor-4 box;
    # the 27 first-moment and 63 pair-moment budgets transport exactly.
    ref = cert["reference_coords"]
    actual = _coords(primes, exponents)
    for s in (1, 2, 3, 7, 15, 31):
        assert factors[s] * _baseline(actual, s) == _baseline(ref, s)
    for s, t in ((1,2), (3,12), (14,17), (30,31)):
        assert (
            factors[s] * factors[t]
            * _baseline(actual, s) * _baseline(actual, t)
            == _baseline(ref, s) * _baseline(ref, t)
        )
    assert cert["summed_rho_margin"] > 0
    return "M55-scaled-a3-certificate"


@lru_cache(maxsize=1)
def theorem_audit() -> dict:
    scan = placement_scan()
    certs = {a: reference_certificate(a) for a in SURVIVING_PLACEMENTS}
    assert all(c["summed_rho_margin"] > 0 for c in certs.values())
    worst = min(certs.values(), key=lambda c: c["summed_rho_margin"])
    assert worst["exponents"] == (3,2,2,2,1,1)
    # Exercise the three universal branches.
    assert proof_branch(MINIMAL_ODD_PRIMES, (3,2,2,2,1,1)) == "M55-scaled-a3-certificate"
    assert proof_branch(OFF3_ANCHOR, (3,2,2,2,1,1)) == "McNew-Setty-off3-anchor"
    assert proof_branch(MINIMAL_ODD_PRIMES, (3,1,2,2,2,1)) == "McNew-Setty-placement"
    return {
        "profile": PROFILE,
        "placement_scan": scan,
        "reference_certificate_count": len(certs),
        "minimum_reference_margin": worst["summed_rho_margin"],
        "all_odd_six_prime_numbers_with_profile_noncovering": True,
        "verified": True,
    }


__all__ = [
    "EXPECTED", "PROFILE", "SURVIVING_PLACEMENTS", "placement_scan",
    "proof_branch", "reference_certificate", "scaling_factors", "theorem_audit",
]
