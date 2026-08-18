"""M40: exact closure of the six-prime exponent profile (3,2,2,1,1,1).

M26 reduces this profile to twelve explicit McNew--Setty survivor seeds.  Every
seed has exponent 3 on prime 3, exponent 2 on prime 5, and exactly one further
squared prime among the four post-stage coordinates.

Stage on 3^3 and select 14 surviving fibres.  Reuse the nonnegative M25
pointwise penalty tensor, but with the actual a=3 baselines.  The universal M28
budgets are

    sum_r q_S(r) <= 27 b_S,
    sum_r q_S(r) q_T(r) <= 63 b_S b_T.

The special coordinate is 5^2, so x_5=6/25 and q_5<=4x_5=24/25<1.  The other
four coordinates include one square and three simple primes.  For every M26
seed all non-special Clique--Shearer coordinate polynomials stay positive on
the entire factor-4 box.  Hence the M39 quantitative completion lemma applies
without a bad-branch case.

For fixed non-special charges, the sixteen 5-containing variables minimize as
independent clipped convex quadratics.  The remaining function is separately
concave in the fifteen non-special variables, so its global minimum is attained
at one of 2^15 endpoints and is checked exactly with Fraction arithmetic.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction

from m25_cross_support_seed import CROSS, DIAGONAL, LAMBDA
from m26_minimal_frontier import P322, SEEDS, family_number
from m28_moment_hierarchy import moment_constant

J_MASK = 0b11110
NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
FIVE_MASKS = tuple(1 | T for T in J_SUBSETS)

# Regression values are (summed-rho margin, minimum proper non-special rho,
# minimum full non-special rho).  The key is exactly one of the twelve M26
# P322 seed pairs (primes, exponents).
EXPECTED = {
    ((3,5,7,11,13,17),(3,2,2,1,1,1)): (
        Fraction(435379245946298325768261464374075213,3089597842089346624077098377320000000),
        Fraction(459,7007), Fraction(155,7007)),
    ((3,5,7,11,13,19),(3,2,2,1,1,1)): (
        Fraction(9458069673716370819985618468557407827,48112913846810962526314343750344000000),
        Fraction(459,7007), Fraction(17,637)),
    ((3,5,7,11,13,23),(3,2,2,1,1,1)): (
        Fraction(59345990347708754143932197,220553939216249158520000000),
        Fraction(459,7007), Fraction(5389,161161)),
    ((3,5,7,11,13,29),(3,2,2,1,1,1)): (
        Fraction(842544214236123271184306497,2454444310332814359560000000),
        Fraction(459,7007), Fraction(8143,203203)),
    ((3,5,7,11,13,31),(3,2,2,1,1,1)): (
        Fraction(1017277524948930300768281113,2804662285647841378760000000),
        Fraction(459,7007), Fraction(697,16709)),
    ((3,5,7,11,17,19),(3,2,2,1,1,1)): (
        Fraction(163639872881967351280553,463658526983722840000000),
        Fraction(807,9163), Fraction(7477,174097)),
    ((3,5,7,11,13,17),(3,2,1,2,1,1)): (
        Fraction(2060845973714338029754745660675653541,6455658913376641062239588603160000000),
        Fraction(1055,11011), Fraction(1225,26741)),
    ((3,5,7,11,13,19),(3,2,1,2,1,1)): (
        Fraction(91610962171963218280361435013514267,244363307930058448513001099480000000),
        Fraction(1055,11011), Fraction(10685,209209)),
    ((3,5,7,11,13,17),(3,2,1,1,2,1)): (
        Fraction(3146110072228565370094252724486610323,9016581457526052392714797305240000000),
        Fraction(1305,13013), Fraction(10873,221221)),
    ((3,5,7,11,13,19),(3,2,1,1,2,1)): (
        Fraction(82586187355919580205193657605717871,204780491108329972555523235432000000),
        Fraction(1305,13013), Fraction(13483,247247)),
    ((3,5,7,11,13,17),(3,2,1,1,1,2)): (
        Fraction(3019811566240650587421443236480063031,8017821665307781973829465911428800000),
        Fraction(109,1001), Fraction(2155,41327)),
    ((3,5,7,11,13,19),(3,2,1,1,1,2)): (
        Fraction(121983892155463133597376823218824285911,279840417272267843265297713649960000000),
        Fraction(109,1001), Fraction(101,1729)),
}


def _prime_power_x(p: int, a: int) -> Fraction:
    return sum((Fraction(1, p**j) for j in range(1, a + 1)), Fraction(0))


def _baseline_table(primes: tuple[int, ...], exponents: tuple[int, ...]) -> dict[int, Fraction]:
    assert primes[:2] == (3, 5) and exponents[:2] == (3, 2)
    coords = (Fraction(6, 25),) + tuple(
        _prime_power_x(p, a) for p, a in zip(primes[2:], exponents[2:])
    )
    out = {}
    for mask in range(1, 32):
        value = Fraction(1)
        for i, x in enumerate(coords):
            if mask & (1 << i):
                value *= x
        out[mask] = value
    return out


def _coordinate_rhos(q: dict[int, Fraction]) -> dict[int, Fraction]:
    """Independent recurrence for the four non-special coordinates."""
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
def seed_certificate(primes: tuple[int, ...], exponents: tuple[int, ...]) -> dict:
    key = (tuple(primes), tuple(exponents))
    if key not in EXPECTED:
        raise ValueError("not an M26 P322 seed")
    assert tuple(sorted(exponents, reverse=True)) == P322
    assert moment_constant(3, 1) == 27
    assert moment_constant(3, 2) == 63

    b = _baseline_table(tuple(primes), tuple(exponents))
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

    expected_margin, expected_proper, expected_full = EXPECTED[key]
    assert margin == expected_margin > 0
    assert proper_min == expected_proper > 0
    assert full_min == expected_full > 0

    # Since q_{5} <= 4*(6/25)=24/25<1 and the entire non-special vector is
    # inside the Shearer region, M39 turns positive full rho into actual
    # uncovered mass at least rho.  The positive summed margin therefore gives
    # positive deficiency for this seed.
    return {
        "primes": tuple(primes),
        "exponents": tuple(exponents),
        "N": family_number(tuple(primes), tuple(exponents)),
        "C": best,
        "summed_rho_margin": margin,
        "proper_non5_min": proper_min,
        "full_non5_min": full_min,
        "noncovering_certified": True,
    }


@lru_cache(maxsize=1)
def profile_audit() -> dict:
    seeds = tuple(SEEDS[P322])
    assert len(seeds) == 12
    assert set(seeds) == set(EXPECTED)
    certificates = tuple(seed_certificate(pr, ex) for pr, ex in seeds)
    assert all(c["noncovering_certified"] for c in certificates)
    worst = min(certificates, key=lambda c: c["summed_rho_margin"])
    assert worst["primes"] == (3, 5, 7, 11, 13, 17)
    assert worst["exponents"] == P322
    return {
        "profile": P322,
        "seed_count": len(seeds),
        "certified_seed_numbers": tuple(c["N"] for c in certificates),
        "minimum_margin": worst["summed_rho_margin"],
        "all_m26_seeds_excluded": True,
        "all_odd_six_prime_numbers_with_profile_noncovering": True,
    }


__all__ = ["EXPECTED", "profile_audit", "seed_certificate"]
