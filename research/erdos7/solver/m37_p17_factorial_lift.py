"""M37: repeated-support factorial information closes the final canonical P52 seed.

Target
------
    N5 = 3^5 * 5^2 * 7 * 11 * 13 * 17.

M35 could not lift this seed using the old M16/M25 quantitative margins.  M37
strengthens the a=4 precursor

    N4 = 3^4 * 5^2 * 7 * 11 * 13 * 17

with the M30 single-divisor factorial constraints on six non-5 supports.

At the a=4 stage each non-5 support among 7,11,13,17 has one exact divisor, so
z_S=q_S/b_S=1+A_S is integral in {1,...,5}, with

    sum A_S <= 40,
    sum binom(A_S,2) <= 18.

The pointwise certificate keeps the nonnegative M25 linear/diagonal penalties
on the sixteen supports containing prime 5, and adds six first/second factorial
penalties.  Six variables are checked at all five integer levels and the other
nine at endpoints by separate concavity: 5^6*2^9=8,000,000 states.

The resulting summed rho margin is quantitative.  The M16 completion audit says
rho>0 gives an actual uncovered proportion at least rho; hence delta(N4) is at
least M times the summed margin.  The deficiency recurrence then proves N5
noncovering.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb, prod

from m16_quadratic_frontier import frontier_certificate
from m25_cross_support_seed import DIAGONAL, LAMBDA
from m30_centered_moments import factorial_spike_cap

N4 = 3**4 * 5**2 * 7 * 11 * 13 * 17
N5 = 3**5 * 5**2 * 7 * 11 * 13 * 17
M = 5**2 * 7 * 11 * 13 * 17
J_PRIMES = (7, 11, 13, 17)
DENOMINATORS = tuple(
    prod(J_PRIMES[i] for i in range(4) if C & (1 << i))
    for C in range(16)
)
# Bit 0 is distinguished prime 5 (with exact M-part powers 5 and 25).
BASE_COORDS = (
    Fraction(6, 25),
    Fraction(1, 7),
    Fraction(1, 11),
    Fraction(1, 13),
    Fraction(1, 17),
)
J_ORIGINAL = 0b11110
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_ORIGINAL))

SELECTED_SUPPORTS = (2, 4, 8, 16, 6, 10)
COEFFICIENT_DEN = 1_000_000
COEFFICIENT_NUMERATORS = (
    (28506, 13846),
    (15147, 4601),
    (11878, 3468),
    (9885, 1278),
    (4026, 1511),
    (2880, 1481),
)
ALPHA = tuple(Fraction(a, COEFFICIENT_DEN) for a, _ in COEFFICIENT_NUMERATORS)
BETA = tuple(Fraction(b, COEFFICIENT_DEN) for _, b in COEFFICIENT_NUMERATORS)

Q = 10**12
C = Fraction(3971, 12500)  # 0.31768
EXPECTED_STATE_COUNT = 5**6 * 2**9
EXPECTED_FLOOR_MIN = 317_680_825_425
EXPECTED_FLOOR_SLACK = 825_425
EXPECTED_ARGMIN = (5, 1, 4, 1, 4, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5)
EXPECTED_EXACT_ARGMIN = Fraction(
    268054818379928913,
    843786583640000000,
)
EXPECTED_SPECIAL_GLOBAL_COST = Fraction(409948781722209, 45246607656250)
EXPECTED_FACTORIAL_COST = Fraction(336421, 100000)
EXPECTED_SUMMED_RHO_MARGIN = Fraction(
    434620215428731,
    723945722500000,
)
EXPECTED_SIGMA_OVER_M = Fraction(107136, 60775)
EXPECTED_LIFT_GAP = Fraction(
    27667327886193,
    723945722500000,
)


def baseline(mask: int) -> Fraction:
    if not 1 <= mask < 32:
        raise ValueError("support mask must be in 1..31")
    out = Fraction(1)
    for i, x in enumerate(BASE_COORDS):
        if mask & (1 << i):
            out *= x
    return out


def special_global_cost() -> Fraction:
    return (
        81 * sum(
            LAMBDA.get(1 | T, Fraction(0)) * baseline(1 | T)
            for T in J_SUBSETS
        )
        + 197 * sum(
            DIAGONAL[1 | T] * baseline(1 | T) ** 2
            for T in J_SUBSETS
        )
    )


def _phi_exact(Cmask: int, numerator: int) -> Fraction:
    complement = 15 ^ Cmask
    special_mask = 1 | (complement << 1)
    rho = Fraction(numerator, DENOMINATORS[Cmask])
    linear = LAMBDA.get(special_mask, Fraction(0)) - rho
    nu = DIAGONAL[special_mask]
    lo = baseline(special_mask)
    hi = 5 * lo
    x = -linear / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + linear * x


def _rho_numerators(z: tuple[int, ...]) -> tuple[int, ...]:
    if len(z) != 15 or any(v not in (1, 2, 3, 4, 5) for v in z):
        raise ValueError("z must contain fifteen integers in 1..5")
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


def _factorial_penalty(z: tuple[int, ...]) -> Fraction:
    selected = (z[0], z[1], z[3], z[7], z[2], z[4])
    return sum(
        alpha * (value - 1) + beta * comb(value - 1, 2)
        for value, alpha, beta in zip(selected, ALPHA, BETA)
    )


def _pointwise_exact(z: tuple[int, ...]) -> Fraction:
    n = _rho_numerators(z)
    return (
        Fraction(n[15], DENOMINATORS[15])
        + sum(_phi_exact(Cmask, n[Cmask]) for Cmask in range(16))
        + _factorial_penalty(z)
    )


@lru_cache(maxsize=1)
def _numerator_bounds() -> tuple[tuple[int, ...], tuple[int, ...]]:
    lows = [None] * 16
    highs = [None] * 16
    for z in product((1, 5), repeat=15):
        n = _rho_numerators(z)
        for Cmask, value in enumerate(n):
            if lows[Cmask] is None or value < lows[Cmask]:
                lows[Cmask] = value
            if highs[Cmask] is None or value > highs[Cmask]:
                highs[Cmask] = value
    return tuple(lows), tuple(highs)


@lru_cache(maxsize=1)
def _floor_tables():
    lows, highs = _numerator_bounds()
    phi = []
    rho = []
    for Cmask, P in enumerate(DENOMINATORS):
        prow = []
        rrow = []
        for numerator in range(lows[Cmask], highs[Cmask] + 1):
            value = _phi_exact(Cmask, numerator)
            prow.append((value.numerator * Q) // value.denominator)
            value = Fraction(numerator, P)
            rrow.append((value.numerator * Q) // value.denominator)
        phi.append(tuple(prow))
        rho.append(tuple(rrow))
    return tuple(phi), tuple(rho), lows


def _lookup(row: tuple[int, ...], low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped endpoint-derived range")
    return row[idx]


@lru_cache(maxsize=1)
def pointwise_certificate() -> dict:
    assert factorial_spike_cap(4, 1) == 40
    assert factorial_spike_cap(4, 2) == 18
    assert Q % COEFFICIENT_DEN == 0
    scale = Q // COEFFICIENT_DEN
    phi, rho, lows = _floor_tables()
    unselected_states = tuple(product((1, 5), repeat=9))

    best = None
    best_state = None
    checked = 0
    for z1, z2, z3, z4, z12, z13 in product(range(1, 6), repeat=6):
        n1 = 7 - z1
        n2 = 11 - z2
        n3 = 13 - z3
        n4 = 17 - z4
        n12 = n1 * n2 - z12
        n13 = n1 * n3 - z13
        selected = (z1, z2, z3, z4, z12, z13)
        penalty_units = 0
        for value, (anum, bnum) in zip(selected, COEFFICIENT_NUMERATORS):
            A = value - 1
            penalty_units += anum * A + bnum * comb(A, 2)
        penalty_scaled = scale * penalty_units

        constant = penalty_scaled
        for Cmask, numerator in (
            (0, 1), (1, n1), (2, n2), (3, n12),
            (4, n3), (5, n13), (8, n4),
        ):
            constant += _lookup(phi[Cmask], lows[Cmask], numerator)

        for (
            z23, z123, z14, z24, z124, z34, z134, z234, z1234,
        ) in unselected_states:
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
            value = constant
            for Cmask in (6, 7, 9, 10, 11, 12, 13, 14, 15):
                value += _lookup(phi[Cmask], lows[Cmask], nvals[Cmask])
            value += _lookup(rho[15], lows[15], n1234)

            checked += 1
            if best is None or value < best:
                best = value
                best_state = (
                    z1, z2, z12, z3, z13, z23, z123, z4,
                    z14, z24, z124, z34, z134, z234, z1234,
                )

    assert checked == EXPECTED_STATE_COUNT
    assert best == EXPECTED_FLOOR_MIN
    assert best_state == EXPECTED_ARGMIN
    assert C * Q == 317_680_000_000
    assert best - C * Q == EXPECTED_FLOOR_SLACK > 0
    exact = _pointwise_exact(EXPECTED_ARGMIN)
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


def factorial_global_cost() -> Fraction:
    return 40 * sum(ALPHA, Fraction(0)) + 18 * sum(BETA, Fraction(0))


def sigma_over_M() -> Fraction:
    out = Fraction(31, 25)
    for p in J_PRIMES:
        out *= Fraction(p + 1, p)
    return out


@lru_cache(maxsize=1)
def seed_certificate() -> dict:
    pointwise = pointwise_certificate()
    completion = frontier_certificate(17)
    assert completion["proper_non5_min"] > 0
    assert completion["completion_upper_max"] < 0
    assert special_global_cost() == EXPECTED_SPECIAL_GLOBAL_COST
    assert factorial_global_cost() == EXPECTED_FACTORIAL_COST

    eta = 41 * C - special_global_cost() - factorial_global_cost()
    assert eta == EXPECTED_SUMMED_RHO_MARGIN > 0
    assert sigma_over_M() == EXPECTED_SIGMA_OVER_M
    gap = 3 * eta - sigma_over_M()
    assert gap == EXPECTED_LIFT_GAP > 0

    # delta(N4) >= M*eta, hence
    # delta(N5) >= 3*M*eta - sigma(M) = M*gap > 0.
    return {
        "N4": N4,
        "N5": N5,
        "pointwise": pointwise,
        "summed_rho_margin": eta,
        "sigma_over_M": sigma_over_M(),
        "normalized_lift_gap": gap,
        "deficiency_lower_bound_N5": M * gap,
        "noncovering_certified": True,
    }


__all__ = [
    "C",
    "EXPECTED_LIFT_GAP",
    "EXPECTED_SUMMED_RHO_MARGIN",
    "N4",
    "N5",
    "factorial_global_cost",
    "pointwise_certificate",
    "seed_certificate",
    "sigma_over_M",
    "special_global_cost",
]
