"""M29: exact dual obstruction for the fixed-five all-orders M28 certificate cone.

Target:
    N = 3^4 * 5^4 * 7 * 11 * 13 * 17.

This does NOT show N is covering or noncovering.  It proves an exact method-level
no-go for the following certificate class.

Keep the M25 linear coefficients and diagonal q_S^2 coefficients on the
16 supports containing prime 5.  On the 15 supports not containing 5, allow
an arbitrary nonnegative multilinear penalty

    sum_A c_A prod_{S in A} q_S,

where A is any nonempty subset of the 15 non-5 supports (so every order
1,...,15 is allowed and no support variable repeats inside a monomial).
Charge each such monomial using the exact M28 moment budget H(4,|A|).

M29 gives a rational dual distribution on 103 of the 2^15 non-5 box corners.
It has total mass 41, satisfies every one of the 2^15-1 normalized moment
constraints, and makes the best possible summed-margin upper bound strictly
negative.  Therefore no certificate in this precisely defined cone can prove
noncoverage of the target.
"""
from __future__ import annotations

from fractions import Fraction

from m14_clique_shearer import J_MASK, coordinate_rhos
from m25_cross_support_seed import DIAGONAL, LAMBDA
from m28_moment_hierarchy import moment_constant

N = 3**4 * 5**4 * 7 * 11 * 13 * 17
DEN = 100_000
BASE_COORDS = (
    Fraction(156, 625),
    Fraction(1, 7),
    Fraction(1, 11),
    Fraction(1, 13),
    Fraction(1, 17),
)
NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
FIVE_MASKS = tuple(1 | T for T in J_SUBSETS)

DUAL_WEIGHTS = {
    0: 1575050,
    10: 74272,
    85: 32662,
    166: 32987,
    168: 4484,
    184: 26079,
    341: 16309,
    440: 8204,
    522: 9954,
    549: 14388,
    586: 42432,
    648: 38060,
    904: 14493,
    1301: 54481,
    1361: 89312,
    2058: 22381,
    2122: 26043,
    2154: 3322,
    2161: 4740,
    2178: 50380,
    2456: 6353,
    2690: 8369,
    3185: 39245,
    3202: 37118,
    3714: 16528,
    3746: 20708,
    3905: 8455,
    4181: 65074,
    4421: 50953,
    4645: 22338,
    4705: 2706,
    4744: 7540,
    4776: 7020,
    5000: 8362,
    5141: 40192,
    5201: 17148,
    5665: 4106,
    6118: 18239,
    6328: 18217,
    6753: 22121,
    6824: 15557,
    7048: 37586,
    8202: 53391,
    8358: 12882,
    8632: 4116,
    9382: 53285,
    10648: 58208,
    11370: 7316,
    11894: 49999,
    11906: 16781,
    11938: 113,
    12097: 13376,
    12472: 22144,
    12728: 30158,
    13192: 6288,
    13208: 10547,
    14278: 11203,
    14520: 30513,
    14744: 8015,
    15228: 50000,
    15240: 10606,
    15256: 9726,
    15937: 27383,
    16510: 13312,
    16513: 49999,
    16645: 32550,
    16661: 26525,
    17002: 5601,
    17502: 421,
    17685: 10325,
    18406: 25762,
    18545: 429,
    19265: 51660,
    19505: 23514,
    19578: 27664,
    20501: 44960,
    20741: 64236,
    21102: 27664,
    21585: 10076,
    21598: 24318,
    22049: 46256,
    22502: 17294,
    22968: 21004,
    23361: 11566,
    23585: 17382,
    23992: 14424,
    24670: 28773,
    25194: 28068,
    25254: 55380,
    25694: 5509,
    25766: 846,
    26502: 59618,
    26721: 11775,
    26730: 24708,
    27754: 26062,
    28417: 45245,
    29290: 5072,
    30241: 17892,
    30314: 18706,
    31640: 21710,
    31777: 10601,
    32184: 35575,
    32710: 37500,
}

EXPECTED_FIXED_COST = Fraction(807151395889143, 83666064453125)
EXPECTED_DUAL_GAP = Fraction(
    -3441114552627898016887069582655901956931361,
    86697898630058196083796127935000000000000000,
)


