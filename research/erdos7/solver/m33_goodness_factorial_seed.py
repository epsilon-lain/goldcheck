"""M33: exact factorial goodness certificate for the last M27 (4,4) seed.

Target
------
    N = 3^4 * 5 * 7^4 * 11 * 13 * 17.

For this asymmetric seed, keep staging modulo 3^4=81 but use the repeated
prime 7 as the distinguished Clique-Shearer completion coordinate.  The four
non-special coordinates are then the simple primes 5,11,13,17, so every one of
their fifteen square-free supports has exactly one exact divisor and hence an
integer activation variable z_S=1+A_S in {1,...,5}.

The difficulty is that the non-special box is not uniformly inside the
Clique-Shearer region.  M33 avoids any implication audit by certifying a
stronger per-fibre goodness functional

    g(q) = min( rho_full(q), rho_C(q^0) for nonempty C subset {5,11,13,17} ).

If g(q)>0, the non-special system is in the Clique-Shearer region and the full
five-coordinate polynomial is positive, so the M14 one-coordinate completion
argument leaves an uncovered point.

Add the frozen M25 linear/diagonal penalties on the sixteen supports containing
the distinguished 7-coordinate.  For fixed non-special q^0, minimizing

g(q) + special_penalty

over the special variables is exact: the full-rho branch gives the usual
clipped-quadratic base B(q^0), while a coordinate branch gives

    rho_C(q^0) + P0,

where P0 is the special penalty at all lower endpoints.  Therefore the reduced
base is

    G(q^0) = min(B(q^0), P0+rho_C(q^0) for C != empty).

G is separately concave in all fifteen non-special variables.  M33 adds the
M30 factorial penalties to six supports and exhausts 5^6*2^9=8,000,000 states.
The verifier uses exact Fraction-built lookup tables rounded downward at
Q=10^12 and an integer-only exhaustive loop.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA

N = 3**4 * 5 * 7**4 * 11 * 13 * 17
J_PRIMES = (5, 11, 13, 17)
DENOMINATORS = tuple(
    prod(J_PRIMES[i] for i in range(4) if C & (1 << i))
    for C in range(16)
)
# Bit 0 is the distinguished repeated prime 7; bits 1..4 are 5,11,13,17.
BASE_COORDS = (
    Fraction(400, 2401),
    Fraction(1, 5),
    Fraction(1, 11),
    Fraction(1, 13),
    Fraction(1, 17),
)
J_ORIGINAL = 0b11110
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_ORIGINAL))

SELECTED_SUPPORTS = (2, 4, 8, 16, 6, 10)
COEFFICIENT_DEN = 1_000_000
COEFFICIENT_NUMERATORS = (
    (54506, 31667),
    (15997, 4353),
    (13268, 2571),
    (10495, 1509),
    (8673, 1858),
    (6719, 3325),
)
ALPHA = tuple(Fraction(a, COEFFICIENT_DEN) for a, _ in COEFFICIENT_NUMERATORS)
BETA = tuple(Fraction(b, COEFFICIENT_DEN) for _, b in COEFFICIENT_NUMERATORS)

Q = 10**12
C = Fraction(3, 10)
EXPECTED_FLOOR_MIN = 303_809_359_581
EXPECTED_FLOOR_SLACK = 3_809_359_581
EXPECTED_ARGMIN = (3, 1, 4, 1, 3, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5)
EXPECTED_EXACT_ARGMIN = Fraction(
    2639033771723344936606712407,
    8686479492576292487080000000,
)
EXPECTED_SPECIAL_POINT_MIN = Fraction(45778312503188, 851714903064025)
EXPECTED_SPECIAL_GLOBAL_COST = Fraction(5019735697491668, 851714903064025)
EXPECTED_FACTORIAL_COST = Fraction(2600707, 500000)
EXPECTED_GLOBAL_MARGIN = Fraction(
    20524715787799539373,
    17034298061280500000,
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
    """Minimum of the nonnegative frozen special penalty, at lower endpoints."""
    return sum(
        LAMBDA.get(1 | T, Fraction(0)) * baseline(1 | T)
        + DIAGONAL[1 | T] * baseline(1 | T) ** 2
        for T in J_SUBSETS
    )


def special_global_cost() -> Fraction:
    """M15 first/second-moment cost of the frozen distinguished-7 penalties."""
    linear = 81 * sum(
        LAMBDA.get(1 | T, Fraction(0)) * baseline(1 | T)
        for T in J_SUBSETS
    )
    diagonal = 197 * sum(
        DIAGONAL[1 | T] * baseline(1 | T) ** 2
        for T in J_SUBSETS
    )
    return linear + diagonal


def _phi_exact(Cmask: int, numerator: int) -> Fraction:
    complement = 15 ^ Cmask
    original_T = complement << 1
    special_mask = 1 | original_T
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
    """P_C*rho_C for J=(5,11,13,17), in normalized subset order."""
    if len(z) != 15 or any(v not in (1, 2, 3, 4, 5) for v in z):
        raise ValueError("z must contain fifteen integers in 1..5")
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
    branches = [_full_branch_exact(z)]
    P0 = special_point_min()
    branches.extend(
        P0 + Fraction(n[Cmask], DENOMINATORS[Cmask])
        for Cmask in range(1, 16)
    )
    return min(branches)


@lru_cache(maxsize=1)
def _floor_tables():
    P0 = special_point_min()
    phi_tables = []
    coordinate_tables = []
    lows = []
    for Cmask, P in enumerate(DENOMINATORS):
        low = -2 * P
        high = 2 * P
        lows.append(low)
        phi_row = []
        coordinate_row = []
        for numerator in range(low, high + 1):
            phi = _phi_exact(Cmask, numerator)
            phi_row.append((phi.numerator * Q) // phi.denominator)
            coordinate = P0 + Fraction(numerator, P)
            coordinate_row.append(
                (coordinate.numerator * Q) // coordinate.denominator
            )
        phi_tables.append(tuple(phi_row))
        coordinate_tables.append(tuple(coordinate_row))

    P = DENOMINATORS[15]
    low = lows[15]
    rho15 = tuple(
        (Fraction(numerator, P).numerator * Q)
        // Fraction(numerator, P).denominator
        for numerator in range(low, 2 * P + 1)
    )
    return tuple(phi_tables), tuple(coordinate_tables), tuple(lows), rho15


def _lookup(row, low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped exact lookup-table range")
    return row[idx]


@lru_cache(maxsize=1)
def pointwise_goodness_certificate() -> dict:
    """Exact integer lower-bound check on all 8,000,000 reduced states."""
    assert special_point_min() == EXPECTED_SPECIAL_POINT_MIN
    assert Q % COEFFICIENT_DEN == 0
    scale = Q // COEFFICIENT_DEN
    phi, coordinate, lows, rho15 = _floor_tables()
    unselected_states = tuple(product((1, 5), repeat=9))

    best = None
    best_state = None
    checked = 0

    for z1, z2, z3, z4, z12, z13 in product(range(1, 6), repeat=6):
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
                full_lower += _lookup(
                    phi[Cmask], lows[Cmask], nvals[Cmask]
                )
            full_lower += _lookup(rho15, lows[15], n1234)

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

    assert checked == 8_000_000
    assert best == EXPECTED_FLOOR_MIN
    assert best_state == EXPECTED_ARGMIN
    assert C * Q == 300_000_000_000
    assert best - C * Q == EXPECTED_FLOOR_SLACK > 0

    exact_at_argmin = _reduced_goodness_exact(EXPECTED_ARGMIN) + _factorial_penalty(EXPECTED_ARGMIN)
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
    return 40 * sum(ALPHA, Fraction(0)) + 18 * sum(BETA, Fraction(0))


@lru_cache(maxsize=1)
def seed_certificate() -> dict:
    pointwise = pointwise_goodness_certificate()
    assert special_global_cost() == EXPECTED_SPECIAL_GLOBAL_COST
    assert factorial_global_cost() == EXPECTED_FACTORIAL_COST
    margin = 41 * C - special_global_cost() - factorial_global_cost()
    assert margin == EXPECTED_GLOBAL_MARGIN > 0
    return {
        "N": N,
        "pointwise": pointwise,
        "special_point_min": special_point_min(),
        "special_global_cost": special_global_cost(),
        "factorial_cost": factorial_global_cost(),
        "summed_goodness_margin": margin,
        "noncovering_certified": True,
    }


__all__ = [
    "ALPHA",
    "BETA",
    "C",
    "EXPECTED_GLOBAL_MARGIN",
    "N",
    "SELECTED_SUPPORTS",
    "factorial_global_cost",
    "pointwise_goodness_certificate",
    "seed_certificate",
    "special_global_cost",
    "special_point_min",
]
