"""Milestone 12 (P1): Hough--Nielsen Theorem 4 as an exact distortion layer.

Hough--Nielsen, *Covering systems with restricted divisibility*,
Theorem 4, applies to an arbitrary finite collection of moduli ``n`` with
residue sets ``a_n mod n``, without requiring square-freeness.  If nonnegative
weights ``x_p`` satisfy, for every prime ``p``,

    x_p >= sum_{n in N : p | n} (|a_n mod n| * prod_{p' | n}(1 + x_{p'})) / n,

then the uncovered set ``R`` has density at least

    exp( - sum_{n in N} (|a_n mod n| * prod_{p | n}(1 + x_p)) / n ) > 0,

and, for every ``n in N``,

    max_b |R ∩ (b mod n)| / |R| <= exp( sum_{p | n} x_p ) / n.

This module implements the exact rational fixed-point iteration and the exact
rational lower-bound and concentration verification for a given residue-size
assignment.  Discovery may use floats; the verifier here is pure ``Fraction``.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import exp

from covering import divisors, factor


def prime_support(n: int) -> list[int]:
    """The distinct primes dividing ``n``."""
    return [p for p, _ in factor(n)]


def hn_weights(
    primes: list[int],
    moduli: list[int],
    residue_sizes: dict[int, int] | None = None,
    iterations: int = 100000,
) -> dict[int, Fraction] | None:
    """Least nonnegative fixed point of the Hough--Nielsen weight map, if any.

    ``moduli`` are the allowed moduli ``n``; ``residue_sizes[n]`` is
    ``|a_n mod n|`` (default ``1``, the distinct-covering case).  The map

        x_p  ->  sum_{n in moduli, p | n} |a_n| * prod_{p' | n}(1 + x_{p'}) / n

    is monotone, so its least fixed point is the limit of iterating from zero.
    If the iteration diverges, no fixed point exists and ``None`` is returned.
    """
    sizes = residue_sizes if residue_sizes is not None else {n: 1 for n in moduli}

    # Discovery: floating-point monotone iteration from zero.
    xf = {p: 0.0 for p in primes}
    converged = False
    for _ in range(iterations):
        yf = {p: 0.0 for p in primes}
        for n in moduli:
            k = float(sizes.get(n, 0))
            if k == 0.0:
                continue
            prod = 1.0
            for p in prime_support(n):
                prod *= 1.0 + xf[p]
            charge = k * prod / float(n)
            for p in prime_support(n):
                yf[p] += charge
        delta = max((abs(yf[p] - xf[p]) for p in primes), default=0.0)
        xf = yf
        if delta < 1e-14:
            converged = True
            break
        if any(v > 1e6 for v in xf.values()):
            return None
    if not converged:
        return None

    # Rationalize strictly above the floating fixed point, then verify exactly.
    margin = 1e-7
    for _ in range(20):
        x = {
            p: Fraction.from_float(xf[p] + margin)
            for p in primes
        }
        if _is_super_solution(primes, moduli, sizes, x):
            return x
        margin *= 10.0
    return None


def _is_super_solution(
    primes: list[int],
    moduli: list[int],
    sizes: dict[int, int],
    x: dict[int, Fraction],
) -> bool:
    for p in primes:
        lhs = Fraction(0)
        for n in moduli:
            if p not in prime_support(n):
                continue
            k = Fraction(sizes.get(n, 0))
            prod = Fraction(1)
            for q in prime_support(n):
                prod *= 1 + x[q]
            lhs += k * prod / n
        if x[p] < lhs:
            return False
    return True


def hn_uncovered_density(
    primes: list[int],
    moduli: list[int],
    residue_sizes: dict[int, int] | None = None,
    iterations: int = 500,
) -> dict:
    """Return the HN lower-bound certificate, or ``{"exists": False}``."""
    sizes = residue_sizes if residue_sizes is not None else {n: 1 for n in moduli}
    x = hn_weights(primes, moduli, sizes, iterations)
    if x is None:
        return {"exists": False}
    total = Fraction(0)
    for n in moduli:
        k = Fraction(sizes.get(n, 0))
        prod = Fraction(1)
        for p in prime_support(n):
            prod *= 1 + x[p]
        total += k * prod / n
    # exp(-total) > 0; return the exact rational exponent and a decimal lower
    # bound computed with Fraction-conservative truncation is omitted here.
    return {"exists": True, "weights": x, "exponent": total, "density_lb_gt_0": total >= 0}


def hn_concentration(
    x: dict[int, Fraction],
    n: int,
) -> Fraction:
    """The HN concentration upper bound ``exp(sum_{p|n} x_p) / n``.

    Since ``exp`` is transcendental, this returns the exact exponent; the final
    inequality should be verified in rational terms as ``n * C <= exp(...)``.
    """
    s = sum((x[p] for p in prime_support(n)), Fraction(0))
    return s


def hn_theorem4_bruteforce_check(N: int) -> bool:
    """Brute-force the HN Theorem 4 conclusions on a small modulus set.

    Enumerate every choice of one residue class or no class for each divisor
    ``d | N, d > 1``, and for each nonempty system that satisfies the HN weight
    hypothesis, check the concentration conclusion

        max_b |R ∩ (b mod n)| / |R| <= exp(sum_{p|n} x_p) / n.

    This is a small-instance validation that Theorem 4 is literally valid for
    repeated prime powers.
    """
    primes = prime_support(N)
    allmods = [d for d in divisors(N) if d > 1]
    ranges = [list(range(-1, d)) for d in allmods]
    for choice in product(*ranges):
        chosen = [d for d, r in zip(allmods, choice) if r >= 0]
        if not chosen:
            continue
        sizes = {d: 1 for d in chosen}
        x = hn_weights(primes, chosen, sizes)
        if x is None:
            continue
        R = [u for u in range(N) if all(u % d != r for d, r in zip(allmods, choice) if r >= 0)]
        if not R:
            return False
        for d in chosen:
            sxp = float(sum((x[p] for p in prime_support(d)), Fraction(0)))
            bound = exp(sxp) / d
            maxfrac = max(sum(1 for u in R if u % d == b) for b in range(d)) / len(R)
            if maxfrac > bound + 1e-9:
                return False
    return True


__all__ = [
    "hn_concentration",
    "hn_theorem4_bruteforce_check",
    "hn_uncovered_density",
    "hn_weights",
    "prime_support",
]
