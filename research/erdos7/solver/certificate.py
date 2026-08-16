"""Exact deficiency certificates for the Erdős #7 stragglers.

This module computes *rigorous* lower bounds on

    delta(N) = N - r(N),

where ``r(N)`` is the maximum number of residue classes modulo ``N`` that can be
covered by a family of congruence classes with pairwise *distinct* moduli ``d > 1``
dividing ``N``.  A positive integer ``N`` is a covering number exactly when
``delta(N) = 0``.

The two ingredients, both proved in ``NOTES.md``, are

* **Square-free CRT/Hall bound** (a specialisation of McNew--Setty Lemma 4.10).
  For odd square-free ``n = prod_i p_i``, the inclusion--exclusion bound gives

      r(n) <= sum_{U nonempty} C_|U| * prod_{i not in U} p_i,

  where ``C_j = sum_{t=1..j} (-1)^{t+1} S2(j, t)`` and ``S2`` is the Stirling
  number of the second kind.  Equivalently ``delta(n) >= n - (that sum)``.

* **Deficiency recurrence** (proved here and in ``NOTES.md``).  For
  ``N = p^a * M`` with ``gcd(p, M) = 1``,

      delta(N) >= p * delta(N/p) - sigma(M).

Chaining the recurrence down to an odd square-free base gives the certificates.
All arithmetic is exact Python integer arithmetic.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

from covering import factor, sigma


@lru_cache(maxsize=None)
def stirling2(n: int, k: int) -> int:
    """Stirling number of the second kind ``S2(n, k)``."""
    if k == 0:
        return int(n == 0)
    if n == 0:
        return 0
    if k > n:
        return 0
    if k == n or k == 1:
        return 1
    return k * stirling2(n - 1, k) + stirling2(n - 1, k - 1)


@lru_cache(maxsize=None)
def complementary_bell_coeff(j: int) -> int:
    """``C_j = sum_{t=1..j} (-1)^{t+1} S2(j, t)`` (negative complementary Bell)."""
    return sum((-1) ** (t + 1) * stirling2(j, t) for t in range(1, j + 1))


def squarefree_coverage_bound(n: int) -> int:
    """Upper bound on ``r(n)`` for odd square-free ``n`` (McNew--Setty Lemma 4.10).

    Returns the inclusion--exclusion value

        sum_{U nonempty subset of primes} C_|U| * prod_{i notin U} p_i.

    This is the number of residues a *distinct-moduli* system with moduli the
    divisors of ``n`` can cover at most.
    """
    fs = factor(n)
    if any(e != 1 for _, e in fs) or any(p == 2 for p, _ in fs):
        raise ValueError("squarefree_coverage_bound expects an odd square-free n")
    primes = [p for p, _ in fs]
    k = len(primes)
    total = 0
    for size in range(1, k + 1):
        coeff = complementary_bell_coeff(size)
        for subset in combinations(range(k), size):
            outside = 1
            for i in range(k):
                if i not in subset:
                    outside *= primes[i]
            total += coeff * outside
    return total


def squarefree_delta_lower(n: int) -> int:
    """Certified lower bound on ``delta(n)`` for odd square-free ``n``."""
    return n - squarefree_coverage_bound(n)


def delta_lower(n: int) -> int:
    """Best available certified lower bound for ``delta(n)``."""
    return best_chain(n)[0]


def best_chain(n: int) -> tuple[int, list[str]]:
    """Return ``(bound, human_readable_chain)`` for ``delta(n)``.

    Odd square-free arguments use the CRT/Hall square-free bound; everything
    else takes the best one-step recurrence over its prime divisors.
    """
    if n == 1:
        return 1, ["  delta(1) >= 1  [base case: r(1) = 0]"]
    fs = factor(n)
    if all(e == 1 for _, e in fs) and n % 2 == 1:
        bound = squarefree_delta_lower(n)
        return bound, [f"  delta({n}) >= {bound}  [square-free CRT/Hall bound]"]

    best = 0
    best_p: int | None = None
    best_lines: list[str] = []
    for p, a in fs:
        M = n // (p ** a)
        sub, sub_lines = best_chain(n // p)
        cand = p * sub - sigma(M)
        if cand > best:
            best = cand
            best_p = p
            best_lines = [
                f"  delta({n}) >= {p}*delta({n // p}) - sigma({M})"
                f" = {p}*delta({n // p}) - {sigma(M)}  [deficiency recurrence, p={p}]"
            ] + sub_lines
    if best_p is None:
        return 0, [f"  delta({n}) >= 0  [trivial]"]
    return max(0, best), best_lines


def certify(N: int) -> tuple[int, str]:
    """Return ``(lower_bound_on_delta, human_readable_chain)`` for N."""
    bound, chain_lines = best_chain(N)
    fs = factor(N)
    lines = [f"N = {N} = " + " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in fs)]
    lines.extend(chain_lines)
    lines.append(f"delta({N}) >= {bound}")
    lines.append("conclusion: " + ("NOT a covering number" if bound >= 1 else "no conclusion"))
    return bound, "\n".join(lines)


def all_primes_lemma_holds(N: int) -> bool:
    """Check the all-primes primitive-covering necessary condition on N.

    Returns ``True`` iff ``p <= tau(N / p^v_p(N))`` for every prime ``p | N``.
    This is a *necessary* (not sufficient) condition for ``N`` to be a primitive
    covering number; see ``NOTES.md``.
    """
    for p, a in factor(N):
        M = N // (p ** a)
        if p > _tau(M):
            return False
    return True


def _tau(n: int) -> int:
    result = 1
    for _, e in factor(n):
        result *= e + 1
    return result


def verify_certificates() -> dict[int, int]:
    """Run the certificate targets and return ``{N: lower_bound}``."""
    expected = {945: 123, 10395: 360, 12285: 606, 17325: 312}
    out: dict[int, int] = {}
    for N in (945, 10395, 12285, 17325):
        bound, _ = certify(N)
        assert bound == expected[N], f"certificate mismatch for {N}: {bound} != {expected[N]}"
        assert bound >= 1
        out[N] = bound
    return out


__all__ = [
    "all_primes_lemma_holds",
    "best_chain",
    "certify",
    "complementary_bell_coeff",
    "delta_lower",
    "squarefree_coverage_bound",
    "squarefree_delta_lower",
    "stirling2",
    "verify_certificates",
]
