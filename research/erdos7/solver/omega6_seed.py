"""Milestone 9 (M9.2): the first six-prime primitive-candidate seed.

The published BFF 1987 theorem gives ``omega(N) >= 6`` but does not settle the
six-prime case.  This module computes, with exact arithmetic, the smallest
odd six-prime candidate that survives every proved necessary filter currently
in the repository:

* six distinct odd prime factors;
* abundance ``sigma(N) > 2N``;
* the all-primes primitive condition ``p_i <= prod_{j != i}(a_j + 1)``;
* the full McNew--Setty Lemma 4.10 bound (``R(N) >= 1`` is necessary to
  survive);
* the BFF 1987 support bound (``bff_bound(support) >= 2``; if the
  infinite-exponent value is ``< 2`` then the whole support is excluded).

The completeness argument is:

1. For a fixed support ``{p_1 < ... < p_6}``, the BFF parameter ``g`` is
   increasing in each ``z_i``/``w`` and those parameters are bounded above by
   their infinite-exponent values, so ``bff_bound`` is the maximum over all
   exponents.  Therefore a support with ``bff_bound < 2`` is excluded for every
   exponent pattern, and only supports with ``bff_bound >= 2`` need be searched.
2. :func:`omega6_support_pool` enumerates *all* such supports exactly by a DFS
   whose pruning uses the same monotonicity: replacing an unchosen prime by a
   smaller one can only increase ``g``, so the maximum completion of a prefix is
   obtained with the smallest available primes.
3. For each surviving support, :func:`smallest_omega6_survivor` enumerates every
   exponent vector whose product is below the running best candidate, so no
   smaller survivor can be missed.

The result is used only as a finite discovery seed for the profile optimizer;
it is **not** a claim that the seed is a covering number.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

from bff1987 import bff_bound
from full_bound import (
    all_primes_condition_vec,
    n_from,
    sigma_from,
    support_R,
)


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


def _next_odd_primes_after(last: int, k: int) -> list[int]:
    """The ``k`` smallest odd primes strictly greater than ``last``."""
    out: list[int] = []
    n = last + 1
    if n % 2 == 0:
        n += 1
    while len(out) < k:
        if is_prime(n):
            out.append(n)
        n += 2
    return out


def omega6_support_pool() -> list[tuple[int, ...]]:
    """All six-prime supports not excluded by the BFF 1987 support bound.

    A support is kept exactly when ``bff_bound(sorted_support) >= 2``.  The DFS
    is complete because, for a fixed prefix of small primes, the completion with
    the smallest remaining odd primes maximises ``g``.
    """
    pool: list[tuple[int, ...]] = []

    def dfs(prefix: list[int]) -> None:
        if len(prefix) == 6:
            if bff_bound(prefix) >= 2:
                pool.append(tuple(prefix))
            return
        last = prefix[-1] if prefix else 2
        minimal = prefix + _next_odd_primes_after(last, 6 - len(prefix))
        if bff_bound(minimal) < 2:
            return
        p = last + 1
        if p % 2 == 0:
            p += 1
        while True:
            if not is_prime(p):
                p += 2
                continue
            remaining = _next_odd_primes_after(p, 6 - len(prefix) - 1)
            if bff_bound(prefix + [p] + remaining) < 2:
                break
            dfs(prefix + [p])
            p += 2

    dfs([])
    return pool


def _omega6_survivor(primes: list[int], exps: list[int], n: int) -> bool:
    return (
        all_primes_condition_vec(primes, exps)
        and sigma_from(primes, exps) > 2 * n
        and support_R(primes, exps) >= 1
    )


def _enumerate_exps_under(primes: list[int], cap: int):
    """Yield every exponent vector (>=1) with ``prod p_i^{a_i} < cap``."""
    exps = [1] * len(primes)
    yield from _dfs_exps(primes, 0, 1, cap, exps)


def _dfs_exps(primes: list[int], idx: int, cur: int, cap: int, exps: list[int]):
    if idx == len(primes):
        if cur < cap:
            yield list(exps)
        return
    p = primes[idx]
    other_min = 1
    for j in range(idx + 1, len(primes)):
        other_min *= primes[j]
    e = 1
    while cur * (p**e) * other_min < cap:
        exps[idx] = e
        yield from _dfs_exps(primes, idx + 1, cur * (p**e), cap, exps)
        e += 1
    exps[idx] = 1


def omega6_survivors(cap: int) -> list[tuple[int, tuple[int, ...], tuple[int, ...], Fraction]]:
    """All six-prime survivors below ``cap``, sorted by ``N``.

    Each row is ``(N, support, exponents, R(N))``.  This is complete for ``N <
    cap`` by the support-pool completeness and the exponent-pruning argument.
    """
    rows: list[tuple[int, tuple[int, ...], tuple[int, ...], Fraction]] = []
    for support in omega6_support_pool():
        primes = list(support)
        for exps in _enumerate_exps_under(primes, cap):
            n = n_from(primes, exps)
            if not _omega6_survivor(primes, exps, n):
                continue
            rows.append((n, tuple(primes), tuple(exps), support_R(primes, exps)))
    rows.sort(key=lambda row: row[0])
    return rows


def smallest_omega6_survivor() -> tuple[int, tuple[int, ...], tuple[int, ...], Fraction]:
    """The smallest six-prime candidate surviving every current filter."""
    return omega6_survivors(50_000_000)[0]


__all__ = [
    "is_prime",
    "omega6_support_pool",
    "omega6_survivors",
    "smallest_omega6_survivor",
]
