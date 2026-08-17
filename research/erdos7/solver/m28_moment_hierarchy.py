"""M28: exact all-orders 3-adic moment hierarchy.

For N=3^a M, after selecting s_a=(3^a+1)/2 surviving 3-adic fibres,
write for each exact M-divisor m

    k_m(r) <= 1 + sum_{j=1}^a 1[r == c_{j,m} (mod 3^j)].

M15 used the t=2 case.  This module records the full hierarchy: for any
t >= 1 and any exact M-divisors m_1,...,m_t,

    sum_r prod_h k_{m_h}(r) <= H(a,t),

where

    H(a,t) = s_a + sum_{u=1}^t binom(t,u) M(a,u),
    M(a,u) = sum_{j=1}^a (j^u-(j-1)^u) 3^(a-j).

The same bound survives grouping by square-free support.  If q_S(r) is the
M14 support charge and b_S=sum_{sqf(m)=S}1/m, then for arbitrary (possibly
repeated) supports S_1,...,S_t,

    sum_r prod_h q_{S_h}(r) <= H(a,t) prod_h b_{S_h}.

At a=4 the first five constants are 81,197,573,1925,7221.  Thus M15 is
exactly the t=2 member, while M28 supplies the third and higher moment budgets
needed beyond the M25 second-order certificates.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb


def selected_fibre_count(a: int) -> int:
    if a < 1:
        raise ValueError("a must be positive")
    return (3**a + 1) // 2


def intersection_level_sum(a: int, u: int) -> int:
    """Sum of the universal u-indicator intersection capacities.

    For u>=1, group tuples (j_1,...,j_u) by J=max(j_h).  There are
    J^u-(J-1)^u tuples with maximum J, and a compatible intersection of
    residue classes modulo 3^{j_h} has at most 3^{a-J} residues modulo 3^a.
    """
    if a < 1 or u < 1:
        raise ValueError("a and u must be positive")
    return sum(
        (j**u - (j - 1) ** u) * 3 ** (a - j)
        for j in range(1, a + 1)
    )


def moment_constant(a: int, t: int) -> int:
    """Return H(a,t), the universal t-fold fibre-load moment constant."""
    if a < 1 or t < 1:
        raise ValueError("a and t must be positive")
    return selected_fibre_count(a) + sum(
        comb(t, u) * intersection_level_sum(a, u)
        for u in range(1, t + 1)
    )


def a4_moment_table(max_order: int = 5) -> tuple[int, ...]:
    if max_order < 1:
        raise ValueError("max_order must be positive")
    return tuple(moment_constant(4, t) for t in range(1, max_order + 1))


def support_moment_budget(
    a: int,
    baselines: tuple[Fraction, ...],
) -> Fraction:
    """Return H(a,t)*prod baselines for a t-fold grouped-support moment."""
    if not baselines:
        raise ValueError("need at least one support baseline")
    out = Fraction(moment_constant(a, len(baselines)))
    for b in baselines:
        if b < 0:
            raise ValueError("support baselines must be nonnegative")
        out *= b
    return out


def hierarchy_audit() -> dict:
    # M15 constants are recovered exactly.
    assert moment_constant(3, 1) == 27
    assert moment_constant(4, 1) == 81
    assert moment_constant(4, 2) == 197
    assert moment_constant(5, 2) == 601

    # New higher moments used by the next frontier campaign.
    assert a4_moment_table() == (81, 197, 573, 1925, 7221)
    assert tuple(moment_constant(3, t) for t in range(1, 6)) == (
        27, 63, 171, 519, 1707
    )
    assert tuple(moment_constant(5, t) for t in range(1, 6)) == (
        243, 601, 1809, 6445, 26313
    )

    # Closed forms for the first three intersection sums.
    for a in range(1, 9):
        A = intersection_level_sum(a, 1)
        B = intersection_level_sum(a, 2)
        C = intersection_level_sum(a, 3)
        assert A == (3**a - 1) // 2
        assert B == 3**a - a - 1
        assert 4 * C == 11 * 3**a - 6 * a * a - 12 * a - 11

        # Consequently H(a,3) has a compact closed form.
        assert 4 * moment_constant(a, 3) == (
            31 * 3**a - 6 * a * a - 24 * a - 27
        )

    return {
        "a4": a4_moment_table(),
        "a3": tuple(moment_constant(3, t) for t in range(1, 6)),
        "a5": tuple(moment_constant(5, t) for t in range(1, 6)),
        "third_moment_a4": moment_constant(4, 3),
        "verified": True,
    }


__all__ = [
    "a4_moment_table",
    "hierarchy_audit",
    "intersection_level_sum",
    "moment_constant",
    "selected_fibre_count",
    "support_moment_budget",
]
