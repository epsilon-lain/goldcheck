"""Milestone 14 generalization: exact 3-adic budgets and an a=4 affine no-go.

This module does two things independently of numerical optimization:

1. It verifies the parameterized fibre budget for N=3^a M:
       s_a = (3^a+1)/2 surviving pure-3 fibres,
       sum_r q_S(r) <= 3^a b_S,
       b_S <= q_S(r) <= (a+1)b_S.

2. For the next same-support frontier
       34459425 = 3^4 * 5^2 * 7 * 11 * 13 * 17,
   it verifies an exact dual certificate showing that *no* affine certificate

       rho(q) >= C - sum_S lambda_S q_S,   lambda_S >= 0,

   valid on the full box b_S <= q_S <= 5 b_S can yield a positive summed
   41-fibre / 81-budget margin.

The dual certificate is a nonnegative rational combination of 32 box corners.
No floating-point optimizer is used by the verifier.
"""

from __future__ import annotations

from fractions import Fraction

from m14_clique_shearer import J_MASK, LAMBDA, baseline, coordinate_rhos


DUAL_DEN = 227239

# Each pair is (numerator of alpha_i over DUAL_DEN, 31-bit endpoint mask).
# Bit (S-1) set means q_S = 5 b_S; otherwise q_S = b_S.
A4_DUAL_CORNERS = (
    (1096083, 0x20222),
    (117439, 0x50151415),
    (109800, 0x5450445),
    (204835, 0x5114115),
    (85276, 0x50401501),
    (85276, 0x6A003980),
    (185416, 0x10402828),
    (681175, 0x55541),
    (27035, 0xB802F80),
    (615378, 0x10555),
    (148075, 0x66246202),
    (41823, 0x20307818),
    (97914, 0x58780018),
    (839009, 0x18381808),
    (261781, 0x1551511),
    (333617, 0x2426206),
    (62799, 0x23800180),
    (98708, 0x68082838),
    (66526, 0x282048),
    (196706, 0x40150105),
    (1039172, 0x4F808080),
    (52129, 0x5803B80),
    (370920, 0x30182858),
    (463592, 0x686838),
    (108482, 0x60481868),
    (295342, 0x60260606),
    (576416, 0x36808080),
    (320109, 0x20666266),
    (85276, 0x29CB8000),
    (79164, 0x20406406),
    (141963, 0x45E8000),
    (429563, 0x1808080),
)


def three_adic_budget(a: int) -> dict[str, int]:
    """Exact pure-3 fibre parameters for exponent a>=1."""
    if a < 1:
        raise ValueError("a must be positive")
    power = 3**a
    survivors = (power + 1) // 2
    pure_covered_max = (power - 1) // 2
    assert survivors + pure_covered_max == power
    return {
        "a": a,
        "power": power,
        "surviving_fibres": survivors,
        "cross_fibre_budget": power,
        "pointwise_multiplier": a + 1,
    }


def a4_same_weights_box_minimum() -> Fraction:
    """Exact min of rho+lambda.q on [b,5b] for the old M14 lambdas."""
    non5 = [m for m in range(1, 32) if not (m & 1)]
    best: Fraction | None = None

    for bits in range(1 << len(non5)):
        q0: dict[int, Fraction] = {}
        for idx, mask in enumerate(non5):
            q0[mask] = baseline(mask) * (5 if bits & (1 << idx) else 1)

        rho = coordinate_rhos(q0, J_MASK)
        value = rho[J_MASK]
        value += sum(LAMBDA[m] * q0[m] for m in non5)

        for T in range(32):
            if T & ~J_MASK:
                continue
            mask = 1 | T
            coeff = LAMBDA[mask] - rho[J_MASK ^ T]
            q5 = baseline(mask) * (5 if coeff < 0 else 1)
            value += coeff * q5

        if best is None or value < best:
            best = value

    assert best is not None
    return best


def _corner(endpoint_mask: int) -> tuple[dict[int, Fraction], Fraction]:
    q = {
        S: baseline(S) * (5 if endpoint_mask & (1 << (S - 1)) else 1)
        for S in range(1, 32)
    }
    rho = coordinate_rhos(q, 31)[31]
    return q, rho


def a4_affine_dual_certificate() -> dict:
    """Verify the exact dual obstruction for the a=4 affine certificate class.

    Suppose lambda_S >= 0 and C obey

        C <= rho(q) + sum lambda_S q_S

    for every corner q of [b,5b].  Multiplying the 32 selected corner
    inequalities below by alpha_i and summing gives

        41 C <= sum alpha_i rho(q_i)
                 + sum_S lambda_S * 81 b_S.

    Therefore

        41 C - 81 sum_S lambda_S b_S
            <= sum alpha_i rho(q_i)
            = -316412/425425 < 0.

    Hence no affine certificate in this class can prove the a=4 frontier via
    the coarse 41-fibre / 81-budget support box alone.
    """
    alphas = [Fraction(num, DUAL_DEN) for num, _ in A4_DUAL_CORNERS]
    corners = [_corner(mask) for _, mask in A4_DUAL_CORNERS]

    assert sum(alphas) == 41

    weighted_q: dict[int, Fraction] = {}
    for S in range(1, 32):
        weighted_q[S] = sum(
            alpha * q[S] for alpha, (q, _rho) in zip(alphas, corners)
        )
        assert weighted_q[S] == 81 * baseline(S)

    weighted_rho = sum(
        alpha * rho for alpha, (_q, rho) in zip(alphas, corners)
    )
    assert weighted_rho == Fraction(-316412, 425425)
    assert weighted_rho < 0

    return {
        "dual_corner_count": len(corners),
        "dual_weight_sum": sum(alphas),
        "all_support_budgets_exact": True,
        "weighted_rho": weighted_rho,
        "positive_affine_margin_impossible": True,
    }


def a4_generalization_audit() -> dict:
    params = three_adic_budget(4)
    assert params == {
        "a": 4,
        "power": 81,
        "surviving_fibres": 41,
        "cross_fibre_budget": 81,
        "pointwise_multiplier": 5,
    }

    old_C = a4_same_weights_box_minimum()
    assert old_C == Fraction(273899, 425425)

    lambda_b = sum(LAMBDA[S] * baseline(S) for S in range(1, 32))
    assert lambda_b == Fraction(144411, 425425)
    old_margin = 41 * old_C - 81 * lambda_b
    assert old_margin == Fraction(-3928, 3575)

    dual = a4_affine_dual_certificate()
    return {
        **params,
        "old_lambda_box_min": old_C,
        "old_lambda_margin": old_margin,
        **dual,
    }


__all__ = [
    "A4_DUAL_CORNERS",
    "DUAL_DEN",
    "a4_affine_dual_certificate",
    "a4_generalization_audit",
    "a4_same_weights_box_minimum",
    "three_adic_budget",
]
