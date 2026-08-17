"""M17: exact bridge from M16 to an infinite six-prime exclusion family.

The family is

    N_P = 3^4 * 5^2 * 7 * 11 * 13 * P,

for prime P >= 17.

P in {17,19,23} is handled by the exact M16 quadratic certificates.  For
P >= 29 the McNew-Setty full-divisor density bound is already < 1.

This module independently recomputes the latter statement with Fraction
arithmetic and verifies the exact threshold.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


DIRECT_A = Fraction(220676, 225225)
DIRECT_B = Fraction(17833, 31185)
DIRECT_REAL_THRESHOLD = Fraction(1159145, 40941)
DIRECT_FIRST_INTEGER = 29
DIRECT_R29 = Fraction(58755581, 58783725)


def elementary_symmetric(xs: tuple[Fraction, ...], degree: int) -> Fraction:
    total = Fraction(0)
    for subset in combinations(xs, degree):
        term = Fraction(1)
        for x in subset:
            term *= x
        total += term
    return total


def direct_bound_from_definition(P: int) -> Fraction:
    """Recompute R=e1-e3-e4+2e5+9e6 for the M17 family."""
    if P <= 0:
        raise ValueError("P must be positive")
    xs = (
        Fraction(40, 81),
        Fraction(6, 25),
        Fraction(1, 7),
        Fraction(1, 11),
        Fraction(1, 13),
        Fraction(1, P),
    )
    return (
        elementary_symmetric(xs, 1)
        - elementary_symmetric(xs, 3)
        - elementary_symmetric(xs, 4)
        + 2 * elementary_symmetric(xs, 5)
        + 9 * elementary_symmetric(xs, 6)
    )


def direct_bound_closed(P: int) -> Fraction:
    """Closed form A+B/P for the same full-divisor bound."""
    if P <= 0:
        raise ValueError("P must be positive")
    return DIRECT_A + DIRECT_B / P


def family_number(P: int) -> int:
    return 3**4 * 5**2 * 7 * 11 * 13 * P


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def proof_branch(P: int) -> str:
    """Return the certified branch for a prime P >= 17."""
    if not is_prime(P) or P < 17:
        raise ValueError("P must be a prime >= 17")
    if P in (17, 19, 23):
        return "M16-quadratic"
    assert P >= 29
    assert direct_bound_closed(P) < 1
    return "McNew-Setty-full-divisor"


def infinite_family_audit() -> dict:
    """Verify the exact symbolic bridge used by M17."""
    # Reconstruct the affine-in-1/P formula from two exact evaluations.
    value_at_infinity = direct_bound_from_definition(10**30)
    # Avoid treating a finite proxy as infinity: derive A by setting x_P=0
    # explicitly through the first five coordinates.
    xs5 = (
        Fraction(40, 81),
        Fraction(6, 25),
        Fraction(1, 7),
        Fraction(1, 11),
        Fraction(1, 13),
    )
    A = (
        elementary_symmetric(xs5, 1)
        - elementary_symmetric(xs5, 3)
        - elementary_symmetric(xs5, 4)
        + 2 * elementary_symmetric(xs5, 5)
    )
    B = direct_bound_from_definition(1) - A

    assert A == DIRECT_A
    assert B == DIRECT_B
    assert DIRECT_B > 0
    assert direct_bound_from_definition(17) == direct_bound_closed(17)
    assert direct_bound_from_definition(29) == direct_bound_closed(29)
    assert direct_bound_closed(29) == DIRECT_R29
    assert DIRECT_R29 < 1

    threshold = DIRECT_B / (1 - DIRECT_A)
    assert threshold == DIRECT_REAL_THRESHOLD
    assert 28 < threshold < 29

    # Because B>0, A+B/P decreases with P.  Hence checking P=29 closes all
    # larger integers, while M16 supplies the only primes in [17,28].
    assert [p for p in range(17, 29) if is_prime(p)] == [17, 19, 23]
    assert all(proof_branch(p) == "M16-quadratic" for p in (17, 19, 23))
    assert proof_branch(29) == "McNew-Setty-full-divisor"

    return {
        "family": "3^4*5^2*7*11*13*P",
        "prime_lower_bound": 17,
        "finite_quadratic_primes": (17, 19, 23),
        "direct_first_integer": DIRECT_FIRST_INTEGER,
        "direct_A": DIRECT_A,
        "direct_B": DIRECT_B,
        "direct_threshold": DIRECT_REAL_THRESHOLD,
        "R29": DIRECT_R29,
        "R29_gap": 1 - DIRECT_R29,
        "all_primes_P_ge_17_noncovering": True,
    }


__all__ = [
    "DIRECT_A",
    "DIRECT_B",
    "DIRECT_FIRST_INTEGER",
    "DIRECT_R29",
    "DIRECT_REAL_THRESHOLD",
    "direct_bound_closed",
    "direct_bound_from_definition",
    "elementary_symmetric",
    "family_number",
    "infinite_family_audit",
    "is_prime",
    "proof_branch",
]
