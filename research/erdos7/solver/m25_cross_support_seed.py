"""M25: exact cross-support second-moment certificate for 172297125.

This closes the sole M24 survivor

    N = 3^4 * 5^3 * 7 * 11 * 13 * 17.

The pointwise certificate uses three kinds of nonnegative penalties:

* linear terms on all 31 nonempty square-free supports;
* diagonal quadratic terms q_S^2 for the 16 supports containing prime 5;
* cross terms q_S q_T for selected pairs of the 15 supports not containing 5.

M15 supplies the uniform a=4 first- and second-moment budgets

    sum_r q_S(r) <= 81 b_S,
    sum_r q_S(r) q_T(r) <= 197 b_S b_T.

After the five-containing variables are minimized independently as clipped
convex quadratics, the remaining function is separately concave in each of the
15 non-5 variables: the new cross terms are bilinear and hence affine in each
coordinate separately.  Therefore the global box minimum is attained at one
of the 2^15 non-5 corners and can be checked exactly with Fraction arithmetic.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction

from m14_clique_shearer import J_MASK, coordinate_rhos
from m15_second_moment import second_moment_constant

N = 3**4 * 5**3 * 7 * 11 * 13 * 17
PRIMES = (5, 7, 11, 13, 17)
BASE_COORDS = (
    Fraction(31, 125),
    Fraction(1, 7),
    Fraction(1, 11),
    Fraction(1, 13),
    Fraction(1, 17),
)
NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
FIVE_MASKS = tuple(1 | T for T in J_SUBSETS)

LAMBDA = {
    2: Fraction(13, 50),
    3: Fraction(3, 4),
    4: Fraction(81, 500),
    5: Fraction(247, 1000),
    6: Fraction(67, 500),
    7: Fraction(169, 200),
    8: Fraction(61, 500),
    9: Fraction(177, 1000),
    10: Fraction(111, 1000),
    11: Fraction(409, 500),
    12: Fraction(31, 1000),
    13: Fraction(347, 500),
    14: Fraction(47, 100),
    15: Fraction(937, 1000),
    16: Fraction(17, 200),
    17: Fraction(33, 500),
    18: Fraction(1, 8),
    19: Fraction(831, 1000),
    21: Fraction(173, 250),
    22: Fraction(109, 500),
    23: Fraction(461, 500),
    25: Fraction(87, 125),
    26: Fraction(201, 1000),
    27: Fraction(903, 1000),
    29: Fraction(213, 250),
    30: Fraction(663, 1000),
    31: Fraction(541, 500),
}

DIAGONAL = {
    1: Fraction(197, 500),
    3: Fraction(113, 1000),
    5: Fraction(428, 125),
    7: Fraction(951, 1000),
    9: Fraction(2233, 500),
    11: Fraction(947, 500),
    13: Fraction(10),
    15: Fraction(10),
    17: Fraction(6731, 1000),
    19: Fraction(221, 1000),
    21: Fraction(10),
    23: Fraction(10),
    25: Fraction(10),
    27: Fraction(10),
    29: Fraction(10),
    31: Fraction(10),
}

CROSS = {
    (2, 6): Fraction(77, 125),
    (2, 10): Fraction(31, 50),
    (2, 14): Fraction(277, 1000),
    (2, 18): Fraction(299, 500),
    (2, 22): Fraction(393, 1000),
    (2, 26): Fraction(407, 1000),
    (2, 30): Fraction(43, 500),
    (4, 6): Fraction(93, 250),
    (4, 8): Fraction(9, 250),
    (4, 12): Fraction(57, 100),
    (4, 14): Fraction(157, 1000),
    (4, 16): Fraction(63, 1000),
    (4, 20): Fraction(289, 500),
    (4, 22): Fraction(24, 125),
    (4, 28): Fraction(121, 200),
    (6, 20): Fraction(11, 25),
    (6, 22): Fraction(1839, 1000),
    (6, 30): Fraction(761, 1000),
    (8, 10): Fraction(93, 250),
    (8, 12): Fraction(573, 1000),
    (8, 14): Fraction(29, 200),
    (8, 16): Fraction(129, 1000),
    (8, 24): Fraction(23, 40),
    (8, 26): Fraction(123, 1000),
    (8, 28): Fraction(601, 1000),
    (10, 18): Fraction(127, 500),
    (10, 24): Fraction(201, 250),
    (10, 26): Fraction(2273, 1000),
    (12, 16): Fraction(21, 200),
    (12, 20): Fraction(263, 500),
    (12, 24): Fraction(169, 500),
    (12, 28): Fraction(493, 1000),
    (16, 18): Fraction(71, 250),
    (16, 20): Fraction(157, 250),
    (16, 22): Fraction(207, 1000),
    (16, 24): Fraction(559, 1000),
    (16, 26): Fraction(149, 1000),
    (16, 28): Fraction(833, 1000),
    (18, 20): Fraction(251, 1000),
    (18, 24): Fraction(263, 1000),
    (18, 26): Fraction(51, 500),
    (18, 28): Fraction(173, 500),
    (20, 22): Fraction(4509, 1000),
    (20, 24): Fraction(14, 25),
    (20, 28): Fraction(21, 40),
    (24, 26): Fraction(1347, 250),
}

EXPECTED_C = Fraction(
    8062944017330066479969,
    19768351476874000000000,
)
EXPECTED_MARGIN = Fraction(
    148743273991746196533,
    3953670295374800000000,
)
EXPECTED_PROPER_NON5_MIN = Fraction(1, 91)
EXPECTED_FULL_NON5_MIN = Fraction(-258, 17017)
EXPECTED_COMPLETION_MAX = Fraction(-3629, 425425)


def baseline(mask: int) -> Fraction:
    if not 1 <= mask < 32:
        raise ValueError("support mask must be in 1..31")
    value = Fraction(1)
    for i, x in enumerate(BASE_COORDS):
        if mask & (1 << i):
            value *= x
    return value


def _quadratic_minimum(
    linear: Fraction,
    quadratic: Fraction,
    lo: Fraction,
    hi: Fraction,
) -> tuple[Fraction, Fraction]:
    """Return the exact minimum value and minimizer of ax+b x^2 on [lo,hi]."""
    if quadratic < 0:
        raise ValueError("quadratic coefficient must be nonnegative")
    if quadratic == 0:
        x = hi if linear < 0 else lo
    else:
        x = -linear / (2 * quadratic)
        if x < lo:
            x = lo
        elif x > hi:
            x = hi
    return linear * x + quadratic * x * x, x


@lru_cache(maxsize=None)
def seed_certificate() -> dict:
    """Verify the complete M25 certificate with exact rational arithmetic."""
    assert second_moment_constant(4) == 197
    b = {m: baseline(m) for m in range(1, 32)}

    best: Fraction | None = None
    proper_non5_min: Fraction | None = None
    full_non5_min: Fraction | None = None
    completion_max: Fraction | None = None

    for bits in range(1 << len(NON5_MASKS)):
        q0 = {
            mask: b[mask] * (5 if bits & (1 << idx) else 1)
            for idx, mask in enumerate(NON5_MASKS)
        }
        rho = coordinate_rhos(q0, J_MASK)

        for Cmask, value in rho.items():
            if Cmask == J_MASK:
                if full_non5_min is None or value < full_non5_min:
                    full_non5_min = value
            elif proper_non5_min is None or value < proper_non5_min:
                proper_non5_min = value

        # If rho_J <= 0, q_5 <= 5*(31/125)=31/25 and all other
        # five-containing charges are at least their baselines.  This is the
        # M16 completion audit with the new 5^3 baseline.
        alpha = 5 * b[1] - 1
        completion = -alpha * rho[J_MASK]
        completion -= sum(
            b[1 | T] * rho[J_MASK ^ T]
            for T in J_SUBSETS
            if T != 0
        )
        if completion_max is None or completion > completion_max:
            completion_max = completion

        value = rho[J_MASK]
        value += sum(LAMBDA.get(m, Fraction(0)) * q0[m] for m in NON5_MASKS)
        value += sum(
            mu * q0[s] * q0[t]
            for (s, t), mu in CROSS.items()
        )

        # Once q^0 is fixed, the 16 five-containing variables are independent
        # clipped convex quadratics because CROSS contains only non-5 pairs.
        for T in J_SUBSETS:
            mask = 1 | T
            linear = LAMBDA.get(mask, Fraction(0)) - rho[J_MASK ^ T]
            quadratic = DIAGONAL[mask]
            contribution, _ = _quadratic_minimum(
                linear,
                quadratic,
                b[mask],
                5 * b[mask],
            )
            value += contribution

        if best is None or value < best:
            best = value

    assert best is not None
    assert proper_non5_min is not None
    assert full_non5_min is not None
    assert completion_max is not None

    linear_cost = 81 * sum(
        LAMBDA.get(m, Fraction(0)) * b[m]
        for m in range(1, 32)
    )
    diagonal_cost = 197 * sum(
        DIAGONAL[m] * b[m] * b[m]
        for m in FIVE_MASKS
    )
    cross_cost = 197 * sum(
        mu * b[s] * b[t]
        for (s, t), mu in CROSS.items()
    )
    margin = 41 * best - linear_cost - diagonal_cost - cross_cost

    assert best == EXPECTED_C
    assert margin == EXPECTED_MARGIN
    assert proper_non5_min == EXPECTED_PROPER_NON5_MIN
    assert full_non5_min == EXPECTED_FULL_NON5_MIN
    assert completion_max == EXPECTED_COMPLETION_MAX
    assert proper_non5_min > 0
    assert completion_max < 0
    assert margin > 0

    return {
        "N": N,
        "C": best,
        "summed_margin": margin,
        "proper_non5_min": proper_non5_min,
        "full_non5_min": full_non5_min,
        "completion_upper_max": completion_max,
        "cross_term_count": len(CROSS),
        "diagonal_term_count": len(DIAGONAL),
        "noncovering_certified": True,
    }


__all__ = [
    "BASE_COORDS",
    "CROSS",
    "DIAGONAL",
    "EXPECTED_C",
    "EXPECTED_MARGIN",
    "LAMBDA",
    "N",
    "baseline",
    "seed_certificate",
]
