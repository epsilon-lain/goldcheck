"""M60: reduce profile (3,2,2,2,2,1) to one explicit hard seed.

At the minimal odd primes only five of the 30 exponent placements survive the
direct McNew--Setty bound.  Three a=3 noncanonical placements are eliminated
by exact M25-tensor reference certificates and M27 scaling.  The placement with
exponent 3 on prime 5 is already eliminated at the absolute minimal tuple by an
exact a=2 certificate; its prime tail is direct.  The canonical a=3 placement
has a positive M25-tensor reference as soon as the last prime is 19.

Thus the sole unresolved member of the whole profile is

    3^3 * 5^2 * 7^2 * 11^2 * 13^2 * 17.
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

PROFILE = (3, 2, 2, 2, 2, 1)
MINIMAL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)
TAIL_PRIMES = (3, 5, 7, 11, 13, 19)
OFF3_ANCHOR = (5, 7, 11, 13, 17, 19)
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
NON5 = tuple(m for m in range(1, 32) if not (m & 1))
FIVE = tuple(1 | T for T in J_SUBSETS)

SWAPPED = (2, 3, 2, 2, 2, 1)
A = (3, 2, 1, 2, 2, 2)
B = (3, 2, 2, 1, 2, 2)
C = (3, 2, 2, 2, 1, 2)
CANONICAL = (3, 2, 2, 2, 2, 1)
SURVIVING_PLACEMENTS = (SWAPPED, A, B, C, CANONICAL)
HARD_PRIMES = MINIMAL_ODD_PRIMES
HARD_EXPONENTS = CANONICAL
HARD_SEED = family_number(HARD_PRIMES, HARD_EXPONENTS)

EXPECTED = {
    (MINIMAL_ODD_PRIMES, SWAPPED): (
        Fraction(948749018239488041074965937399333,2270410860378991957944517200000000),
        Fraction(350534617678214732127596103208121,2270410860378991957944517200000000),
        Fraction(188107,1002001), Fraction(2125388,17034017)),
    (MINIMAL_ODD_PRIMES, A): (
        Fraction(5364030713898845299092233314118680589423,13021273503938641196731010199224560000000),
        Fraction(204440715883069613374331631525623334383,930090964567045799766500728516040000000),
        Fraction(12547,143143), Fraction(1540675,41368327)),
    (MINIMAL_ODD_PRIMES, B): (
        Fraction(248279117457468787115512303613475125810977,595857780093456663688426474984350320000000),
        Fraction(134637258372126924668647611221276451301,3273943846667344305980365247166760000000),
        Fraction(5295,91091), Fraction(385167,26325299)),
    (MINIMAL_ODD_PRIMES, C): (
        Fraction(534092066115880396701687712093515673320773,1279860202212572597153247398930882640000000),
        Fraction(31621123910895727363040943800431904909,3656743434893064563294992568373950400000),
        Fraction(4177,77077), Fraction(263521,22275253)),
    (TAIL_PRIMES, CANONICAL): (
        Fraction(389660975261985211319725668620927378993459,934890519471592073606906892414772560000000),
        Fraction(2814405251375347289543327217245912476019,66777894247970862400493349458198040000000),
        Fraction(47337,1002001), Fraction(255999,19038019)),
}

EXPECTED_SWAPPED_MIN_R = Fraction(1742300576,1742115375)
EXPECTED_SWAPPED_TAIL_R = Fraction(2371773562,2379752375)
EXPECTED_CANONICAL_MIN_R = Fraction(1683513532,1642565925)
EXPECTED_CANONICAL_TAIL_R = Fraction(34098646,33378345)


def _ppx(p: int, a: int) -> Fraction:
    return sum((Fraction(1, p**j) for j in range(1, a + 1)), Fraction(0))


def _H(a: int, t: int) -> int:
    selected = (3**a + 1) // 2
    out = selected
    for u in range(1, t + 1):
        centered = sum((j**u - (j - 1)**u) * 3**(a - j) for j in range(1, a + 1))
        out += comb(t, u) * centered
    return out


def _quadratic_min(linear: Fraction, quadratic: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
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
        raise ValueError("not an M60 reference")
    a = exponents[0]
    assert primes[0] == 3 and a in (2, 3)
    factor = a + 1
    selected = (3**a + 1) // 2
    h1, h2 = _H(a, 1), _H(a, 2)

    coords = tuple(_ppx(p, e) for p, e in zip(primes[1:], exponents[1:]))
    b = {}
    for m in range(1, 32):
        value = Fraction(1)
        for i, x in enumerate(coords):
            if m & (1 << i):
                value *= x
        b[m] = value

    best = proper = full = None
    for bits in range(1 << len(NON5)):
        q0 = {m: b[m] * (factor if bits & (1 << i) else 1) for i, m in enumerate(NON5)}
        rho = coordinate_rhos(q0, J_MASK)
        for Cmask, value in rho.items():
            if Cmask == J_MASK:
                full = value if full is None or value < full else full
            else:
                proper = value if proper is None or value < proper else proper

        value = rho[J_MASK]
        value += sum(LAMBDA.get(m, Fraction(0)) * q0[m] for m in NON5)
        value += sum(mu * q0[s] * q0[t] for (s, t), mu in CROSS.items())
        for T in J_SUBSETS:
            m = 1 | T
            linear = LAMBDA.get(m, Fraction(0)) - rho[J_MASK ^ T]
            value += _quadratic_min(linear, DIAGONAL[m], b[m], factor * b[m])
        best = value if best is None or value < best else best

    assert best is not None and proper is not None and full is not None
    margin = (
        selected * best
        - h1 * sum(LAMBDA.get(m, Fraction(0)) * b[m] for m in range(1, 32))
        - h2 * sum(DIAGONAL[m] * b[m] ** 2 for m in FIVE)
        - h2 * sum(mu * b[s] * b[t] for (s, t), mu in CROSS.items())
    )
    eb, em, ep, ef = EXPECTED[key]
    assert best == eb
    assert margin == em > 0
    assert proper == ep > 0
    assert full == ef > 0
    assert factor * coords[0] < 1
    return {
        "primes": tuple(primes), "exponents": tuple(exponents),
        "C": best, "summed_rho_margin": margin,
        "proper_non5_min": proper, "full_non5_min": full,
        "verified": True,
    }


def placement_scan() -> dict:
    assignments = tuple(sorted(set(permutations(PROFILE))))
    values = {a: direct_bound(MINIMAL_ODD_PRIMES, a) for a in assignments}
    survivors = tuple(a for a in assignments if values[a] >= 1)
    assert len(assignments) == 30
    assert set(survivors) == set(SURVIVING_PLACEMENTS)
    assert len(survivors) == 5
    assert max(v for a, v in values.items() if a not in survivors) < 1
    assert values[SWAPPED] == EXPECTED_SWAPPED_MIN_R > 1
    assert values[CANONICAL] == EXPECTED_CANONICAL_MIN_R > 1
    assert direct_bound(TAIL_PRIMES, SWAPPED) == EXPECTED_SWAPPED_TAIL_R < 1
    assert direct_bound(TAIL_PRIMES, CANONICAL) == EXPECTED_CANONICAL_TAIL_R > 1
    return {"assignment_count": 30, "surviving_placements": survivors,
            "directly_killed_placement_count": 25, "verified": True}


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

    if exponents == SWAPPED:
        if primes == MINIMAL_ODD_PRIMES:
            assert reference_certificate(MINIMAL_ODD_PRIMES, SWAPPED)["summed_rho_margin"] > 0
            return "M60-a2-minimal"
        assert all(p >= q for p, q in zip(primes, TAIL_PRIMES))
        assert direct_bound(primes, exponents) <= EXPECTED_SWAPPED_TAIL_R < 1
        return "McNew-Setty-swapped-tail"

    if exponents in (A, B, C):
        assert reference_certificate(MINIMAL_ODD_PRIMES, exponents)["summed_rho_margin"] > 0
        return "M60-scaled-a3-noncanonical"

    assert exponents == CANONICAL
    if primes == HARD_PRIMES:
        return "M60-hard-seed"
    assert all(p >= q for p, q in zip(primes, TAIL_PRIMES))
    assert reference_certificate(TAIL_PRIMES, CANONICAL)["summed_rho_margin"] > 0
    return "M60-scaled-canonical-tail"


@lru_cache(maxsize=1)
def reduction_audit() -> dict:
    scan = placement_scan()
    for key in EXPECTED:
        assert reference_certificate(*key)["summed_rho_margin"] > 0
    assert proof_branch(HARD_PRIMES, HARD_EXPONENTS) == "M60-hard-seed"
    return {
        "profile": PROFILE,
        "placement_scan": scan,
        "reference_certificate_count": len(EXPECTED),
        "hard_seed": HARD_SEED,
        "hard_primes": HARD_PRIMES,
        "hard_exponents": HARD_EXPONENTS,
        "all_other_profile_members_noncovering": True,
        "verified": True,
    }


__all__ = [
    "CANONICAL", "HARD_SEED", "PROFILE", "SURVIVING_PLACEMENTS",
    "placement_scan", "proof_branch", "reduction_audit", "reference_certificate",
]
