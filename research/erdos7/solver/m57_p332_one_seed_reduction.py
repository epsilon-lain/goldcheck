"""M57: reduce profile (3,3,2,1,1,1) to one explicit hard seed.

At the minimal odd primes only eight exponent placements survive the direct
McNew--Setty bound.  Seven are excluded on their entire prime families by exact
a=3 M25-tensor reference certificates plus M27 scaling.  The canonical
placement (3,3,2,1,1,1) has a positive scaled reference as soon as the prime
tuple is coordinatewise at least (3,5,7,11,13,19).  Thus the only member of the
whole profile not excluded here is

    3^3 * 5^3 * 7^2 * 11 * 13 * 17.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import permutations

from m17_infinite_family import is_prime
from m22_universal_direct_zones import universal_monotonicity_gap
from m25_cross_support_seed import CROSS, DIAGONAL, LAMBDA
from m26_minimal_frontier import direct_bound, family_number, sorted_profile
from m28_moment_hierarchy import moment_constant

PROFILE = (3, 3, 2, 1, 1, 1)
MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
OFF3_ANCHOR = (5, 7, 11, 13, 17, 19)
CANONICAL_REFERENCE_PRIMES = (3, 5, 7, 11, 13, 19)
HARD_PRIMES = MINIMAL_ODD_PRIMES
HARD_EXPONENTS = PROFILE
HARD_SEED = family_number(HARD_PRIMES, HARD_EXPONENTS)
J_MASK = 0b11110
NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
FIVE_MASKS = tuple(1 | T for T in J_SUBSETS)

SURVIVING_PLACEMENTS = (
    (3,2,1,1,1,3),
    (3,2,1,1,3,1),
    (3,2,1,3,1,1),
    (3,2,3,1,1,1),
    (3,3,1,1,1,2),
    (3,3,1,1,2,1),
    (3,3,1,2,1,1),
    (3,3,2,1,1,1),
)
NONCANONICAL = SURVIVING_PLACEMENTS[:-1]

# Exact reference regressions: (margin, proper non-special min, full non-special min).
EXPECTED = {
    (MINIMAL_ODD_PRIMES,(3,2,1,1,1,3)): (
        Fraction(4341983534131193547536085379019372526739,11585752306369744952183578242014616000000),
        Fraction(109,1001), Fraction(255533,4917913)),
    (MINIMAL_ODD_PRIMES,(3,2,1,1,3,1)): (
        Fraction(604999365472416260266326275527987481,1757557400601964076549943188680000000),
        Fraction(16853,169169), Fraction(139989,2875873)),
    (MINIMAL_ODD_PRIMES,(3,2,1,3,1,1)): (
        Fraction(18674638301851256379759235159244830577,60087286809121043733153093921720000000),
        Fraction(11461,121121), Fraction(92549,2059057)),
    (MINIMAL_ODD_PRIMES,(3,2,3,1,1,1)): (
        Fraction(33810273516261122806335087397024553683,333058647377231566075511205075096000000),
        Fraction(2909,49049), Fraction(14493,833833)),
    (MINIMAL_ODD_PRIMES,(3,3,1,1,1,2)): (
        Fraction(1092359497017625575699138356325941776583,5011138540817363733643416194643000000000),
        Fraction(109,1001), Fraction(2155,41327)),
    (MINIMAL_ODD_PRIMES,(3,3,1,1,2,1)): (
        Fraction(42742934185834253987103257780105580059,225414536438151309817869932631000000000),
        Fraction(1305,13013), Fraction(10873,221221)),
    (MINIMAL_ODD_PRIMES,(3,3,1,2,1,1)): (
        Fraction(25711456047027971169742570153788296861,161391472834416026555989715079000000000),
        Fraction(1055,11011), Fraction(1225,26741)),
    (CANONICAL_REFERENCE_PRIMES,PROFILE): (
        Fraction(217161974733034408394686802579413972423,6014114230851370315789292968793000000000),
        Fraction(459,7007), Fraction(17,637)),
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
def reference_certificate(primes: tuple[int, ...], exponents: tuple[int, ...]) -> dict:
    key = (tuple(primes), tuple(exponents))
    if key not in EXPECTED:
        raise ValueError("not an M57 reference")
    assert exponents[0] == 3
    assert moment_constant(3, 1) == 27 and moment_constant(3, 2) == 63
    coords = _coords(tuple(primes), tuple(exponents))
    b = {m: _baseline(coords, m) for m in range(1, 32)}
    best = None
    proper_min = None
    full_min = None

    for bits in range(1 << len(NON5_MASKS)):
        q0 = {m: b[m] * (4 if bits & (1 << i) else 1) for i, m in enumerate(NON5_MASKS)}
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
    margin = (
        14 * best
        - 27 * sum(LAMBDA.get(m, Fraction(0)) * b[m] for m in range(1, 32))
        - 63 * sum(DIAGONAL[m] * b[m] ** 2 for m in FIVE_MASKS)
        - 63 * sum(mu * b[s] * b[t] for (s, t), mu in CROSS.items())
    )
    em, ep, ef = EXPECTED[key]
    assert margin == em > 0 and proper_min == ep > 0 and full_min == ef > 0
    # The special-coordinate factor-4 upper endpoint is below 1 both for 5^2
    # and 5^3, the only possibilities among the references.
    assert 4 * coords[0] < 1
    return {
        "primes": tuple(primes), "exponents": tuple(exponents), "reference_coords": coords,
        "C": best, "summed_rho_margin": margin, "proper_non5_min": proper_min,
        "full_non5_min": full_min, "verified": True,
    }


def placement_scan() -> dict:
    assert universal_monotonicity_gap() > 0
    assignments = tuple(sorted(set(permutations(PROFILE))))
    values = {a: direct_bound(MINIMAL_ODD_PRIMES, a) for a in assignments}
    survivors = tuple(a for a in assignments if values[a] >= 1)
    assert set(survivors) == set(SURVIVING_PLACEMENTS)
    assert len(assignments) == 60 and len(survivors) == 8
    assert max(v for a, v in values.items() if a not in survivors) < 1
    for a in survivors:
        assert direct_bound(OFF3_ANCHOR, a) < 1
    return {"assignment_count": 60, "surviving_placements": survivors,
            "directly_killed_placement_count": 52, "verified": True}


def _scaled_from_reference(actual_primes, exponents, reference_primes) -> bool:
    actual = _coords(tuple(actual_primes), tuple(exponents))
    ref = _coords(tuple(reference_primes), tuple(exponents))
    assert all(x <= y for x, y in zip(actual, ref))
    for m in (1,2,3,7,15,31):
        gamma = _baseline(ref, m) / _baseline(actual, m)
        assert gamma >= 1 and gamma * _baseline(actual, m) == _baseline(ref, m)
    return True


def proof_branch(primes: tuple[int, ...], exponents: tuple[int, ...]) -> str:
    primes = tuple(primes); exponents = tuple(exponents)
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
        anchor = direct_bound(OFF3_ANCHOR, exponents)
        assert anchor < 1 and direct_bound(primes, exponents) <= anchor
        return "McNew-Setty-off3-anchor"

    if exponents != PROFILE:
        cert = reference_certificate(MINIMAL_ODD_PRIMES, exponents)
        assert _scaled_from_reference(primes, exponents, MINIMAL_ODD_PRIMES)
        assert cert["summed_rho_margin"] > 0
        return "M57-scaled-noncanonical"

    if primes == HARD_PRIMES:
        return "M57-hard-seed"

    # Any increasing odd-prime tuple beginning with 3 and distinct from the
    # minimal tuple is coordinatewise >= (3,5,7,11,13,19).
    assert all(p >= r for p, r in zip(primes, CANONICAL_REFERENCE_PRIMES))
    cert = reference_certificate(CANONICAL_REFERENCE_PRIMES, PROFILE)
    assert _scaled_from_reference(primes, PROFILE, CANONICAL_REFERENCE_PRIMES)
    assert cert["summed_rho_margin"] > 0
    return "M57-scaled-canonical-tail"


@lru_cache(maxsize=1)
def reduction_audit() -> dict:
    scan = placement_scan()
    for exponents in NONCANONICAL:
        assert reference_certificate(MINIMAL_ODD_PRIMES, exponents)["summed_rho_margin"] > 0
    tail = reference_certificate(CANONICAL_REFERENCE_PRIMES, PROFILE)
    assert tail["summed_rho_margin"] > 0
    assert proof_branch(HARD_PRIMES, PROFILE) == "M57-hard-seed"
    assert proof_branch(CANONICAL_REFERENCE_PRIMES, PROFILE) == "M57-scaled-canonical-tail"
    return {
        "profile": PROFILE,
        "placement_scan": scan,
        "noncanonical_reference_count": len(NONCANONICAL),
        "canonical_tail_reference": CANONICAL_REFERENCE_PRIMES,
        "hard_seed": HARD_SEED,
        "hard_primes": HARD_PRIMES,
        "hard_exponents": HARD_EXPONENTS,
        "all_other_profile_members_noncovering": True,
        "verified": True,
    }


__all__ = [
    "CANONICAL_REFERENCE_PRIMES", "HARD_SEED", "NONCANONICAL", "PROFILE",
    "SURVIVING_PLACEMENTS", "placement_scan", "proof_branch", "reduction_audit",
    "reference_certificate",
]
