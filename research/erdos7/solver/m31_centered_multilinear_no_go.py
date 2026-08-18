"""M31: exact dual barrier for the full centered multilinear M30 cone.

Target:
    N = 3^4 * 5^4 * 7 * 11 * 13 * 17.

Keep the M29/M25 treatment of the sixteen supports containing prime 5 fixed.
On the fifteen non-5 supports, allow every nonnegative centered multilinear
penalty

    c_A * prod_{S in A} (q_S - b_S),

for every nonempty subset A of the fifteen support variables.  M30 charges an
order-t monomial by M(4,t)*prod b_S.

After normalizing y_S=(q_S-b_S)/b_S, a non-5 box corner has y_S in {0,4}.
The reduced pointwise function is separately concave because the frozen-five
base is separately concave and centered distinct-variable monomials are
multi-affine.  Hence box minima occur at corners.

The rational dual below has mass 41, satisfies all 2^15-1 centered moment
constraints, and gives a strictly negative summed-margin upper bound.  Thus the
entire centered distinct-variable multilinear cone is insufficient while the
five-containing side is frozen.

Importantly, the same dual violates every repeated centered square constraint:
for each non-5 variable its dual second centered moment is 160, while M30 gives
M(4,2)=76.  Repeated-support powers are therefore a genuine escape direction,
not part of this no-go theorem.
"""
from __future__ import annotations

from fractions import Fraction

from m29_all_orders_no_go import corner_base, fixed_five_cost
from m30_centered_moments import centered_moment_constant

N = 3**4 * 5**4 * 7 * 11 * 13 * 17
DEN = 5120

DUAL_WEIGHTS = {
    0: 80640, 81: 56, 85: 405, 168: 820, 325: 2569, 522: 1049,
    586: 733, 648: 2867, 674: 258, 678: 413, 1045: 1006, 1118: 916,
    1153: 1290, 1297: 1270, 1301: 1358, 1349: 150, 1361: 3718,
    1633: 722, 2058: 2030, 2154: 256, 2178: 4635, 2232: 93,
    2456: 573, 2625: 230, 2690: 1, 2952: 173, 3162: 96, 3169: 1025,
    3178: 35, 3185: 793, 3234: 178, 3746: 1533, 3905: 297, 3970: 709,
    4177: 429, 4181: 2801, 4421: 1115, 4705: 1288, 4718: 1229,
    4776: 93, 5141: 503, 5214: 604, 5381: 3549, 5669: 1264,
    5729: 207, 6328: 1647, 6824: 1520, 7048: 2387, 7064: 307,
    8202: 5474, 8358: 885, 8360: 220, 8376: 1520, 8866: 626,
    8870: 472, 9094: 48, 9096: 93, 9382: 1155, 10118: 67,
    10182: 1040, 10648: 3241, 11073: 707, 11377: 128, 11394: 707,
    11894: 2560, 12382: 211, 12728: 2560, 13192: 1427, 14520: 820,
    14744: 359, 15228: 2560, 16510: 1737, 16513: 1270,
    16661: 2864, 16721: 1910, 16906: 1047, 17002: 349,
    17957: 1463, 19546: 288, 19562: 1647, 19578: 916, 20130: 662,
    20354: 104, 20501: 3531, 20574: 743, 21029: 223, 21102: 291,
    21478: 1107, 22053: 307, 22438: 223, 22502: 1453,
    22625: 467, 22968: 307, 23448: 733, 23601: 896, 23649: 64,
    23992: 640, 24170: 754, 24518: 884, 24629: 1212, 25194: 822,
    25254: 1155, 25766: 2040, 26218: 766, 26502: 3142,
    26566: 223, 27457: 1147, 27738: 220, 27754: 419,
    28417: 1290, 28546: 187, 28766: 1309, 30662: 413,
    30753: 235, 30769: 1269, 30817: 426, 31233: 743,
    31297: 1290, 31553: 693, 31793: 171, 31850: 379,
    32248: 1920, 32257: 1166, 32577: 1683,
}

EXPECTED_FIXED_COST = Fraction(807151395889143, 83666064453125)
EXPECTED_WEIGHTED_BASE = Fraction(
    116636509250882496503565785210872183589527,
    12137705808208147451731457910900000000000,
)
EXPECTED_DUAL_GAP = Fraction(
    -459546958093873554501492643621474782569,
    12137705808208147451731457910900000000000,
)


def centered_monomial_numerator(mask: int) -> int:
    """DEN times the dual average of prod_{i in mask} y_i at box corners."""
    if not 1 <= mask < (1 << 15):
        raise ValueError("mask must be a nonempty 15-bit mask")
    order = mask.bit_count()
    return (4**order) * sum(
        weight
        for corner, weight in DUAL_WEIGHTS.items()
        if (corner & mask) == mask
    )


def repeated_square_moment(variable: int) -> Fraction:
    """Dual average of y_variable^2; deliberately outside the no-go cone."""
    if not 0 <= variable < 15:
        raise ValueError("variable must be in 0..14")
    used = 16 * sum(
        weight
        for corner, weight in DUAL_WEIGHTS.items()
        if corner & (1 << variable)
    )
    return Fraction(used, DEN)


def dual_audit() -> dict:
    assert len(DUAL_WEIGHTS) == 124
    assert sum(DUAL_WEIGHTS.values()) == 41 * DEN
    assert fixed_five_cost() == EXPECTED_FIXED_COST

    tightest_slack = None
    tightest_mask = None
    for mask in range(1, 1 << 15):
        order = mask.bit_count()
        cap = DEN * centered_moment_constant(4, order)
        used = centered_monomial_numerator(mask)
        slack = cap - used
        assert slack >= 0
        if tightest_slack is None or slack < tightest_slack:
            tightest_slack = slack
            tightest_mask = mask

    weighted_base = sum(
        Fraction(weight, DEN) * corner_base(corner)
        for corner, weight in DUAL_WEIGHTS.items()
    )
    gap = weighted_base - fixed_five_cost()

    assert weighted_base == EXPECTED_WEIGHTED_BASE
    assert gap == EXPECTED_DUAL_GAP < 0
    assert tightest_slack == 0
    assert tightest_mask == 1

    repeated = tuple(repeated_square_moment(i) for i in range(15))
    assert repeated == (Fraction(160),) * 15
    assert centered_moment_constant(4, 2) == 76
    assert all(value - 76 == 84 for value in repeated)

    return {
        "N": N,
        "dual_support_size": len(DUAL_WEIGHTS),
        "total_mass": Fraction(sum(DUAL_WEIGHTS.values()), DEN),
        "tightest_centered_slack": tightest_slack,
        "tightest_centered_mask": tightest_mask,
        "fixed_five_cost": fixed_five_cost(),
        "weighted_base": weighted_base,
        "dual_gap": gap,
        "repeated_square_dual_moment": repeated[0],
        "repeated_square_cap": Fraction(76),
        "repeated_square_violation": Fraction(84),
        "method_class_excluded": True,
    }


__all__ = [
    "DEN",
    "DUAL_WEIGHTS",
    "EXPECTED_DUAL_GAP",
    "N",
    "centered_monomial_numerator",
    "dual_audit",
    "repeated_square_moment",
]
