"""Conditioned top-layer profile inequality (Milestone 3, Task F1).

For ``N = p^a M`` with ``gcd(p, M) = 1``, write ``L = N/p = p^{a-1} M``.  Fix a
choice of all congruence classes whose moduli divide ``L`` (the *lower layer*),
and let ``U`` be the set of residues of ``Z/LZ`` left uncovered by that layer.

For a divisor ``d | L`` define the *profile*

    mu_d(U) = max_b |{ u in U : u ≡ b (mod d) }|.

The *top layer* consists of the full-``p``-adic moduli ``p^a e`` for ``e | M``.
One such class, ``r mod p^a e``, can meet only lifts ``u + tL`` whose base ``u``
lies in the single residue class ``r mod p^{a-1} e``, and it meets at most one
lift of each such ``u``.  Hence it meets at most ``mu_{p^{a-1} e}(U)`` lifts, so
the whole top layer covers at most

    C(U) = sum_{e | M} mu_{p^{a-1} e}(U)

of the ``p * |U|`` lifts.  A full cover therefore requires

    p * |U| <= C(U).

This strictly refines the raw deficiency recurrence: since
``mu_{p^{a-1} e}(U) <= M/e``, replacing every profile term by ``M/e`` recovers
``sigma(M)``.
"""

from __future__ import annotations

from itertools import product

from covering import divisors


def uncovered(N: int, p: int, lower: dict[int, int]) -> list[int]:
    """Residues of ``Z/(N/p)Z`` not covered by the lower-layer classes."""
    L = N // p
    out: list[int] = []
    for x in range(L):
        covered = any(x % d == r for d, r in lower.items())
        if not covered:
            out.append(x)
    return out


def mu(U: list[int], d: int) -> int:
    """``max_b |{u in U : u ≡ b (mod d)}|``."""
    if not U:
        return 0
    counts: dict[int, int] = {}
    best = 0
    for u in U:
        b = u % d
        counts[b] = counts.get(b, 0) + 1
        if counts[b] > best:
            best = counts[b]
    return best


def profile_capacity(p: int, a: int, M: int, U: list[int]) -> int:
    """``sum_{e | M} mu_{p^{a-1} e}(U)``."""
    return sum(mu(U, p ** (a - 1) * e) for e in divisors(M) if e >= 1)


def lower_choices(L: int):
    """All lower-layer choices: for every divisor ``d | L, d > 1``, either
    unused or a single residue class ``r mod d``."""
    ds = [d for d in divisors(L) if d > 1]
    ranges = [list(range(d)) + [None] for d in ds]
    for combo in product(*ranges):
        yield {d: r for d, r in zip(ds, combo) if r is not None}


def top_lifts_met(N: int, p: int, a: int, e: int, r: int, U: list[int]) -> int:
    """Number of lifts ``u + t·(N/p)`` (``u in U``, ``0 <= t < p``) lying in
    the residue class ``r mod p^a e``."""
    L = N // p
    top_mod = p**a * e
    total = 0
    for u in U:
        for t in range(p):
            if (u + t * L) % top_mod == r:
                total += 1
    return total


def max_top_coverage(N: int, p: int, a: int, M: int, U: list[int]) -> int:
    """Brute-force maximum number of lifts of ``U`` coverable by the top layer.

    Enumerates, for each ``e | M``, a single residue (or unused) for the modulus
    ``p^a e``.  Only for small instances in tests.
    """
    L = N // p
    es = [e for e in divisors(M) if e >= 1]
    best = 0
    # Iterate over all assignments: -1 means "unused".
    ranges = [list(range(p**a * e)) + [-1] for e in es]
    for combo in product(*ranges):
        covered = set()
        for e, r in zip(es, combo):
            if r < 0:
                continue
            top_mod = p**a * e
            for u in U:
                for t in range(p):
                    if (u + t * L) % top_mod == r:
                        covered.add((u, t))
        if len(covered) > best:
            best = len(covered)
    return best
