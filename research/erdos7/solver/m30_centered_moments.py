"""M30: centered 3-adic moment and factorial hierarchies.

M28 bounds raw support charges q_S.  Saturation gives a deterministic baseline
b_S in every selected fibre, so it is stronger to center first:

    u_S(r) = q_S(r) - b_S >= 0.

If N=3^a M and s_a=(3^a+1)/2 surviving fibres are selected, write

    A_m(r) = sum_{j=1}^a 1[r == c_{j,m} (mod 3^j)]

for each exact M-divisor m.  Then

    u_S(r) = sum_{sqf(m)=S} A_m(r)/m.

For arbitrary, possibly repeated supports S_1,...,S_t,

    sum_r prod_h u_{S_h}(r)
      <= M(a,t) prod_h b_{S_h},

where

    M(a,t)=sum_{J=1}^a (J^t-(J-1)^t) 3^(a-J).

This is the centered binomial component hidden inside M28.  In particular
H(a,t)=sum_{u=0}^t binom(t,u) M(a,u), with M(a,0)=s_a.

When a square-free support S contains only primes occurring to exponent one in
M, there is exactly one exact divisor m with sqf(m)=S.  Then

    q_S/b_S = 1 + A_m,

so A_m is an integer in {0,...,a}.  Its falling-factorial/binomial spikes obey

    sum_r binom(A_m(r),t) <= F(a,t),
    F(a,t)=sum_{J=t}^a binom(J-1,t-1) 3^(a-J).

At a=4 the centered moment constants are 40,76,184,532,1720 and the
single-divisor factorial caps are 40,18,6,1.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb

from m28_moment_hierarchy import moment_constant, selected_fibre_count


def centered_moment_constant(a: int, t: int) -> int:
    """Return M(a,t), the t-fold centered 3-adic moment constant."""
    if a < 1 or t < 1:
        raise ValueError("a and t must be positive")
    return sum(
        (j**t - (j - 1) ** t) * 3 ** (a - j)
        for j in range(1, a + 1)
    )


def centered_support_budget(
    a: int,
    baselines: tuple[Fraction, ...],
) -> Fraction:
    """Return M(a,t)*prod baselines for a centered t-fold support product."""
    if not baselines:
        raise ValueError("need at least one support baseline")
    out = Fraction(centered_moment_constant(a, len(baselines)))
    for b in baselines:
        if b < 0:
            raise ValueError("support baselines must be nonnegative")
        out *= b
    return out


def factorial_spike_cap(a: int, t: int) -> int:
    """Return F(a,t) for one exact divisor's activation count A_m.

    binom(A_m(r),t) is the sum of products of t distinct level indicators.
    Group such level subsets by their largest level J.  There are
    binom(J-1,t-1) choices with maximum J, and a compatible intersection has at
    most 3^(a-J) residues modulo 3^a.
    """
    if a < 1 or t < 1 or t > a:
        raise ValueError("need 1 <= t <= a")
    return sum(
        comb(j - 1, t - 1) * 3 ** (a - j)
        for j in range(t, a + 1)
    )


def raw_from_centered(a: int, t: int) -> int:
    """Recover the M28 raw moment constant H(a,t) by binomial expansion."""
    if a < 1 or t < 1:
        raise ValueError("a and t must be positive")
    return selected_fibre_count(a) + sum(
        comb(t, u) * centered_moment_constant(a, u)
        for u in range(1, t + 1)
    )


def hierarchy_audit() -> dict:
    assert tuple(centered_moment_constant(4, t) for t in range(1, 6)) == (
        40, 76, 184, 532, 1720
    )
    assert tuple(factorial_spike_cap(4, t) for t in range(1, 5)) == (
        40, 18, 6, 1
    )

    # M28 is exactly the binomially uncentered version of M30.
    for a in range(1, 8):
        for t in range(1, 8):
            assert raw_from_centered(a, t) == moment_constant(a, t)

    # Closed forms already implicit in the M28 proof become centered constants.
    for a in range(1, 9):
        assert centered_moment_constant(a, 1) == (3**a - 1) // 2
        assert centered_moment_constant(a, 2) == 3**a - a - 1
        assert 4 * centered_moment_constant(a, 3) == (
            11 * 3**a - 6 * a * a - 12 * a - 11
        )

    return {
        "a4_centered": tuple(centered_moment_constant(4, t) for t in range(1, 6)),
        "a4_factorial": tuple(factorial_spike_cap(4, t) for t in range(1, 5)),
        "raw_recovery_checked": True,
        "verified": True,
    }


__all__ = [
    "centered_moment_constant",
    "centered_support_budget",
    "factorial_spike_cap",
    "hierarchy_audit",
    "raw_from_centered",
]
