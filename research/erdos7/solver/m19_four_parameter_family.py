"""M19: exact bridge to a four-parameter six-prime exclusion family.

For distinct primes p<q<r<s with p>=7, verify that

    N = 3^4 * 5^2 * p * q * r * s

is noncovering.  The p=7 branch is M18; the p>=11 branch is killed by the
McNew-Setty full-divisor bound plus an exact coordinatewise monotonicity margin.
"""

from __future__ import annotations

from fractions import Fraction

from m17_infinite_family import elementary_symmetric, is_prime
from m18_three_parameter_family import proof_branch as m18_proof_branch


MONOTONICITY_E23_CAP = Fraction(137266, 231525)
MONOTONICITY_DERIVATIVE_GAP = Fraction(94259, 231525)
DIRECT_ANCHOR = Fraction(276127, 289575)


def direct_bound_four_primes(p: int, q: int, r: int, s: int) -> Fraction:
    if min(p, q, r, s) <= 0:
        raise ValueError("prime parameters must be positive")
    xs = (
        Fraction(40, 81),
        Fraction(6, 25),
        Fraction(1, p),
        Fraction(1, q),
        Fraction(1, r),
        Fraction(1, s),
    )
    return (
        elementary_symmetric(xs, 1)
        - elementary_symmetric(xs, 3)
        - elementary_symmetric(xs, 4)
        + 2 * elementary_symmetric(xs, 5)
        + 9 * elementary_symmetric(xs, 6)
    )


def monotonicity_derivative_lower_bound() -> Fraction:
    U = (
        Fraction(40, 81),
        Fraction(6, 25),
        Fraction(1, 7),
        Fraction(1, 7),
        Fraction(1, 7),
    )
    cap = elementary_symmetric(U, 2) + elementary_symmetric(U, 3)
    assert cap == MONOTONICITY_E23_CAP
    gap = 1 - cap
    assert gap == MONOTONICITY_DERIVATIVE_GAP
    assert gap > 0
    return gap


def _ordered_distinct_primes(
    p: int, q: int, r: int, s: int
) -> tuple[int, int, int, int]:
    quad = tuple(sorted((p, q, r, s)))
    if len(set(quad)) != 4:
        raise ValueError("p,q,r,s must be distinct primes")
    if not all(is_prime(t) for t in quad):
        raise ValueError("p,q,r,s must be prime")
    if quad[0] < 7:
        raise ValueError("the smallest variable prime must be at least 7")
    return quad


def family_number(p: int, q: int, r: int, s: int) -> int:
    return 3**4 * 5**2 * p * q * r * s


def proof_branch(p: int, q: int, r: int, s: int) -> str:
    p, q, r, s = _ordered_distinct_primes(p, q, r, s)

    if p == 7:
        assert q >= 11
        assert m18_proof_branch(q, r, s) in (
            "M16-quadratic",
            "McNew-Setty-full-divisor",
        )
        return "M18-three-parameter"

    assert p >= 11 and q >= 13 and r >= 17 and s >= 19
    assert monotonicity_derivative_lower_bound() > 0
    assert direct_bound_four_primes(11, 13, 17, 19) == DIRECT_ANCHOR
    assert DIRECT_ANCHOR < 1
    assert direct_bound_four_primes(p, q, r, s) <= DIRECT_ANCHOR
    return "McNew-Setty-full-divisor"


def four_parameter_family_audit() -> dict:
    gap = monotonicity_derivative_lower_bound()
    assert direct_bound_four_primes(11, 13, 17, 19) == DIRECT_ANCHOR
    assert 1 - DIRECT_ANCHOR == Fraction(13448, 289575)

    assert proof_branch(7, 11, 13, 17) == "M18-three-parameter"
    assert proof_branch(7, 17, 19, 23) == "M18-three-parameter"
    assert proof_branch(11, 13, 17, 19) == "McNew-Setty-full-divisor"
    assert proof_branch(13, 17, 19, 23) == "McNew-Setty-full-divisor"

    return {
        "family": "3^4*5^2*p*q*r*s",
        "variable_prime_lower_bound": 7,
        "direct_anchor": DIRECT_ANCHOR,
        "direct_anchor_gap": 1 - DIRECT_ANCHOR,
        "coordinate_derivative_lower_bound": gap,
        "all_distinct_primes_p_q_r_s_ge_7_noncovering": True,
    }


__all__ = [
    "DIRECT_ANCHOR",
    "MONOTONICITY_DERIVATIVE_GAP",
    "MONOTONICITY_E23_CAP",
    "direct_bound_four_primes",
    "family_number",
    "four_parameter_family_audit",
    "monotonicity_derivative_lower_bound",
    "proof_branch",
]
