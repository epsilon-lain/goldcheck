"""M32: exact repeated-support factorial certificate for 861485625.

Target
------
    N = 3^4 * 5^4 * 7 * 11 * 13 * 17.

M29/M31 prove that large distinct-variable moment cones are insufficient while
the prime-5 side is frozen.  M30 identifies the missing information: for a
non-5 support S there is exactly one exact divisor with square-free support S,
so

    z_S = q_S / b_S = 1 + A_S,       A_S in {0,1,2,3,4},

and across the 41 selected 3-adic fibres

    sum A_S <= 40,
    sum binom(A_S,2) <= 18.

M32 uses those repeated-support/factorial constraints on six supports:

    {7}, {11}, {13}, {17}, {7,11}, {7,13}.

For those six supports it adds

    alpha_S A_S + beta_S binom(A_S,2)

with nonnegative rational coefficients.  The remaining nine non-5 variables
have no new penalty, so the reduced pointwise function remains separately
concave in them and their minimum is at endpoints z=1 or 5.  The six penalized
variables are genuinely integral z in {1,2,3,4,5}.  Thus a complete pointwise
verification has only

    5^6 * 2^9 = 8,000,000

states.

The verifier is exact.  It does not trust floating point.  Each clipped
quadratic contribution from the frozen prime-5 side is evaluated as a Fraction
when a small lookup table is built, then rounded *down* after multiplication by
Q=10^12.  The exhaustive loop uses only Python integers.  Therefore its minimum
is a rigorous rational lower bound for the true pointwise minimum.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m29_all_orders_no_go import baseline, fixed_five_cost

N = 3**4 * 5**4 * 7 * 11 * 13 * 17
PRIMES = (7, 11, 13, 17)
DENOMINATORS = tuple(
    __import__("math").prod(PRIMES[i] for i in range(4) if C & (1 << i))
    for C in range(16)
)
J_ORIGINAL = 0b11110

# Selected normalized non-5 supports 1,2,4,8,3,5 correspond, in the original
# five-prime mask convention, to 2,4,8,16,6,10.
SELECTED_SUPPORTS = (2, 4, 8, 16, 6, 10)
COEFFICIENT_DEN = 1_000_000
# (alpha numerator, beta numerator) over COEFFICIENT_DEN, in SELECTED_SUPPORTS order.
COEFFICIENT_NUMERATORS = (
    (27687, 14172),
    (14737, 4884),
    (12743, 2484),
    (9775, 1333),
    (3191, 2315),
    (3924, 838),
)
ALPHA = tuple(Fraction(a, COEFFICIENT_DEN) for a, _ in COEFFICIENT_NUMERATORS)
BETA = tuple(Fraction(b, COEFFICIENT_DEN) for _, b in COEFFICIENT_NUMERATORS)

Q = 10**12
C = Fraction(79437, 250000)  # 0.317748 exactly
EXPECTED_FLOOR_MIN = 317_748_994_349
EXPECTED_FLOOR_SLACK = 994_349
EXPECTED_ARGMIN = (2, 2, 2, 5, 3, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5)
EXPECTED_EXACT_ARGMIN = Fraction(
    3274623664211662201315187,
    10305693243258381718750000,
)
EXPECTED_GLOBAL_MARGIN = Fraction(19827332308731, 669328515625000)
EXPECTED_PROPER_NON5_MIN = Fraction(1, 91)
EXPECTED_FULL_NON5_MIN = Fraction(-258, 17017)
EXPECTED_COMPLETION_MAX = Fraction(-1062, 125125)


def _phi_exact(Cmask: int, numerator: int) -> Fraction:
    """Frozen-five clipped quadratic for rho_C=numerator/P_C."""
    complement = 15 ^ Cmask
    original_T = complement << 1
    five_mask = 1 | original_T
    rho = Fraction(numerator, DENOMINATORS[Cmask])
    linear = LAMBDA.get(five_mask, Fraction(0)) - rho
    nu = DIAGONAL[five_mask]
    lo = baseline(five_mask)
    hi = 5 * lo
    x = -linear / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + linear * x


def _rho_numerators(z: tuple[int, ...]) -> tuple[int, ...]:
    """Exact integer numerators n_C=P_C*rho_C for the 15 non-5 charges.

    The z order is the normalized nonempty-subset order
      1,2,12,3,13,23,123,4,14,24,124,34,134,234,1234.
    """
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
    """Exact M32 penalty on the six selected support variables."""
    # Selected z values in coefficient order: z1,z2,z3,z4,z12,z13.
    selected = (z[0], z[1], z[3], z[7], z[2], z[4])
    out = Fraction(0)
    for value, alpha, beta in zip(selected, ALPHA, BETA):
        A = value - 1
        out += alpha * A + beta * comb(A, 2)
    return out


def _pointwise_exact(z: tuple[int, ...]) -> Fraction:
    """Exact B(z)+factorial penalty, used to audit the reported minimizer."""
    n = _rho_numerators(z)
    value = Fraction(n[15], DENOMINATORS[15])
    value += sum(_phi_exact(Cmask, n[Cmask]) for Cmask in range(16))
    return value + _factorial_penalty(z)


@lru_cache(maxsize=1)
def _floor_tables() -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...], tuple[int, ...]]:
    """Build rigorous Q-scaled lower lookup tables using Fraction arithmetic."""
    tables = []
    lows = []
    for Cmask, P in enumerate(DENOMINATORS):
        # The exhaustive loop below checks every generated numerator lands in
        # these deliberately generous ranges.  They are table-allocation bounds,
        # not assumptions in the mathematical proof.
        low = -2 * P
        high = 2 * P
        lows.append(low)
        row = []
        for numerator in range(low, high + 1):
            value = _phi_exact(Cmask, numerator)
            row.append((value.numerator * Q) // value.denominator)
        tables.append(tuple(row))

    P = DENOMINATORS[15]
    low = lows[15]
    rho15 = tuple(
        (Fraction(numerator, P).numerator * Q)
        // Fraction(numerator, P).denominator
        for numerator in range(low, 2 * P + 1)
    )
    return tuple(tables), tuple(lows), rho15


def _lookup(row: tuple[int, ...], low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped exact lookup-table range")
    return row[idx]


@lru_cache(maxsize=1)
def pointwise_floor_certificate() -> dict:
    """Exhaust all 8,000,000 reduced states using integer lower bounds only."""
    if Q % COEFFICIENT_DEN:
        raise AssertionError("Q must exactly absorb the coefficient denominator")
    scale = Q // COEFFICIENT_DEN
    tables, lows, rho15 = _floor_tables()
    unselected_states = tuple(product((1, 5), repeat=9))

    best = None
    best_state = None
    checked = 0

    # The six integral variables are z1,z2,z3,z4,z12,z13.
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
            constant += _lookup(tables[Cmask], lows[Cmask], numerator)

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

            value = constant
            for Cmask, numerator in (
                (6, n23), (7, n123), (9, n14), (10, n24),
                (11, n124), (12, n34), (13, n134), (14, n234),
                (15, n1234),
            ):
                value += _lookup(tables[Cmask], lows[Cmask], numerator)
            value += _lookup(rho15, lows[15], n1234)

            checked += 1
            if best is None or value < best:
                best = value
                best_state = (
                    z1, z2, z12, z3, z13, z23, z123, z4,
                    z14, z24, z124, z34, z134, z234, z1234,
                )

    assert checked == 5**6 * 2**9 == 8_000_000
    assert best == EXPECTED_FLOOR_MIN
    assert best_state == EXPECTED_ARGMIN
    assert C * Q == 317_748_000_000
    assert best - C * Q == EXPECTED_FLOOR_SLACK > 0

    exact_at_argmin = _pointwise_exact(EXPECTED_ARGMIN)
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


@lru_cache(maxsize=1)
def completion_audit() -> dict:
    """Exact M14/M25 factor-5 completion audit on the full non-5 box.

    All coordinate rho polynomials and the bad-branch completion expression are
    multi-affine, so extrema on [1,5]^15 occur at the 2^15 corners checked here.
    """
    proper_min = None
    full_min = None
    completion_max = None
    b5 = baseline(1)
    alpha = 5 * b5 - 1

    for z in product((1, 5), repeat=15):
        n = _rho_numerators(z)
        rho = tuple(Fraction(n[Cmask], DENOMINATORS[Cmask]) for Cmask in range(16))

        for Cmask in range(15):
            value = rho[Cmask]
            if proper_min is None or value < proper_min:
                proper_min = value
        if full_min is None or rho[15] < full_min:
            full_min = rho[15]

        completion = -alpha * rho[15]
        # T != 0 is equivalent to C=J\T being a proper subset of J.
        for Cmask in range(15):
            original_T = (15 ^ Cmask) << 1
            completion -= baseline(1 | original_T) * rho[Cmask]
        if completion_max is None or completion > completion_max:
            completion_max = completion

    assert proper_min == EXPECTED_PROPER_NON5_MIN > 0
    assert full_min == EXPECTED_FULL_NON5_MIN
    assert completion_max == EXPECTED_COMPLETION_MAX < 0
    return {
        "proper_non5_min": proper_min,
        "full_non5_min": full_min,
        "completion_upper_max": completion_max,
        "verified": True,
    }


def factorial_global_cost() -> Fraction:
    return 40 * sum(ALPHA, Fraction(0)) + 18 * sum(BETA, Fraction(0))


@lru_cache(maxsize=1)
def seed_certificate() -> dict:
    pointwise = pointwise_floor_certificate()
    completion = completion_audit()
    cost = factorial_global_cost()
    margin = 41 * C - fixed_five_cost() - cost
    assert margin == EXPECTED_GLOBAL_MARGIN > 0
    assert completion["completion_upper_max"] < 0
    return {
        "N": N,
        "pointwise": pointwise,
        "completion": completion,
        "factorial_cost": cost,
        "fixed_five_cost": fixed_five_cost(),
        "summed_margin": margin,
        "noncovering_certified": True,
    }


__all__ = [
    "ALPHA",
    "BETA",
    "C",
    "EXPECTED_GLOBAL_MARGIN",
    "N",
    "SELECTED_SUPPORTS",
    "completion_audit",
    "factorial_global_cost",
    "pointwise_floor_certificate",
    "seed_certificate",
]
