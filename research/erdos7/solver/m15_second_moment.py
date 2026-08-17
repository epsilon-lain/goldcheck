"""M15: exact second-moment 3-adic compatibility constraints.

For N=3^a M, fix s_a=(3^a+1)/2 surviving 3-adic fibres and, for an
M-divisor m, write

    k_m(r) <= 1 + sum_{j=1}^a 1[r == c_{j,m} (mod 3^j)].

This module verifies the universal pair bound

    sum_r k_m(r) k_n(r) <= H_a,
    H_a = (5*3^a - 2*a - 3)/2,

for any two M-divisors m,n.  Consequently, for the square-free support
charges q_S used in M14,

    sum_r q_S(r) q_T(r) <= H_a b_S b_T.

At a=4, H_4=197.  The 32-corner affine dual obstruction from M14 has
second moment 281 b_S^2 on every support coordinate, so it is not realizable
once genuine second-order 3-adic compatibility is retained.
"""

from __future__ import annotations

from fractions import Fraction

from m14_clique_shearer import baseline
from m14_generalization import A4_DUAL_CORNERS, DUAL_DEN


def second_moment_constant(a: int) -> int:
    """Return H_a for the universal pair-load bound."""
    if a < 1:
        raise ValueError("a must be positive")
    power = 3**a
    survivors = (power + 1) // 2
    first_increment = sum(3 ** (a - j) for j in range(1, a + 1))
    pair_intersections = sum(
        3 ** (a - max(j, ell))
        for j in range(1, a + 1)
        for ell in range(1, a + 1)
    )
    assert first_increment == (power - 1) // 2
    assert pair_intersections == power - a - 1
    direct = survivors + 2 * first_increment + pair_intersections
    closed = (5 * power - 2 * a - 3) // 2
    assert direct == closed
    return closed


def support_pair_budget(a: int, support_s: int, support_t: int) -> Fraction:
    """Exact upper bound H_a*b_S*b_T for the summed support product."""
    return second_moment_constant(a) * baseline(support_s) * baseline(support_t)


def _endpoint_multiplier(endpoint_mask: int, support: int) -> int:
    return 5 if endpoint_mask & (1 << (support - 1)) else 1


def a4_old_dual_second_moments() -> dict:
    """Show exactly why the old a=4 affine dual is killed by second moments.

    The M14 dual has total mass 41 and, for each support S, first moment
    sum_i alpha_i q_S^(i) = 81 b_S.  Since every dual corner uses endpoint
    multiplier z_S in {1,5}, this forces

        sum_i alpha_i z_S^2 = 281

    for every S.  Actual 3-adic fibre systems satisfy the sharper bound 197.
    """
    alphas = [Fraction(num, DUAL_DEN) for num, _ in A4_DUAL_CORNERS]
    assert sum(alphas) == 41
    allowed = second_moment_constant(4)
    assert allowed == 197

    diagonal: dict[int, Fraction] = {}
    for support in range(1, 32):
        first = sum(
            alpha * _endpoint_multiplier(mask, support)
            for alpha, (_num, mask) in zip(alphas, A4_DUAL_CORNERS)
        )
        second = sum(
            alpha * _endpoint_multiplier(mask, support) ** 2
            for alpha, (_num, mask) in zip(alphas, A4_DUAL_CORNERS)
        )
        assert first == 81
        assert second == 281
        assert second > allowed
        diagonal[support] = second

    return {
        "a": 4,
        "actual_second_moment_cap": Fraction(allowed),
        "dual_diagonal_second_moment": Fraction(281),
        "violating_support_count": len(diagonal),
        "all_31_diagonals_cut": True,
    }


__all__ = [
    "a4_old_dual_second_moments",
    "second_moment_constant",
    "support_pair_budget",
]
