"""M18: exact bridge to a three-parameter six-prime exclusion family.

For distinct primes p<q<r with p>=11, this module verifies that

    N = 3^4 * 5^2 * 7 * p * q * r

is excluded by one of two branches:

* the exact M16 quadratic certificates for the three exceptional triples
  (11,13,17), (11,13,19), (11,13,23);
* the McNew-Setty full-divisor bound everywhere else.

The direct bound is shown coordinatewise monotone on the entire relevant box by
an exact positive lower bound for every partial derivative.
"""

from __future__ import annotations

from fractions import Fraction

from m16_quadratic_frontier import FRONTIER_PRIMES
from m17_infinite_family import elementary_symmetric, is_prime


MONOTONICITY_E23_CAP = Fraction(111682, 245025)
MONOTONICITY_DERIVATIVE_GAP = Fraction(133343, 245025)
R_11_13_29 = Fraction(58755581, 58783725)
R_11_17_19 = Fraction(7187843, 7194825)


def direct_bound_three_primes(p: int, q: int, r: int) -> Fraction:
    """Return R=e1-e3-e4+2e5+9e6 for 3^4*5^2*7*p*q*r."""
    if min(p, q, r) <= 0:
        raise ValueError("prime parameters must be positive")
    xs = (
        Fraction(40, 81),
        Fraction(6, 25),
        Fraction(1, 7),
        Fraction(1, p),
        Fraction(1, q),
        Fraction(1, r),
    )
    return (
        elementary_symmetric(xs, 1)
        - elementary_symmetric(xs, 3)
        - elementary_symmetric(xs, 4)
        + 2 * elementary_symmetric(xs, 5)
        + 9 * elementary_symmetric(xs, 6)
    )


def monotonicity_derivative_lower_bound() -> Fraction:
    """Exact universal positive lower bound for every coordinate derivative.

    For R=e1-e3-e4+2e5+9e6,

        dR/dx_i = 1-e2(y)-e3(y)+2e4(y)+9e5(y)
                >= 1-e2(y)-e3(y).

    Every five-coordinate remainder y in the present parameter box is, after
    sorting, coordinatewise at most

        U=(40/81, 6/25, 1/7, 1/11, 1/11).

    Hence e2(y)+e3(y) <= e2(U)+e3(U) exactly.
    """
    U = (
        Fraction(40, 81),
        Fraction(6, 25),
        Fraction(1, 7),
        Fraction(1, 11),
        Fraction(1, 11),
    )
    cap = elementary_symmetric(U, 2) + elementary_symmetric(U, 3)
    assert cap == MONOTONICITY_E23_CAP
    gap = 1 - cap
    assert gap == MONOTONICITY_DERIVATIVE_GAP
    assert gap > 0
    return gap


def family_number(p: int, q: int, r: int) -> int:
    return 3**4 * 5**2 * 7 * p * q * r


def _ordered_distinct_primes(p: int, q: int, r: int) -> tuple[int, int, int]:
    triple = tuple(sorted((p, q, r)))
    if len(set(triple)) != 3:
        raise ValueError("p,q,r must be distinct primes")
    if not all(is_prime(t) for t in triple):
        raise ValueError("p,q,r must be prime")
    if triple[0] < 11:
        raise ValueError("the smallest variable prime must be at least 11")
    return triple


def proof_branch(p: int, q: int, r: int) -> str:
    """Return the certified proof branch for the M18 family."""
    p, q, r = _ordered_distinct_primes(p, q, r)

    if (p, q) == (11, 13) and r in FRONTIER_PRIMES:
        assert FRONTIER_PRIMES == (17, 19, 23)
        return "M16-quadratic"

    # Coordinatewise monotonicity is certified separately by the positive
    # derivative bound.  Only two minimal direct-bound anchor points are needed.
    assert monotonicity_derivative_lower_bound() > 0

    if (p, q) == (11, 13):
        # The only primes above 23 start at 29.
        assert r >= 29
        assert direct_bound_three_primes(11, 13, 29) == R_11_13_29
        assert R_11_13_29 < 1
        assert direct_bound_three_primes(p, q, r) <= R_11_13_29
        return "McNew-Setty-full-divisor"

    # If the first two primes are not 11,13 then q>=17 and r>=19.
    assert p >= 11 and q >= 17 and r >= 19
    assert direct_bound_three_primes(11, 17, 19) == R_11_17_19
    assert R_11_17_19 < 1
    assert direct_bound_three_primes(p, q, r) <= R_11_17_19
    return "McNew-Setty-full-divisor"


def three_parameter_family_audit() -> dict:
    """Verify the exact M18 bridge."""
    assert FRONTIER_PRIMES == (17, 19, 23)
    derivative_gap = monotonicity_derivative_lower_bound()

    assert direct_bound_three_primes(11, 13, 29) == R_11_13_29
    assert 1 - R_11_13_29 == Fraction(28144, 58783725)
    assert direct_bound_three_primes(11, 17, 19) == R_11_17_19
    assert 1 - R_11_17_19 == Fraction(6982, 7194825)

    for last in FRONTIER_PRIMES:
        assert proof_branch(11, 13, last) == "M16-quadratic"

    assert proof_branch(11, 13, 29) == "McNew-Setty-full-divisor"
    assert proof_branch(11, 17, 19) == "McNew-Setty-full-divisor"
    assert proof_branch(13, 17, 19) == "McNew-Setty-full-divisor"
    assert proof_branch(17, 19, 23) == "McNew-Setty-full-divisor"

    return {
        "family": "3^4*5^2*7*p*q*r",
        "variable_prime_lower_bound": 11,
        "exceptional_quadratic_triples": tuple(
            (11, 13, last) for last in FRONTIER_PRIMES
        ),
        "direct_anchor_11_13_29": R_11_13_29,
        "direct_anchor_11_17_19": R_11_17_19,
        "coordinate_derivative_lower_bound": derivative_gap,
        "all_distinct_primes_p_q_r_ge_11_noncovering": True,
    }


__all__ = [
    "MONOTONICITY_DERIVATIVE_GAP",
    "MONOTONICITY_E23_CAP",
    "R_11_13_29",
    "R_11_17_19",
    "direct_bound_three_primes",
    "family_number",
    "monotonicity_derivative_lower_bound",
    "proof_branch",
    "three_parameter_family_audit",
]
