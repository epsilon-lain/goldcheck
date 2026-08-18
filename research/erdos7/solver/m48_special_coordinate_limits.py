"""M48: exact special-coordinate limit certificates used to close P53.

Three earlier finite certificates become stronger when the repeated
post-stage coordinate is inflated all the way to its geometric-series limit.
Using a limit baseline is legitimate: for every finite exponent the grouped
charges may be multiplied by b_limit/b_actual, producing valid (looser) upper
probability bounds with exactly the reference moment budgets.

The three exact reference limits are:

1. a=3, distinguished prime 5 at x_5=infinity=1/4, J=(7,11,13,17), using the
   M40 factorial penalties.  This covers every finite power of 5 in that
   staged geometry.
2. a=5, distinguished prime 5 at x_5=infinity=1/4, J=(7,11,13,17), using the
   M44 goodness/factorial penalties.
3. a=5, distinguished prime 7 at x_7=infinity=1/6, J=(5,11,13,17), using the
   M36 goodness/factorial penalties.

All three pointwise minima are verified by exhaustive integer lower-bound loops
whose lookup tables are built from exact Fractions and rounded downward.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m28_moment_hierarchy import moment_constant, selected_fibre_count
from m30_centered_moments import factorial_spike_cap
from m40_p322_exceptional_lifts import ALPHA_NUM as M40_ALPHA_NUM, BETA_NUM as M40_BETA_NUM
from m44_p62_profile_closure import (
    SELECTED_ALPHA_NUM as M44_SELECTED_ALPHA_NUM,
    SELECTED_BETA_NUM as M44_SELECTED_BETA_NUM,
    UNSELECTED_ALPHA_NUM as M44_UNSELECTED_ALPHA_NUM,
)
from m36_a5_exceptional_goodness import COEFFICIENT_NUMERATORS as M36_COEFFICIENTS

Q = 10**12
SELECTED_MASKS = (1, 2, 4, 8, 3, 5)
UNSELECTED_MASKS = (6, 7, 9, 10, 11, 12, 13, 14, 15)

A3_C = Fraction(3219, 10000)
A3_EXPECTED_FLOOR_MIN = 321_972_889_801
A3_EXPECTED_ARGMIN = (1, 1, 1, 1, 1, 4, 4, 1, 4, 4, 4, 4, 4, 4, 4)
A3_EXPECTED_EXACT_ARGMIN = Fraction(
    2237914997425511686938229122037,
    6950631771340631703208880000000,
)
A3_EXPECTED_SPECIAL_COST = Fraction(208149232581, 66189323200)
A3_EXPECTED_PENALTY_COST = Fraction(1021923, 1000000)
A3_EXPECTED_ETA = Fraction(7030993631127, 20684163500000)
A3_EXPECTED_CLIQUE_MIN = Fraction(941, 17017)

A5_FIVE_C = Fraction(32999, 100000)
A5_FIVE_EXPECTED_FLOOR_MIN = 330_004_947_384
A5_FIVE_EXPECTED_ARGMIN = (1,) * 15
A5_FIVE_EXPECTED_EXACT_ARGMIN = Fraction(
    3204402373366585023349981183247200703,
    9710164646566517961385166328720000000,
)
A5_FIVE_EXPECTED_SPECIAL_COST = Fraction(67908929447201, 2316626312000)
A5_FIVE_EXPECTED_PENALTY_COST = Fraction(2411069, 250000)
A5_FIVE_EXPECTED_ETA = Fraction(376679506003531, 289578289000000)

A5_SEVEN_C = Fraction(2929, 10000)
A5_SEVEN_EXPECTED_FLOOR_MIN = 293_118_223_450
A5_SEVEN_EXPECTED_ARGMIN = (3, 1, 3, 1, 3, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6)
A5_SEVEN_EXPECTED_EXACT_ARGMIN = Fraction(
    4197539859160637669,
    14320296464760000000,
)
A5_SEVEN_EXPECTED_SPECIAL_COST = Fraction(47402485392467, 2659392450000)
A5_SEVEN_EXPECTED_PENALTY_COST = Fraction(16178201, 1000000)
A5_SEVEN_EXPECTED_ETA = Fraction(92070538867211, 53187849000000)


def _denominators(J: tuple[int, int, int, int]) -> tuple[int, ...]:
    return tuple(
        prod(J[i] for i in range(4) if Cmask & (1 << i))
        for Cmask in range(16)
    )


def _rho_numerators(z: tuple[int, ...], J: tuple[int, int, int, int]) -> tuple[int, ...]:
    if len(z) != 15:
        raise ValueError("need fifteen normalized support values")
    (
        z1, z2, z12, z3, z13, z23, z123, z4, z14, z24, z124,
        z34, z134, z234, z1234,
    ) = z
    n1 = J[0] - z1
    n2 = J[1] - z2
    n3 = J[2] - z3
    n4 = J[3] - z4
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


def _special_point_min(special_limit: Fraction, J: tuple[int, int, int, int]) -> Fraction:
    den = _denominators(J)
    return sum(
        LAMBDA.get(1 | (T << 1), Fraction(0)) * (special_limit / den[T])
        + DIAGONAL[1 | (T << 1)] * (special_limit / den[T]) ** 2
        for T in range(16)
    )


def _phi_exact(
    special_limit: Fraction,
    J: tuple[int, int, int, int],
    levels: int,
    Cmask: int,
    numerator: int,
) -> Fraction:
    den = _denominators(J)
    rho = Fraction(numerator, den[Cmask])
    T = 15 ^ Cmask
    mask = 1 | (T << 1)
    lam = LAMBDA.get(mask, Fraction(0))
    nu = DIAGONAL[mask]
    lo = special_limit / den[T]
    hi = levels * lo
    x = -(lam - rho) / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + (lam - rho) * x


def _bounds(J: tuple[int, int, int, int], levels: int):
    lows = [None] * 16
    highs = [None] * 16
    for endpoint in product((1, levels), repeat=15):
        n = _rho_numerators(endpoint, J)
        for Cmask, value in enumerate(n):
            lows[Cmask] = value if lows[Cmask] is None or value < lows[Cmask] else lows[Cmask]
            highs[Cmask] = value if highs[Cmask] is None or value > highs[Cmask] else highs[Cmask]
    return tuple(lows), tuple(highs)


def _floor_tables(special_limit, J, levels, goodness):
    den = _denominators(J)
    P0 = _special_point_min(special_limit, J)
    lows, highs = _bounds(J, levels)
    phi = []
    coordinate = []
    rho = []
    for Cmask in range(16):
        prow = []
        crow = []
        rrow = []
        for numerator in range(lows[Cmask], highs[Cmask] + 1):
            value = _phi_exact(special_limit, J, levels, Cmask, numerator)
            prow.append((value.numerator * Q) // value.denominator)
            if goodness:
                value = P0 + Fraction(numerator, den[Cmask])
                crow.append((value.numerator * Q) // value.denominator)
            value = Fraction(numerator, den[Cmask])
            rrow.append((value.numerator * Q) // value.denominator)
        phi.append(tuple(prow))
        coordinate.append(tuple(crow))
        rho.append(tuple(rrow))
    return tuple(phi), tuple(coordinate), tuple(rho), lows


def _lookup(row: tuple[int, ...], low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped exact endpoint range")
    return row[idx]


def _penalty_exact(z, selected_alpha, selected_beta, unselected_alpha):
    out = Fraction(0)
    for mask, alpha, beta in zip(SELECTED_MASKS, selected_alpha, selected_beta):
        A = z[mask - 1] - 1
        out += alpha * A + beta * comb(A, 2)
    for mask, alpha in zip(UNSELECTED_MASKS, unselected_alpha):
        out += alpha * (z[mask - 1] - 1)
    return out


def _pointwise_exact(special_limit, J, levels, z, selected_alpha, selected_beta, unselected_alpha, goodness):
    den = _denominators(J)
    n = _rho_numerators(z, J)
    full = Fraction(n[15], den[15]) + sum(
        _phi_exact(special_limit, J, levels, Cmask, n[Cmask])
        for Cmask in range(16)
    )
    base = full
    if goodness:
        P0 = _special_point_min(special_limit, J)
        base = min([full] + [P0 + Fraction(n[Cmask], den[Cmask]) for Cmask in range(1, 16)])
    return base + _penalty_exact(z, selected_alpha, selected_beta, unselected_alpha)


def _enumerate(
    *, special_limit, J, levels, selected_alpha_num, selected_beta_num,
    unselected_alpha_num, C, goodness, expected_min, expected_argmin,
    expected_exact,
):
    assert Q % 1_000_000 == 0
    scale = Q // 1_000_000
    phi, coordinate, rho, lows = _floor_tables(special_limit, J, levels, goodness)
    unselected_states = tuple(product((1, levels), repeat=9))
    unselected_units = tuple(
        sum(a * (value - 1) for a, value in zip(unselected_alpha_num, state))
        for state in unselected_states
    )

    best = None
    best_state = None
    checked = 0
    d1, d2, d3, d4 = J
    for z1, z2, z3, z4, z12, z13 in product(range(1, levels + 1), repeat=6):
        n1 = d1 - z1
        n2 = d2 - z2
        n3 = d3 - z3
        n4 = d4 - z4
        n12 = n1 * n2 - z12
        n13 = n1 * n3 - z13
        selected = (z1, z2, z3, z4, z12, z13)
        selected_units = sum(
            a * (value - 1) + b * comb(value - 1, 2)
            for value, a, b in zip(selected, selected_alpha_num, selected_beta_num)
        )

        constant_phi = sum(
            _lookup(phi[Cmask], lows[Cmask], numerator)
            for Cmask, numerator in (
                (0, 1), (1, n1), (2, n2), (3, n12),
                (4, n3), (5, n13), (8, n4),
            )
        )

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
            penalty_scaled = scale * (selected_units + unselected_units[state_index])
            full_lower = penalty_scaled + constant_phi
            for Cmask in (6, 7, 9, 10, 11, 12, 13, 14, 15):
                full_lower += _lookup(phi[Cmask], lows[Cmask], nvals[Cmask])
            full_lower += _lookup(rho[15], lows[15], n1234)

            value = full_lower
            if goodness:
                for Cmask in range(1, 16):
                    branch = penalty_scaled + _lookup(coordinate[Cmask], lows[Cmask], nvals[Cmask])
                    if branch < value:
                        value = branch

            checked += 1
            if best is None or value < best:
                best = value
                best_state = (
                    z1, z2, z12, z3, z13, z23, z123, z4,
                    z14, z24, z124, z34, z134, z234, z1234,
                )

    assert checked == levels**6 * 2**9
    assert best == expected_min
    assert best_state == expected_argmin
    assert best - C * Q > 0
    selected_alpha = tuple(Fraction(x, 1_000_000) for x in selected_alpha_num)
    selected_beta = tuple(Fraction(x, 1_000_000) for x in selected_beta_num)
    unselected_alpha = tuple(Fraction(x, 1_000_000) for x in unselected_alpha_num)
    exact = _pointwise_exact(
        special_limit, J, levels, best_state,
        selected_alpha, selected_beta, unselected_alpha, goodness,
    )
    assert exact == expected_exact > C
    assert Fraction(best, Q) <= exact
    return {
        "state_count": checked,
        "floor_min_scaled": best,
        "floor_slack_scaled": best - C * Q,
        "argmin": best_state,
        "exact_argmin_value": exact,
        "verified": True,
    }


def _special_global_cost(special_limit, J, a):
    den = _denominators(J)
    return sum(
        moment_constant(a, 1) * LAMBDA.get(1 | (T << 1), Fraction(0)) * (special_limit / den[T])
        + moment_constant(a, 2) * DIAGONAL[1 | (T << 1)] * (special_limit / den[T]) ** 2
        for T in range(16)
    )


def _penalty_global_cost(a, selected_alpha_num, selected_beta_num, unselected_alpha_num):
    first = sum(selected_alpha_num) + sum(unselected_alpha_num)
    second = sum(selected_beta_num)
    return (
        factorial_spike_cap(a, 1) * Fraction(first, 1_000_000)
        + factorial_spike_cap(a, 2) * Fraction(second, 1_000_000)
    )


@lru_cache(maxsize=1)
def a3_five_limit_certificate() -> dict:
    J = (7, 11, 13, 17)
    out = _enumerate(
        special_limit=Fraction(1, 4), J=J, levels=4,
        selected_alpha_num=M40_ALPHA_NUM, selected_beta_num=M40_BETA_NUM,
        unselected_alpha_num=(0,) * 9, C=A3_C, goodness=False,
        expected_min=A3_EXPECTED_FLOOR_MIN, expected_argmin=A3_EXPECTED_ARGMIN,
        expected_exact=A3_EXPECTED_EXACT_ARGMIN,
    )
    # The complete non-special factor-4 box is in the Shearer region; this is
    # the M14 exact endpoint minimum.
    assert A3_EXPECTED_CLIQUE_MIN > 0
    special = _special_global_cost(Fraction(1, 4), J, 3)
    penalty = _penalty_global_cost(3, M40_ALPHA_NUM, M40_BETA_NUM, (0,) * 9)
    eta = 14 * A3_C - special - penalty
    assert special == A3_EXPECTED_SPECIAL_COST
    assert penalty == A3_EXPECTED_PENALTY_COST
    assert eta == A3_EXPECTED_ETA > 0
    out.update({"special_limit": Fraction(1,4), "summed_rho_margin": eta})
    return out


@lru_cache(maxsize=1)
def a5_five_limit_certificate() -> dict:
    J = (7, 11, 13, 17)
    out = _enumerate(
        special_limit=Fraction(1, 4), J=J, levels=6,
        selected_alpha_num=M44_SELECTED_ALPHA_NUM,
        selected_beta_num=M44_SELECTED_BETA_NUM,
        unselected_alpha_num=M44_UNSELECTED_ALPHA_NUM,
        C=A5_FIVE_C, goodness=True,
        expected_min=A5_FIVE_EXPECTED_FLOOR_MIN,
        expected_argmin=A5_FIVE_EXPECTED_ARGMIN,
        expected_exact=A5_FIVE_EXPECTED_EXACT_ARGMIN,
    )
    special = _special_global_cost(Fraction(1, 4), J, 5)
    penalty = _penalty_global_cost(
        5, M44_SELECTED_ALPHA_NUM, M44_SELECTED_BETA_NUM, M44_UNSELECTED_ALPHA_NUM
    )
    eta = 122 * A5_FIVE_C - special - penalty
    assert special == A5_FIVE_EXPECTED_SPECIAL_COST
    assert penalty == A5_FIVE_EXPECTED_PENALTY_COST
    assert eta == A5_FIVE_EXPECTED_ETA > 0
    out.update({"special_limit": Fraction(1,4), "summed_goodness_margin": eta})
    return out


@lru_cache(maxsize=1)
def a5_seven_limit_certificate() -> dict:
    J = (5, 11, 13, 17)
    selected_alpha_num = tuple(a for a, _ in M36_COEFFICIENTS)
    selected_beta_num = tuple(b for _, b in M36_COEFFICIENTS)
    out = _enumerate(
        special_limit=Fraction(1, 6), J=J, levels=6,
        selected_alpha_num=selected_alpha_num,
        selected_beta_num=selected_beta_num,
        unselected_alpha_num=(0,) * 9,
        C=A5_SEVEN_C, goodness=True,
        expected_min=A5_SEVEN_EXPECTED_FLOOR_MIN,
        expected_argmin=A5_SEVEN_EXPECTED_ARGMIN,
        expected_exact=A5_SEVEN_EXPECTED_EXACT_ARGMIN,
    )
    special = _special_global_cost(Fraction(1, 6), J, 5)
    penalty = _penalty_global_cost(5, selected_alpha_num, selected_beta_num, (0,) * 9)
    eta = 122 * A5_SEVEN_C - special - penalty
    assert special == A5_SEVEN_EXPECTED_SPECIAL_COST
    assert penalty == A5_SEVEN_EXPECTED_PENALTY_COST
    assert eta == A5_SEVEN_EXPECTED_ETA > 0
    out.update({"special_limit": Fraction(1,6), "summed_goodness_margin": eta})
    return out


def limit_audit() -> dict:
    a3 = a3_five_limit_certificate()
    a5five = a5_five_limit_certificate()
    a5seven = a5_seven_limit_certificate()
    return {
        "a3_five_limit": a3,
        "a5_five_limit": a5five,
        "a5_seven_limit": a5seven,
        "all_three_limits_positive": True,
        "verified": True,
    }


__all__ = [
    "A3_EXPECTED_ETA",
    "A5_FIVE_EXPECTED_ETA",
    "A5_SEVEN_EXPECTED_ETA",
    "a3_five_limit_certificate",
    "a5_five_limit_certificate",
    "a5_seven_limit_certificate",
    "limit_audit",
]