def baseline(mask: int) -> Fraction:
    if not 1 <= mask < 32:
        raise ValueError("support mask must be in 1..31")
    out = Fraction(1)
    for i, x in enumerate(BASE_COORDS):
        if mask & (1 << i):
            out *= x
    return out


def _quadratic_minimum(
    linear: Fraction,
    quadratic: Fraction,
    lo: Fraction,
    hi: Fraction,
) -> Fraction:
    if quadratic <= 0:
        raise ValueError("M29 keeps the positive M25 five-support diagonals")
    x = -linear / (2 * quadratic)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return linear * x + quadratic * x * x


def corner_base(corner: int) -> Fraction:
    """Exact pointwise base after minimizing all five-containing variables."""
    if not 0 <= corner < (1 << len(NON5_MASKS)):
        raise ValueError("corner must be a 15-bit mask")
    q0 = {
        mask: baseline(mask) * (5 if corner & (1 << idx) else 1)
        for idx, mask in enumerate(NON5_MASKS)
    }
    rho = coordinate_rhos(q0, J_MASK)
    value = rho[J_MASK]
    for T in J_SUBSETS:
        mask = 1 | T
        linear = LAMBDA.get(mask, Fraction(0)) - rho[J_MASK ^ T]
        value += _quadratic_minimum(
            linear,
            DIAGONAL[mask],
            baseline(mask),
            5 * baseline(mask),
        )
    return value


def fixed_five_cost() -> Fraction:
    """Global M28 charge of the frozen five-containing M25 terms."""
    linear = 81 * sum(
        LAMBDA.get(mask, Fraction(0)) * baseline(mask)
        for mask in FIVE_MASKS
    )
    diagonal = 197 * sum(
        DIAGONAL[mask] * baseline(mask) ** 2
        for mask in FIVE_MASKS
    )
    return linear + diagonal


def normalized_moment_numerator(monomial: int) -> int:
    """Return DEN * sum alpha_z prod_{i in A} z_i for a 15-bit A.

    At a non-5 box corner z_i is 1 or 5.  DUAL_WEIGHTS stores DEN*alpha_z.
    """
    if not 1 <= monomial < (1 << len(NON5_MASKS)):
        raise ValueError("monomial must be a nonempty 15-bit mask")
    return sum(
        weight * 5 ** ((corner & monomial).bit_count())
        for corner, weight in DUAL_WEIGHTS.items()
    )


def dual_audit() -> dict:
    assert len(DUAL_WEIGHTS) == 103
    assert sum(DUAL_WEIGHTS.values()) == 41 * DEN
    assert fixed_five_cost() == EXPECTED_FIXED_COST

    tightest_slack = None
    tightest_mask = None
    for monomial in range(1, 1 << len(NON5_MASKS)):
        order = monomial.bit_count()
        cap = DEN * moment_constant(4, order)
        used = normalized_moment_numerator(monomial)
        slack = cap - used
        assert slack >= 0
        if tightest_slack is None or slack < tightest_slack:
            tightest_slack = slack
            tightest_mask = monomial

    weighted_base = sum(
        Fraction(weight, DEN) * corner_base(corner)
        for corner, weight in DUAL_WEIGHTS.items()
    )
    gap = weighted_base - fixed_five_cost()
    assert gap == EXPECTED_DUAL_GAP
    assert gap < 0
    assert tightest_slack == 60
    assert tightest_mask == 4

    return {
        "N": N,
        "dual_support_size": len(DUAL_WEIGHTS),
        "total_mass": Fraction(sum(DUAL_WEIGHTS.values()), DEN),
        "tightest_moment_slack_numerator": tightest_slack,
        "tightest_moment_mask": tightest_mask,
        "fixed_five_cost": fixed_five_cost(),
        "dual_gap": gap,
        "all_orders_checked": 15,
        "method_class_excluded": True,
    }


__all__ = [
    "BASE_COORDS",
    "DEN",
    "DUAL_WEIGHTS",
    "EXPECTED_DUAL_GAP",
    "N",
    "baseline",
    "corner_base",
    "dual_audit",
    "fixed_five_cost",
    "normalized_moment_numerator",
]
