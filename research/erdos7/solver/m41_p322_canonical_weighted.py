"""M41: weighted two-level activation excludes all six canonical P322 seeds.

The remaining M26 seeds of profile P322=(3,2,2,1,1,1) have canonical form

    3^3 * 5^2 * 7^2 * p * q * r,

with the six explicit prime tuples listed by M26.  Stage on 3^3, distinguish
5^2, and retain the two exact divisors carrying the repeated coordinate 7:
7*m and 49*m.

For a support S containing 7, write A_S and B_S for their 3-adic activation
counts.  Since

    b_S = 1/(7m) + 1/(49m) = 8/(49m),

its normalized grouped charge is not an arbitrary box variable but

    q_S/b_S = 1 + (7*A_S + B_S)/8,

with A_S,B_S in {0,1,2,3}.  M41 exploits this weighted discrete structure for
the singleton support {7}; all other unpenalized coordinates are reduced to
endpoints by separate concavity.

At the reference simple tuple (11,13,17), the exact certificate has a positive
summed-rho margin.  Every other canonical M26 seed has coordinatewise smaller
simple-prime baselines, so inflation to the reference baselines preserves the
same certificate and excludes all six seeds.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m26_minimal_frontier import P322, SEEDS, family_number
from m30_centered_moments import factorial_spike_cap

REFERENCE_SIMPLE = (11, 13, 17)
D = (49, 11, 13, 17)
SELECTED_SIMPLE = (2, 4, 8, 6, 10)
UNSELECTED = tuple(m for m in range(2, 16) if m not in SELECTED_SIMPLE)
COEFFICIENT_DEN = 1_000_000
REP_ALPHA_NUM = (37094, 5952)
REP_BETA_NUM = (17949, 602)
SIMPLE_COEFFICIENT_NUM = (
    (15816, 3723),
    (13298, 2026),
    (9089, 1187),
    (1866, 491),
    (1330, 382),
)
REP_ALPHA = tuple(Fraction(x, COEFFICIENT_DEN) for x in REP_ALPHA_NUM)
REP_BETA = tuple(Fraction(x, COEFFICIENT_DEN) for x in REP_BETA_NUM)
SIMPLE_COEFFICIENTS = tuple(
    (Fraction(a, COEFFICIENT_DEN), Fraction(b, COEFFICIENT_DEN))
    for a, b in SIMPLE_COEFFICIENT_NUM
)

Q = 10**12
C = Fraction(15473, 50000)  # 0.30946
EXPECTED_STATE_COUNT = 16 * 4**5 * 2**9
EXPECTED_FLOOR_MIN = 309_465_375_243
EXPECTED_FLOOR_SLACK = 5_375_243
EXPECTED_A_B = (1, 1)
EXPECTED_Z = (2, 2, 4, 2, 4, 2, 4, 4, 4, 3, 4, 4, 4, 4, 4)
EXPECTED_EXACT_ARGMIN = Fraction(
    41353979144540955436,
    133630391156527890625,
)
EXPECTED_SPECIAL_COST = Fraction(487174848269706, 158363126796875)
EXPECTED_FACTORIAL_COST = Fraction(245917, 200000)
EXPECTED_ETA = Fraction(268990177767141, 10135240115000000)
EXPECTED_COORDINATE_MIN = Fraction(155, 7007)


def _denominators() -> tuple[int, ...]:
    return tuple(prod(D[i] for i in range(4) if Cmask & (1 << i)) for Cmask in range(16))


def _support_weight(mask: int, z: Fraction) -> int:
    """Return c_S*z_S, where c_S=8 exactly when support contains 7."""
    c = 8 if mask & 1 else 1
    value = c * z
    if value.denominator != 1:
        raise ValueError("weighted support did not have integral numerator")
    return value.numerator


def _rho_numerators(z: tuple[Fraction, ...]) -> tuple[int, ...]:
    """Integer numerators of non-special coordinate polynomials.

    q_S = (c_S z_S)/d_S with d_1=49 and c_S=8 for supports containing
    the repeated 7-coordinate.  Thus all recurrence numerators stay integral.
    """
    if len(z) != 15:
        raise ValueError("need fifteen normalized support charges")
    t = {m: _support_weight(m, z[m - 1]) for m in range(1, 16)}
    n = [0] * 16
    n[0] = 1
    for size in range(1, 5):
        for Cmask in range(1, 16):
            if Cmask.bit_count() != size:
                continue
            pivot = Cmask & -Cmask
            i = pivot.bit_length() - 1
            rest = Cmask ^ pivot
            value = D[i] * n[rest]
            T = rest
            while True:
                S = pivot | T
                value -= t[S] * n[Cmask ^ S]
                if T == 0:
                    break
                T = (T - 1) & rest
            n[Cmask] = value
    return tuple(n)


@lru_cache(maxsize=1)
def _numerator_bounds() -> tuple[tuple[int, ...], tuple[int, ...]]:
    lows = [None] * 16
    highs = [None] * 16
    for endpoint in product((1, 4), repeat=15):
        z = tuple(Fraction(v) for v in endpoint)
        n = _rho_numerators(z)
        for Cmask, value in enumerate(n):
            lows[Cmask] = value if lows[Cmask] is None or value < lows[Cmask] else lows[Cmask]
            highs[Cmask] = value if highs[Cmask] is None or value > highs[Cmask] else highs[Cmask]
    return tuple(lows), tuple(highs)


def _phi_exact(Cmask: int, numerator: int) -> Fraction:
    den = _denominators()
    rho = Fraction(numerator, den[Cmask])
    T = 15 ^ Cmask
    special_mask = 1 | (T << 1)
    lam = LAMBDA.get(special_mask, Fraction(0))
    nu = DIAGONAL[special_mask]
    # b_T for the non-special support is 8/49 on coordinate 7 and 1/p
    # on the three simple coordinates.  The distinguished 5^2 contributes 6/25.
    cT = 8 if T & 1 else 1
    lo = Fraction(6 * cT, 25 * den[T])
    hi = 4 * lo
    x = -(lam - rho) / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + (lam - rho) * x


@lru_cache(maxsize=1)
def _floor_tables():
    lows, highs = _numerator_bounds()
    den = _denominators()
    phi = []
    rho = []
    for Cmask in range(16):
        prow = []
        rrow = []
        for numerator in range(lows[Cmask], highs[Cmask] + 1):
            value = _phi_exact(Cmask, numerator)
            prow.append((value.numerator * Q) // value.denominator)
            value = Fraction(numerator, den[Cmask])
            rrow.append((value.numerator * Q) // value.denominator)
        phi.append(tuple(prow))
        rho.append(tuple(rrow))
    return tuple(phi), tuple(rho), lows


def _lookup(row: tuple[int, ...], low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped endpoint-derived range")
    return row[idx]


def _penalty(A: int, B: int, z: tuple[Fraction, ...]) -> Fraction:
    out = (
        REP_ALPHA[0] * A
        + REP_ALPHA[1] * B
        + REP_BETA[0] * comb(A, 2)
        + REP_BETA[1] * comb(B, 2)
    )
    for mask, (alpha, beta) in zip(SELECTED_SIMPLE, SIMPLE_COEFFICIENTS):
        a = z[mask - 1].numerator - 1
        out += alpha * a + beta * comb(a, 2)
    return out


def _pointwise_exact(A: int, B: int, z: tuple[Fraction, ...]) -> Fraction:
    n = _rho_numerators(z)
    den = _denominators()
    return (
        Fraction(n[15], den[15])
        + sum(_phi_exact(Cmask, n[Cmask]) for Cmask in range(16))
        + _penalty(A, B, z)
    )


@lru_cache(maxsize=1)
def coordinate_box_minimum() -> Fraction:
    """Audit that the full four-coordinate non-special box is in Shearer."""
    den = _denominators()
    best = None
    for endpoint in product((1, 4), repeat=15):
        z = tuple(Fraction(v) for v in endpoint)
        n = _rho_numerators(z)
        local = min(Fraction(n[Cmask], den[Cmask]) for Cmask in range(1, 16))
        best = local if best is None or local < best else best
    assert best == EXPECTED_COORDINATE_MIN > 0
    return best


@lru_cache(maxsize=1)
def pointwise_certificate() -> dict:
    assert factorial_spike_cap(3, 1) == 13
    assert factorial_spike_cap(3, 2) == 5
    assert Q % COEFFICIENT_DEN == 0
    scale = Q // COEFFICIENT_DEN
    phi, rho, lows = _floor_tables()

    best = None
    best_data = None
    checked = 0
    for A in range(4):
        for B in range(4):
            z1 = Fraction(8 + 7 * A + B, 8)
            rep_units = (
                REP_ALPHA_NUM[0] * A
                + REP_ALPHA_NUM[1] * B
                + REP_BETA_NUM[0] * comb(A, 2)
                + REP_BETA_NUM[1] * comb(B, 2)
            )
            for simple_values in product(range(1, 5), repeat=5):
                simple_units = sum(
                    anum * (value - 1) + bnum * comb(value - 1, 2)
                    for value, (anum, bnum) in zip(simple_values, SIMPLE_COEFFICIENT_NUM)
                )
                for endpoints in product((1, 4), repeat=len(UNSELECTED)):
                    z = [Fraction(0)] * 15
                    z[0] = z1
                    for mask, value in zip(SELECTED_SIMPLE, simple_values):
                        z[mask - 1] = Fraction(value)
                    for mask, value in zip(UNSELECTED, endpoints):
                        z[mask - 1] = Fraction(value)
                    zt = tuple(z)
                    n = _rho_numerators(zt)
                    value = scale * (rep_units + simple_units)
                    value += _lookup(rho[15], lows[15], n[15])
                    for Cmask in range(16):
                        value += _lookup(phi[Cmask], lows[Cmask], n[Cmask])
                    checked += 1
                    if best is None or value < best:
                        best = value
                        best_data = (A, B, zt)

    assert checked == EXPECTED_STATE_COUNT
    assert best == EXPECTED_FLOOR_MIN
    assert best_data == (EXPECTED_A_B[0], EXPECTED_A_B[1], tuple(Fraction(v) for v in EXPECTED_Z))
    assert C * Q == 309_460_000_000
    assert best - C * Q == EXPECTED_FLOOR_SLACK > 0
    exact = _pointwise_exact(best_data[0], best_data[1], best_data[2])
    assert exact == EXPECTED_EXACT_ARGMIN > C
    assert Fraction(best, Q) <= exact
    return {
        "state_count": checked,
        "floor_min_scaled": best,
        "floor_slack_scaled": best - C * Q,
        "A_B": EXPECTED_A_B,
        "argmin_z": EXPECTED_Z,
        "exact_argmin_value": exact,
        "verified": True,
    }


def special_global_cost() -> Fraction:
    den = _denominators()
    out = Fraction(0)
    for T in range(16):
        mask = 1 | (T << 1)
        cT = 8 if T & 1 else 1
        b = Fraction(6 * cT, 25 * den[T])
        out += 27 * LAMBDA.get(mask, Fraction(0)) * b
        out += 63 * DIAGONAL[mask] * b * b
    return out


def factorial_global_cost() -> Fraction:
    # A_7 and A_49 separately obey the same single-divisor factorial caps.
    first = sum(REP_ALPHA, Fraction(0)) + sum((a for a, _ in SIMPLE_COEFFICIENTS), Fraction(0))
    second = sum(REP_BETA, Fraction(0)) + sum((b for _, b in SIMPLE_COEFFICIENTS), Fraction(0))
    return 13 * first + 5 * second


def reference_margin() -> Fraction:
    eta = 14 * C - special_global_cost() - factorial_global_cost()
    assert special_global_cost() == EXPECTED_SPECIAL_COST
    assert factorial_global_cost() == EXPECTED_FACTORIAL_COST
    assert eta == EXPECTED_ETA > 0
    return eta


def canonical_seed_numbers() -> tuple[int, ...]:
    canonical = tuple(
        (primes, exponents)
        for primes, exponents in SEEDS[P322]
        if tuple(exponents) == P322
    )
    assert len(canonical) == 6
    nums = tuple(sorted(family_number(primes, exponents) for primes, exponents in canonical))

    # Every simple tuple is coordinatewise no smaller than the reference
    # (11,13,17), so reciprocal baselines are no larger.  The repeated 7^2
    # coordinate is identical.  Inflate grouped q to the reference baselines;
    # normalized activations and all reference moment/factorial budgets survive.
    for primes, _ in canonical:
        simple = tuple(primes[3:])
        assert all(p >= r for p, r in zip(simple, REFERENCE_SIMPLE))
    return nums


@lru_cache(maxsize=1)
def seed_audit() -> dict:
    pointwise = pointwise_certificate()
    clique_min = coordinate_box_minimum()
    eta = reference_margin()
    nums = canonical_seed_numbers()
    assert len(nums) == 6 and clique_min > 0 and eta > 0
    return {
        "pointwise": pointwise,
        "coordinate_box_minimum": clique_min,
        "reference_eta": eta,
        "canonical_seed_numbers": nums,
        "canonical_seed_count": 6,
        "all_canonical_seeds_noncovering": True,
    }


__all__ = [
    "C",
    "EXPECTED_ETA",
    "REFERENCE_SIMPLE",
    "canonical_seed_numbers",
    "coordinate_box_minimum",
    "factorial_global_cost",
    "pointwise_certificate",
    "reference_margin",
    "seed_audit",
    "special_global_cost",
]
