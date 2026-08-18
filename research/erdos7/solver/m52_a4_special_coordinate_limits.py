"""M52: exact a=4 special-coordinate limit certificates.

M48 sent the distinguished repeated prime to its infinite geometric-series
baseline at stages a=3 and a=5.  M52 fills the missing a=4 layer for the two
special primes needed in the two-repeated-coordinate campaign:

- special prime 5, x_5(infinity)=1/4, non-special J=(7,11,13,17);
- special prime 7, x_7(infinity)=1/6, non-special J=(5,11,13,17).

The first certificate reuses M44's stronger goodness penalties at five
activation levels.  The second reuses the M33 asymmetric-goodness factorial
penalties.  Both are exact 5^6*2^9=8,000,000-state verifications.
"""
from __future__ import annotations

from fractions import Fraction

from m44_p62_profile_closure import (
    SELECTED_ALPHA_NUM as M44_SELECTED_ALPHA_NUM,
    SELECTED_BETA_NUM as M44_SELECTED_BETA_NUM,
    UNSELECTED_ALPHA_NUM as M44_UNSELECTED_ALPHA_NUM,
)
from m48_special_coordinate_limits import (
    A5_FIVE_EXPECTED_EXACT_ARGMIN,
    _enumerate,
    _penalty_global_cost,
    _special_global_cost,
)

A4_FIVE_C = Fraction(32999, 100000)
A4_FIVE_EXPECTED_FLOOR_MIN = 330_004_947_384
A4_FIVE_EXPECTED_ARGMIN = (1,) * 15
A4_FIVE_EXPECTED_SPECIAL_COST = Fraction(22406709699637, 2316626312000)
A4_FIVE_EXPECTED_PENALTY_COST = Fraction(1575103, 500000)
A4_FIVE_EXPECTED_ETA = Fraction(204805547139351, 289578289000000)

M33_ALPHA_NUM = (54506, 15997, 13268, 10495, 8673, 6719)
M33_BETA_NUM = (31667, 4353, 2571, 1509, 1858, 3325)
A4_SEVEN_C = Fraction(3, 10)
A4_SEVEN_EXPECTED_FLOOR_MIN = 303_811_982_434
A4_SEVEN_EXPECTED_ARGMIN = (3, 1, 3, 1, 2, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5)
A4_SEVEN_EXPECTED_EXACT_ARGMIN = Fraction(
    811658073226246909231891,
    2671580188169160840000000,
)
A4_SEVEN_EXPECTED_SPECIAL_COST = Fraction(15683039995699, 2659392450000)
A4_SEVEN_EXPECTED_PENALTY_COST = Fraction(2600707, 500000)
A4_SEVEN_EXPECTED_ETA = Fraction(31948860183767, 26593924500000)


def a4_five_limit_certificate() -> dict:
    out = _enumerate(
        special_limit=Fraction(1, 4),
        J=(7, 11, 13, 17),
        levels=5,
        selected_alpha_num=M44_SELECTED_ALPHA_NUM,
        selected_beta_num=M44_SELECTED_BETA_NUM,
        unselected_alpha_num=M44_UNSELECTED_ALPHA_NUM,
        C=A4_FIVE_C,
        goodness=True,
        expected_min=A4_FIVE_EXPECTED_FLOOR_MIN,
        expected_argmin=A4_FIVE_EXPECTED_ARGMIN,
        expected_exact=A5_FIVE_EXPECTED_EXACT_ARGMIN,
    )
    special = _special_global_cost(Fraction(1, 4), (7, 11, 13, 17), 4)
    penalty = _penalty_global_cost(
        4,
        M44_SELECTED_ALPHA_NUM,
        M44_SELECTED_BETA_NUM,
        M44_UNSELECTED_ALPHA_NUM,
    )
    eta = 41 * A4_FIVE_C - special - penalty
    assert special == A4_FIVE_EXPECTED_SPECIAL_COST
    assert penalty == A4_FIVE_EXPECTED_PENALTY_COST
    assert eta == A4_FIVE_EXPECTED_ETA > 0
    out.update({
        "special_limit": Fraction(1, 4),
        "summed_goodness_margin": eta,
    })
    return out


def a4_seven_limit_certificate() -> dict:
    out = _enumerate(
        special_limit=Fraction(1, 6),
        J=(5, 11, 13, 17),
        levels=5,
        selected_alpha_num=M33_ALPHA_NUM,
        selected_beta_num=M33_BETA_NUM,
        unselected_alpha_num=(0,) * 9,
        C=A4_SEVEN_C,
        goodness=True,
        expected_min=A4_SEVEN_EXPECTED_FLOOR_MIN,
        expected_argmin=A4_SEVEN_EXPECTED_ARGMIN,
        expected_exact=A4_SEVEN_EXPECTED_EXACT_ARGMIN,
    )
    special = _special_global_cost(Fraction(1, 6), (5, 11, 13, 17), 4)
    penalty = _penalty_global_cost(4, M33_ALPHA_NUM, M33_BETA_NUM, (0,) * 9)
    eta = 41 * A4_SEVEN_C - special - penalty
    assert special == A4_SEVEN_EXPECTED_SPECIAL_COST
    assert penalty == A4_SEVEN_EXPECTED_PENALTY_COST
    assert eta == A4_SEVEN_EXPECTED_ETA > 0
    out.update({
        "special_limit": Fraction(1, 6),
        "summed_goodness_margin": eta,
    })
    return out


def limit_audit() -> dict:
    five = a4_five_limit_certificate()
    seven = a4_seven_limit_certificate()
    return {
        "a4_five_limit": five,
        "a4_seven_limit": seven,
        "both_limits_positive": True,
        "verified": True,
    }


__all__ = [
    "A4_FIVE_EXPECTED_ETA",
    "A4_SEVEN_EXPECTED_ETA",
    "a4_five_limit_certificate",
    "a4_seven_limit_certificate",
    "limit_audit",
]
