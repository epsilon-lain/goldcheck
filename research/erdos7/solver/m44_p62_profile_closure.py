"""M44: close the full six-prime exponent profile (6,2,1,1,1,1).

M43 reduces P62 to eight exact seeds.  Seven canonical seeds have 3^6*5^2;
one exceptional seed has 3^6*5*7^2.

Canonical branch: build a quantitative goodness certificate at the reference
precursor

    N5 = 3^5 * 5^2 * 7 * 11 * 13 * 17.

The certificate stages on 3^5, distinguishes 5^2, and uses six selected simple
supports at all six activation levels.  Nine remaining supports receive only
linear centered penalties, so separate concavity reduces them to endpoints.
The exact state space is 6^6*2^9=23,887,872.  Its summed-goodness margin is
large enough that the deficiency recurrence lifts 3^5 to 3^6.  Coordinatewise
baseline inflation sends the same reference certificate to all seven canonical
M43 seeds.

Exceptional branch: M36 already proves a quantitative a=5 goodness margin for
3^5*5*7^2*11*13*17.  The same deficiency recurrence lifts that one seed to
3^6.  Thus all eight M43 seeds are noncovering and the whole P62 profile closes.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m28_moment_hierarchy import moment_constant, selected_fibre_count
from m30_centered_moments import factorial_spike_cap
from m36_a5_exceptional_goodness import (
    EXPECTED_GLOBAL_MARGIN as M36_ETA,
    N as M36_N5,
)
from m43_p62_direct_frontier import P612, P62, SEEDS

REFERENCE_J = (7, 11, 13, 17)
DENOMINATORS = tuple(
    prod(REFERENCE_J[i] for i in range(4) if Cmask & (1 << i))
    for Cmask in range(16)
)
J_ORIGINAL = 0b11110
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_ORIGINAL))

SELECTED_SUPPORTS = (1, 2, 4, 8, 3, 5)
UNSELECTED_SUPPORTS = (6, 7, 9, 10, 11, 12, 13, 14, 15)
COEFFICIENT_DEN = 1_000_000
SELECTED_ALPHA_NUM = (18860, 11896, 9760, 6345, 4095, 3068)
SELECTED_BETA_NUM = (18054, 5465, 3740, 2463, 1428, 1217)
UNSELECTED_ALPHA_NUM = (2278, 611, 3458, 1591, 423, 1254, 343, 165, 43)
SELECTED_ALPHA = tuple(Fraction(x, COEFFICIENT_DEN) for x in SELECTED_ALPHA_NUM)
SELECTED_BETA = tuple(Fraction(x, COEFFICIENT_DEN) for x in SELECTED_BETA_NUM)
UNSELECTED_ALPHA = tuple(Fraction(x, COEFFICIENT_DEN) for x in UNSELECTED_ALPHA_NUM)

Q = 10**12
C = Fraction(32999, 100000)
EXPECTED_STATE_COUNT = 6**6 * 2**9
EXPECTED_FLOOR_MIN = 329_998_003_891
EXPECTED_FLOOR_SLACK = 8_003_891
EXPECTED_ARGMIN = (3, 2, 2, 3, 3, 1, 1, 3, 6, 1, 1, 6, 6, 1, 6)
EXPECTED_EXACT_ARGMIN = Fraction(
    90509692970019047913,
    274273455901445000000,
)
EXPECTED_SPECIAL_POINT_MIN = Fraction(3285521839497, 45246607656250)
EXPECTED_SPECIAL_GLOBAL_COST = Fraction(1242244751435847, 45246607656250)
EXPECTED_PENALTY_COST = Fraction(2411069, 250000)
EXPECTED_ETA = Fraction(571830798571397, 180986430625000)
EXPECTED_SIGMA_OVER_M = Fraction(107136, 60775)
EXPECTED_CANONICAL_LIFT_GAP = Fraction(1396444066114191, 180986430625000)
EXPECTED_EXCEPTIONAL_SIGMA_OVER_M = Fraction(147744, 85085)
EXPECTED_EXCEPTIONAL_LIFT_GAP = Fraction(
    71329092093939597,
    14189336161000000,
)

REFERENCE_N5 = 3**5 * 5**2 * 7 * 11 * 13 * 17
REFERENCE_N6 = 3**6 * 5**2 * 7 * 11 * 13 * 17
EXCEPTIONAL_N6 = 3**6 * 5 * 7**2 * 11 * 13 * 17


def _baseline_special(T: int) -> Fraction:
    return Fraction(6, 25 * DENOMINATORS[T])


def special_point_min() -> Fraction:
    out = Fraction(0)
    for T in range(16):
        mask = 1 | (T << 1)
        b = _baseline_special(T)
        out += LAMBDA.get(mask, Fraction(0)) * b + DIAGONAL[mask] * b * b
    assert out == EXPECTED_SPECIAL_POINT_MIN
    return out


def special_global_cost() -> Fraction:
    out = Fraction(0)
    for T in range(16):
        mask = 1 | (T << 1)
        b = _baseline_special(T)
        out += moment_constant(5, 1) * LAMBDA.get(mask, Fraction(0)) * b
        out += moment_constant(5, 2) * DIAGONAL[mask] * b * b
    assert out == EXPECTED_SPECIAL_GLOBAL_COST
    return out


def _phi_exact(Cmask: int, numerator: int) -> Fraction:
    rho = Fraction(numerator, DENOMINATORS[Cmask])
    T = 15 ^ Cmask
    mask = 1 | (T << 1)
    lam = LAMBDA.get(mask, Fraction(0))
    nu = DIAGONAL[mask]
    lo = _baseline_special(T)
    hi = 6 * lo
    x = -(lam - rho) / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + (lam - rho) * x


def _rho_numerators(z: tuple[int, ...]) -> tuple[int, ...]:
    """P_C*rho_C for J=(7,11,13,17), natural subset-mask order."""
    if len(z) != 15 or any(v not in (1, 2, 3, 4, 5, 6) for v in z):
        raise ValueError("z must contain fifteen integers in 1..6")
    (
        z1, z2, z12, z3, z13, z23, z123, z4, z14, z24, z124,
        z34, z134, z234, z1234,
    ) = z
    n1 = 7 - z1
    n2 = 11 - z2
    n3 = 13 - z3
    n4 = 17 - z4
    n12 = n1 * n2 - z12
    n13 = n1 * n3 - z13
    n23 = n2 * n3 - z23
    n14 = n1 * n4 - z14
    n24 = n2 * n4 - z24
    n34 = n3 * n4 - z34
    n123 = n1 * n23 - z12 * n3 - z13 * n2 - z123
    n124 = n1 * n24 - z12 * n4 - z14 * n2 - z124
    n134 = n1 * n34 - z13 * n4 - z14 * n3 - z134
    n234 = n2 * n34 - z23 * n4 - z24 * n3 - z234
    n1234 = (
        n1 * n234
        - z12 * n34
        - z13 * n24
        - z14 * n23
        - z123 * n4
        - z124 * n3
        - z134 * n2
        - z1234
    )
    return (
        1, n1, n2, n12, n3, n13, n23, n123,
        n4, n14, n24, n124, n34, n134, n234, n1234,
    )


def _penalty(z: tuple[int, ...]) -> Fraction:
    out = Fraction(0)
    for mask, alpha, beta in zip(SELECTED_SUPPORTS, SELECTED_ALPHA, SELECTED_BETA):
        A = z[mask - 1] - 1
        out += alpha * A + beta * comb(A, 2)
    for mask, alpha in zip(UNSELECTED_SUPPORTS, UNSELECTED_ALPHA):
        out += alpha * (z[mask - 1] - 1)
    return out


def _full_branch_exact(z: tuple[int, ...]) -> Fraction:
    n = _rho_numerators(z)
    return (
        Fraction(n[15], DENOMINATORS[15])
        + sum(_phi_exact(Cmask, n[Cmask]) for Cmask in range(16))
    )


def _reduced_goodness_exact(z: tuple[int, ...]) -> Fraction:
    n = _rho_numerators(z)
    P0 = special_point_min()
    branches = [_full_branch_exact(z)]
    branches.extend(P0 + Fraction(n[Cmask], DENOMINATORS[Cmask]) for Cmask in range(1, 16))
    return min(branches)


@lru_cache(maxsize=1)
def _numerator_bounds() -> tuple[tuple[int, ...], tuple[int, ...]]:
    lows = [None] * 16
    highs = [None] * 16
    for endpoint in product((1, 6), repeat=15):
        n = _rho_numerators(endpoint)
        for Cmask, value in enumerate(n):
            lows[Cmask] = value if lows[Cmask] is None or value < lows[Cmask] else lows[Cmask]
            highs[Cmask] = value if highs[Cmask] is None or value > highs[Cmask] else highs[Cmask]
    return tuple(lows), tuple(highs)


@lru_cache(maxsize=1)
def _floor_tables():
    P0 = special_point_min()
    lows, highs = _numerator_bounds()
    phi = []
    coordinate = []
    rho = []
    for Cmask, P in enumerate(DENOMINATORS):
        prow = []
        crow = []
        rrow = []
        for numerator in range(lows[Cmask], highs[Cmask] + 1):
            value = _phi_exact(Cmask, numerator)
            prow.append((value.numerator * Q) // value.denominator)
            value = P0 + Fraction(numerator, P)
            crow.append((value.numerator * Q) // value.denominator)
            value = Fraction(numerator, P)
            rrow.append((value.numerator * Q) // value.denominator)
        phi.append(tuple(prow))
        coordinate.append(tuple(crow))
        rho.append(tuple(rrow))
    return tuple(phi), tuple(coordinate), tuple(rho), lows


def _lookup(row: tuple[int, ...], low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped endpoint-derived range")
    return row[idx]


@lru_cache(maxsize=1)
def pointwise_goodness_certificate() -> dict:
    assert selected_fibre_count(5) == 122
    assert factorial_spike_cap(5, 1) == 121
    assert factorial_spike_cap(5, 2) == 58
    assert Q % COEFFICIENT_DEN == 0
    scale = Q // COEFFICIENT_DEN
    phi, coordinate, rho, lows = _floor_tables()

    unselected_states = tuple(product((1, 6), repeat=9))
    unselected_penalty_units = tuple(
        sum(alpha * (value - 1) for alpha, value in zip(UNSELECTED_ALPHA_NUM, state))
        for state in unselected_states
    )

    best = None
    best_state = None
    checked = 0
    for z1, z2, z3, z4, z12, z13 in product(range(1, 7), repeat=6):
        n1 = 7 - z1
        n2 = 11 - z2
        n3 = 13 - z3
        n4 = 17 - z4
        n12 = n1 * n2 - z12
        n13 = n1 * n3 - z13
        selected = (z1, z2, z3, z4, z12, z13)
        selected_units = sum(
            anum * (value - 1) + bnum * comb(value - 1, 2)
            for value, anum, bnum in zip(selected, SELECTED_ALPHA_NUM, SELECTED_BETA_NUM)
        )

        phi_constant = 0
        for Cmask, numerator in (
            (0, 1), (1, n1), (2, n2), (3, n12),
            (4, n3), (5, n13), (8, n4),
        ):
            phi_constant += _lookup(phi[Cmask], lows[Cmask], numerator)

        for state_index, (
            z23, z123, z14, z24, z124, z34, z134, z234, z1234,
        ) in enumerate(unselected_states):
            n23 = n2 * n3 - z23
            n14 = n1 * n4 - z14
            n24 = n2 * n4 - z24
            n34 = n3 * n4 - z34
            n123 = n1 * n23 - z12 * n3 - z13 * n2 - z123
            n124 = n1 * n24 - z12 * n4 - z14 * n2 - z124
            n134 = n1 * n34 - z13 * n4 - z14 * n3 - z134
            n234 = n2 * n34 - z23 * n4 - z24 * n3 - z234
            n1234 = (
                n1 * n234
                - z12 * n34
                - z13 * n24
                - z14 * n23
                - z123 * n4
                - z124 * n3
                - z134 * n2
                - z1234
            )
            nvals = (
                1, n1, n2, n12, n3, n13, n23, n123,
                n4, n14, n24, n124, n34, n134, n234, n1234,
            )
            penalty_scaled = scale * (selected_units + unselected_penalty_units[state_index])
            full_lower = penalty_scaled + phi_constant
            for Cmask in (6, 7, 9, 10, 11, 12, 13, 14, 15):
                full_lower += _lookup(phi[Cmask], lows[Cmask], nvals[Cmask])
            full_lower += _lookup(rho[15], lows[15], n1234)

            goodness_lower = full_lower
            for Cmask in range(1, 16):
                branch = penalty_scaled + _lookup(coordinate[Cmask], lows[Cmask], nvals[Cmask])
                if branch < goodness_lower:
                    goodness_lower = branch

            checked += 1
            if best is None or goodness_lower < best:
                best = goodness_lower
                best_state = (
                    z1, z2, z12, z3, z13, z23, z123, z4,
                    z14, z24, z124, z34, z134, z234, z1234,
                )

    assert checked == EXPECTED_STATE_COUNT
    assert best == EXPECTED_FLOOR_MIN
    assert best_state == EXPECTED_ARGMIN
    assert C * Q == 329_990_000_000
    assert best - C * Q == EXPECTED_FLOOR_SLACK > 0
    exact = _reduced_goodness_exact(EXPECTED_ARGMIN) + _penalty(EXPECTED_ARGMIN)
    assert exact == EXPECTED_EXACT_ARGMIN > C
    assert Fraction(best, Q) <= exact
    return {
        "state_count": checked,
        "floor_min_scaled": best,
        "floor_slack_scaled": best - C * Q,
        "argmin": best_state,
        "exact_argmin_value": exact,
        "verified": True,
    }


def penalty_global_cost() -> Fraction:
    first = sum(SELECTED_ALPHA, Fraction(0)) + sum(UNSELECTED_ALPHA, Fraction(0))
    second = sum(SELECTED_BETA, Fraction(0))
    out = 121 * first + 58 * second
    assert out == EXPECTED_PENALTY_COST
    return out


def reference_margin() -> Fraction:
    eta = 122 * C - special_global_cost() - penalty_global_cost()
    assert eta == EXPECTED_ETA > 0
    return eta


def sigma_over_M_reference() -> Fraction:
    out = Fraction(31, 25)
    for p in REFERENCE_J:
        out *= Fraction(p + 1, p)
    assert out == EXPECTED_SIGMA_OVER_M
    return out


def canonical_lift_gap() -> Fraction:
    gap = 3 * reference_margin() - sigma_over_M_reference()
    assert gap == EXPECTED_CANONICAL_LIFT_GAP > 0
    return gap


def exceptional_lift_gap() -> Fraction:
    assert M36_N5 == 3**5 * 5 * 7**2 * 11 * 13 * 17
    ratio = Fraction(6, 5) * Fraction(57, 49) * Fraction(12, 11) * Fraction(14, 13) * Fraction(18, 17)
    assert ratio == EXPECTED_EXCEPTIONAL_SIGMA_OVER_M
    gap = 3 * M36_ETA - ratio
    assert gap == EXPECTED_EXCEPTIONAL_LIFT_GAP > 0
    return gap


def seed_accounting() -> dict:
    canonical = [(primes, exp) for primes, exp in SEEDS if exp == P62]
    exceptional = [(primes, exp) for primes, exp in SEEDS if exp == P612]
    assert len(canonical) == 7 and len(exceptional) == 1
    for primes, _ in canonical:
        actual_J = tuple(primes[2:])
        assert all(p >= r for p, r in zip(actual_J, REFERENCE_J))
    assert exceptional[0][0] == (3, 5, 7, 11, 13, 17)
    return {
        "canonical_seed_count": 7,
        "exceptional_seed_count": 1,
        "all_eight_seeds_accounted_for": True,
    }


@lru_cache(maxsize=1)
def profile_audit() -> dict:
    pointwise = pointwise_goodness_certificate()
    eta = reference_margin()
    cgap = canonical_lift_gap()
    egap = exceptional_lift_gap()
    accounting = seed_accounting()
    assert eta > 0 and cgap > 0 and egap > 0
    return {
        "profile": P62,
        "reference_N5": REFERENCE_N5,
        "reference_N6": REFERENCE_N6,
        "exceptional_N6": EXCEPTIONAL_N6,
        "pointwise": pointwise,
        "reference_eta": eta,
        "canonical_lift_gap": cgap,
        "exceptional_lift_gap": egap,
        "seed_accounting": accounting,
        "all_P62_numbers_noncovering": True,
    }


__all__ = [
    "C",
    "EXPECTED_ETA",
    "P62",
    "canonical_lift_gap",
    "exceptional_lift_gap",
    "penalty_global_cost",
    "pointwise_goodness_certificate",
    "profile_audit",
    "reference_margin",
    "seed_accounting",
    "special_global_cost",
]
