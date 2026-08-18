"""M36: exact a=5 factorial-goodness certificate for the exceptional P52 seed.

Target
------
    N = 3^5 * 5 * 7^2 * 11 * 13 * 17.

M35 quantitatively lifts five of the six canonical (5,2,1,1,1,1) seeds.  The
remaining M26 exceptional placement has the square on prime 7.  M36 attacks it
directly at the 3^5 stage.

Distinguish the repeated post-stage coordinate 7^2.  The other four coordinates
5,11,13,17 are simple, so every nonempty support among them corresponds to one
exact divisor and has

    z_S = q_S/b_S = 1 + A_S in {1,...,6}.

M30 gives the a=5 factorial budgets

    sum A_S <= F(5,1)=121,
    sum binom(A_S,2) <= F(5,2)=58.

As in M33, use the goodness functional

    g(q) = min(rho_full(q), rho_C(q^0) for nonempty C subset J).

Thus g(q)>0 simultaneously puts the non-special system in the Clique-Shearer
region and makes the full five-coordinate polynomial positive.  The relative
one-coordinate completion argument then leaves an uncovered point.

The frozen M25 linear/diagonal special-coordinate penalties are minimized
exactly.  Six non-special variables receive nonnegative first/second factorial
penalties.  They are checked at all six integer levels; the other nine variables
have no new penalty and minimize at box endpoints by separate concavity.  The
complete pointwise state space is

    6^6 * 2^9 = 23,887,872.

Lookup entries are built with Fraction, multiplied by Q=10^12, and rounded
down.  The exhaustive loop therefore uses integer lower bounds only.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m28_moment_hierarchy import moment_constant, selected_fibre_count
from m30_centered_moments import factorial_spike_cap

N = 3**5 * 5 * 7**2 * 11 * 13 * 17
J_PRIMES = (5, 11, 13, 17)
DENOMINATORS = tuple(
    prod(J_PRIMES[i] for i in range(4) if C & (1 << i))
    for C in range(16)
)
# Bit 0 is the distinguished repeated coordinate 7^2; bits 1..4 are 5,11,13,17.
BASE_COORDS = (
    Fraction(8, 49),
    Fraction(1, 5),
    Fraction(1, 11),
    Fraction(1, 13),
    Fraction(1, 17),
)
J_ORIGINAL = 0b11110
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_ORIGINAL))

# Normalized non-special supports {5},{11},{13},{17},{5,11},{5,13}.
SELECTED_SUPPORTS = (2, 4, 8, 16, 6, 10)
COEFFICIENT_DEN = 1_000_000
COEFFICIENT_NUMERATORS = (
    (55520, 32504),
    (16007, 4671),
    (13335, 2716),
    (10803, 1636),
    (8762, 2963),
    (7194, 1580),
)
ALPHA = tuple(Fraction(a, COEFFICIENT_DEN) for a, _ in COEFFICIENT_NUMERATORS)
BETA = tuple(Fraction(b, COEFFICIENT_DEN) for _, b in COEFFICIENT_NUMERATORS)

Q = 10**12
C = Fraction(2929, 10000)
EXPECTED_STATE_COUNT = 6**6 * 2**9
EXPECTED_FLOOR_MIN = 292_944_712_245
EXPECTED_FLOOR_SLACK = 44_712_245
EXPECTED_ARGMIN = (1, 6, 2, 1, 1, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6)
EXPECTED_EXACT_ARGMIN = Fraction(
    47181019651823844673970073,
    161057761680622927120000000,
)
EXPECTED_SPECIAL_POINT_MIN = Fraction(2324089726722, 44341675503125)
EXPECTED_SPECIAL_GLOBAL_COST = Fraction(767161507789382, 44341675503125)
EXPECTED_FACTORIAL_COST = Fraction(16178201, 1000000)
EXPECTED_GLOBAL_MARGIN = Fraction(
    31989285548113199,
    14189336161000000,
)


def baseline(mask: int) -> Fraction:
    if not 1 <= mask < 32:
        raise ValueError("support mask must be in 1..31")
    out = Fraction(1)
    for i, x in enumerate(BASE_COORDS):
        if mask & (1 << i):
            out *= x
    return out


def special_point_min() -> Fraction:
    """Minimum frozen special penalty, attained at all lower endpoints."""
    return sum(
        LAMBDA.get(1 | T, Fraction(0)) * baseline(1 | T)
        + DIAGONAL[1 | T] * baseline(1 | T) ** 2
        for T in J_SUBSETS
    )


def special_global_cost() -> Fraction:
    """a=5 raw first/second moment cost of the frozen special penalties."""
    return (
        moment_constant(5, 1)
        * sum(
            LAMBDA.get(1 | T, Fraction(0)) * baseline(1 | T)
            for T in J_SUBSETS
        )
        + moment_constant(5, 2)
        * sum(
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
    hi = 6 * lo
    x = -linear / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + linear * x


def _rho_numerators(z: tuple[int, ...]) -> tuple[int, ...]:
    """P_C*rho_C for J=(5,11,13,17), in normalized subset order."""
    if len(z) != 15 or any(v not in (1, 2, 3, 4, 5, 6) for v in z):
        raise ValueError("z must contain fifteen integers in 1..6")
    (
        z1, z2, z12, z3, z13, z23, z123, z4, z14, z24, z124,
        z34, z134, z234, z1234,
    ) = z

    n1 = 5 - z1
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
    out = Fraction(0)
    for value, alpha, beta in zip(selected, ALPHA, BETA):
        A = value - 1
        out += alpha * A + beta * comb(A, 2)
    return out


def _full_branch_exact(z: tuple[int, ...]) -> Fraction:
    n = _rho_numerators(z)
    value = Fraction(n[15], DENOMINATORS[15])
    value += sum(_phi_exact(Cmask, n[Cmask]) for Cmask in range(16))
    return value


def _reduced_goodness_exact(z: tuple[int, ...]) -> Fraction:
    n = _rho_numerators(z)
    P0 = special_point_min()
    branches = [_full_branch_exact(z)]
    branches.extend(
        P0 + Fraction(n[Cmask], DENOMINATORS[Cmask])
        for Cmask in range(1, 16)
    )
    return min(branches)


@lru_cache(maxsize=1)
def _numerator_bounds() -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Exact box extrema for every multi-affine coordinate numerator."""
    lows = [None] * 16
    highs = [None] * 16
    for z in product((1, 6), repeat=15):
        n = _rho_numerators(z)
        for Cmask, value in enumerate(n):
            if lows[Cmask] is None or value < lows[Cmask]:
                lows[Cmask] = value
            if highs[Cmask] is None or value > highs[Cmask]:
                highs[Cmask] = value
    return tuple(lows), tuple(highs)


