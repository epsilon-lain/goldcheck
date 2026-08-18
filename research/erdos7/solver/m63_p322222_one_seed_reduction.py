"""M63: reduce profile (3,2,2,2,2,2) to one explicit hard seed.

At the minimal odd primes only two of the six placements survive the direct
McNew--Setty bound: exponent 3 on prime 3 (canonical), or on prime 5
(swapped).  The swapped absolute-minimal tuple has a positive exact a=2
M25-tensor certificate, and every nonminimal swapped tuple is direct.  For the
canonical placement, the reference tuple (3,5,7,11,13,19) has a positive exact
a=3 M25-tensor certificate, which scales to every nonminimal canonical tuple.
Thus only 3^3*5^2*7^2*11^2*13^2*17^2 remains.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import permutations
from math import comb

from m14_clique_shearer import J_MASK, coordinate_rhos
from m17_infinite_family import is_prime
from m22_universal_direct_zones import universal_monotonicity_gap
from m25_cross_support_seed import CROSS, DIAGONAL, LAMBDA
from m26_minimal_frontier import direct_bound, family_number, sorted_profile

PROFILE = (3,2,2,2,2,2)
MINIMAL_ODD_PRIMES = (3,5,7,11,13,17)
TAIL_PRIMES = (3,5,7,11,13,19)
OFF3_ANCHOR = (5,7,11,13,17,19)
CANONICAL = PROFILE
SWAPPED = (2,3,2,2,2,2)
SURVIVING_PLACEMENTS = (SWAPPED, CANONICAL)
HARD_PRIMES = MINIMAL_ODD_PRIMES
HARD_SEED = family_number(HARD_PRIMES, CANONICAL)

J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
NON5 = tuple(m for m in range(1,32) if not (m & 1))
FIVE = tuple(1 | T for T in J_SUBSETS)

EXPECTED = {
    (MINIMAL_ODD_PRIMES, SWAPPED): (
        Fraction(33868448812182084944300049699884875858603,80969847930582921147185215705838000000000),
        Fraction(10396620060393879335269823900407176231,73275880480165539499715127335600000000),
        Fraction(188107,1002001), Fraction(35059165,289578289),
    ),
    (TAIL_PRIMES, CANONICAL): (
        Fraction(28164743009849495865769491868227672885178687,67499095505848947714418677632346578832000000),
        Fraction(66138381986300034053279312820363673862719,4821363964703496265315619830881898488000000),
        Fraction(47337,1002001), Fraction(4220577,361722361),
    ),
}

EXPECTED_MIN_CANONICAL_R = Fraction(1365332933,1329696225)
EXPECTED_MIN_SWAPPED_R = Fraction(25110764647,25059659625)
EXPECTED_MAX_KILLED_R = Fraction(455234610631,456085805175)
EXPECTED_SWAPPED_TAIL_R = Fraction(406203011801,406937656125)
EXPECTED_OFF3_CANONICAL_R = Fraction(8908790816491,13067220291125)
EXPECTED_OFF3_SWAPPED_R = Fraction(12386164211767,18294108407575)


def _ppx(p: int, a: int) -> Fraction:
    return sum((Fraction(1,p**j) for j in range(1,a+1)), Fraction(0))


def _H(a: int, t: int) -> int:
    selected = (3**a + 1)//2
    out = selected
    for u in range(1,t+1):
        centered = sum((j**u-(j-1)**u)*3**(a-j) for j in range(1,a+1))
        out += comb(t,u)*centered
    return out


def _quadratic_min(linear: Fraction, quadratic: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    x = -linear/(2*quadratic)
    if x < lo: x = lo
    elif x > hi: x = hi
    return linear*x + quadratic*x*x


@lru_cache(maxsize=None)
def reference_certificate(primes: tuple[int,...], exponents: tuple[int,...]) -> dict:
    key = (tuple(primes), tuple(exponents))
    if key not in EXPECTED:
        raise ValueError("not an M63 reference")
    a = exponents[0]
    assert primes[0] == 3 and a in (2,3)
    factor = a+1
    selected = (3**a+1)//2
    h1,h2 = _H(a,1),_H(a,2)
    coords = tuple(_ppx(p,e) for p,e in zip(primes[1:],exponents[1:]))
    b = {}
    for m in range(1,32):
        value = Fraction(1)
        for i,x in enumerate(coords):
            if m & (1<<i): value *= x
        b[m] = value

    best = proper = full = None
    for bits in range(1<<len(NON5)):
        q0 = {m:b[m]*(factor if bits & (1<<i) else 1) for i,m in enumerate(NON5)}
        rho = coordinate_rhos(q0,J_MASK)
        for Cmask,value in rho.items():
            if Cmask == J_MASK:
                full = value if full is None or value < full else full
            else:
                proper = value if proper is None or value < proper else proper
        value = rho[J_MASK]
        value += sum(LAMBDA.get(m,Fraction(0))*q0[m] for m in NON5)
        value += sum(mu*q0[s]*q0[t] for (s,t),mu in CROSS.items())
        for T in J_SUBSETS:
            m = 1|T
            linear = LAMBDA.get(m,Fraction(0)) - rho[J_MASK ^ T]
            value += _quadratic_min(linear,DIAGONAL[m],b[m],factor*b[m])
        best = value if best is None or value < best else best

    assert best is not None and proper is not None and full is not None
    margin = (
        selected*best
        - h1*sum(LAMBDA.get(m,Fraction(0))*b[m] for m in range(1,32))
        - h2*sum(DIAGONAL[m]*b[m]**2 for m in FIVE)
        - h2*sum(mu*b[s]*b[t] for (s,t),mu in CROSS.items())
    )
    eb,em,ep,ef = EXPECTED[key]
    assert best == eb
    assert margin == em > 0
    assert proper == ep > 0
    assert full == ef > 0
    assert factor*coords[0] < 1
    return {"primes":tuple(primes),"exponents":tuple(exponents),"C":best,
            "summed_rho_margin":margin,"proper_non5_min":proper,
            "full_non5_min":full,"verified":True}


def placement_scan() -> dict:
    assignments = tuple(sorted(set(permutations(PROFILE))))
    values = {a:direct_bound(MINIMAL_ODD_PRIMES,a) for a in assignments}
    survivors = tuple(a for a in assignments if values[a] >= 1)
    assert len(assignments) == 6
    assert set(survivors) == set(SURVIVING_PLACEMENTS)
    assert values[CANONICAL] == EXPECTED_MIN_CANONICAL_R > 1
    assert values[SWAPPED] == EXPECTED_MIN_SWAPPED_R > 1
    killed = {a:v for a,v in values.items() if a not in survivors}
    assert max(killed.values()) == EXPECTED_MAX_KILLED_R < 1
    assert direct_bound(TAIL_PRIMES,SWAPPED) == EXPECTED_SWAPPED_TAIL_R < 1
    return {"assignment_count":6,"surviving_placements":survivors,
            "directly_killed_placement_count":4,"verified":True}


def proof_branch(primes: tuple[int,...], exponents: tuple[int,...]) -> str:
    primes = tuple(primes); exponents = tuple(exponents)
    if len(primes) != 6 or tuple(sorted(primes)) != primes or len(set(primes)) != 6:
        raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p%2 for p in primes):
        raise ValueError("need six odd primes")
    if sorted_profile(exponents) != PROFILE:
        raise ValueError("wrong exponent profile")
    assert universal_monotonicity_gap() > 0

    if exponents not in SURVIVING_PLACEMENTS:
        base = direct_bound(MINIMAL_ODD_PRIMES,exponents)
        assert base < 1 and direct_bound(primes,exponents) <= base
        return "McNew-Setty-placement"

    if primes[0] != 3:
        anchor = direct_bound(OFF3_ANCHOR,exponents)
        expected = EXPECTED_OFF3_SWAPPED_R if exponents == SWAPPED else EXPECTED_OFF3_CANONICAL_R
        assert anchor == expected < 1 and direct_bound(primes,exponents) <= anchor
        return "McNew-Setty-off3-anchor"

    if exponents == SWAPPED:
        if primes == MINIMAL_ODD_PRIMES:
            assert reference_certificate(MINIMAL_ODD_PRIMES,SWAPPED)["summed_rho_margin"] > 0
            return "M63-a2-minimal"
        assert all(p >= q for p,q in zip(primes,TAIL_PRIMES))
        assert direct_bound(primes,exponents) <= EXPECTED_SWAPPED_TAIL_R < 1
        return "McNew-Setty-swapped-tail"

    assert exponents == CANONICAL
    if primes == HARD_PRIMES:
        return "M63-hard-seed"
    assert all(p >= q for p,q in zip(primes,TAIL_PRIMES))
    assert reference_certificate(TAIL_PRIMES,CANONICAL)["summed_rho_margin"] > 0
    # M27 coordinatewise scaling transports this positive reference certificate
    # to every larger prime tuple with the same exponent placement.
    return "M63-scaled-canonical-tail"


@lru_cache(maxsize=1)
def reduction_audit() -> dict:
    scan = placement_scan()
    for key in EXPECTED:
        assert reference_certificate(*key)["summed_rho_margin"] > 0
    assert proof_branch(HARD_PRIMES,CANONICAL) == "M63-hard-seed"
    return {"profile":PROFILE,"placement_scan":scan,"reference_certificate_count":2,
            "hard_seed":HARD_SEED,"hard_primes":HARD_PRIMES,
            "hard_exponents":CANONICAL,"all_other_profile_members_noncovering":True,
            "verified":True}


__all__ = [
    "CANONICAL","HARD_SEED","PROFILE","SURVIVING_PLACEMENTS","SWAPPED",
    "placement_scan","proof_branch","reduction_audit","reference_certificate",
]