@lru_cache(maxsize=1)
def _floor_tables():
    """Build rigorous Q-scaled lower tables from exact Fractions."""
    P0 = special_point_min()
    lows, highs = _numerator_bounds()
    phi_tables = []
    coordinate_tables = []
    rho_tables = []
    for Cmask, P in enumerate(DENOMINATORS):
        phi_row = []
        coordinate_row = []
        rho_row = []
        for numerator in range(lows[Cmask], highs[Cmask] + 1):
            value = _phi_exact(Cmask, numerator)
            phi_row.append((value.numerator * Q) // value.denominator)
            value = P0 + Fraction(numerator, P)
            coordinate_row.append((value.numerator * Q) // value.denominator)
            value = Fraction(numerator, P)
            rho_row.append((value.numerator * Q) // value.denominator)
        phi_tables.append(tuple(phi_row))
        coordinate_tables.append(tuple(coordinate_row))
        rho_tables.append(tuple(rho_row))
    return (
        tuple(phi_tables), tuple(coordinate_tables), tuple(rho_tables),
        lows, highs,
    )


def _lookup(row: tuple[int, ...], low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped exact endpoint-derived range")
    return row[idx]


@lru_cache(maxsize=1)
def pointwise_goodness_certificate() -> dict:
    """Exhaust all 23,887,872 reduced states with integer lower bounds."""
    assert selected_fibre_count(5) == 122
    assert factorial_spike_cap(5, 1) == 121
    assert factorial_spike_cap(5, 2) == 58
    assert Q % COEFFICIENT_DEN == 0
    assert special_point_min() == EXPECTED_SPECIAL_POINT_MIN

    scale = Q // COEFFICIENT_DEN
    phi, coordinate, rho, lows, _ = _floor_tables()
    unselected_states = tuple(product((1, 6), repeat=9))

    best = None
    best_state = None
    checked = 0

    # Integral selected variables: z1,z2,z3,z4,z12,z13.
    for z1, z2, z3, z4, z12, z13 in product(range(1, 7), repeat=6):
        n1 = 5 - z1
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

            full_lower = constant
            for Cmask in (6, 7, 9, 10, 11, 12, 13, 14, 15):
                full_lower += _lookup(phi[Cmask], lows[Cmask], nvals[Cmask])
            full_lower += _lookup(rho[15], lows[15], n1234)

            goodness_lower = full_lower
            for Cmask in range(1, 16):
                branch = penalty_scaled + _lookup(
                    coordinate[Cmask], lows[Cmask], nvals[Cmask]
                )
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
    assert C * Q == 292_900_000_000
    assert best - C * Q == EXPECTED_FLOOR_SLACK > 0

    exact_at_argmin = (
        _reduced_goodness_exact(EXPECTED_ARGMIN)
        + _factorial_penalty(EXPECTED_ARGMIN)
    )
    assert exact_at_argmin == EXPECTED_EXACT_ARGMIN
    assert Fraction(best, Q) <= exact_at_argmin
    assert exact_at_argmin > C

    return {
        "state_count": checked,
        "floor_min_scaled": best,
        "floor_min": Fraction(best, Q),
        "pointwise_C": C,
        "floor_slack_scaled": best - C * Q,
        "argmin": best_state,
        "exact_argmin_value": exact_at_argmin,
        "verified": True,
    }


def factorial_global_cost() -> Fraction:
    return (
        factorial_spike_cap(5, 1) * sum(ALPHA, Fraction(0))
        + factorial_spike_cap(5, 2) * sum(BETA, Fraction(0))
    )


@lru_cache(maxsize=1)
def seed_certificate() -> dict:
    pointwise = pointwise_goodness_certificate()
    assert special_global_cost() == EXPECTED_SPECIAL_GLOBAL_COST
    assert factorial_global_cost() == EXPECTED_FACTORIAL_COST

    margin = (
        selected_fibre_count(5) * C
        - special_global_cost()
        - factorial_global_cost()
    )
    assert margin == EXPECTED_GLOBAL_MARGIN > 0
    return {
        "N": N,
        "pointwise": pointwise,
        "special_point_min": special_point_min(),
        "special_global_cost": special_global_cost(),
        "factorial_global_cost": factorial_global_cost(),
        "summed_goodness_margin": margin,
        "noncovering_certified": True,
    }


__all__ = [
    "C",
    "COEFFICIENT_NUMERATORS",
    "EXPECTED_GLOBAL_MARGIN",
    "EXPECTED_STATE_COUNT",
    "N",
    "factorial_global_cost",
    "pointwise_goodness_certificate",
    "seed_certificate",
    "special_global_cost",
    "special_point_min",
]
