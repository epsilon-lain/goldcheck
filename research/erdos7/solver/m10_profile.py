"""Milestone 10 primitives: first-order dual no-go, head/tail truncation,
and the exact head-signature state.

The lossy-profile program deliberately drops the full ``h_L`` state.  This
module provides the two exact building blocks for that program:

* :func:`first_order_dual_status` proves that the translation-invariant
  first-order weighted-set-cover dual can never exceed the abundance condition
  (N0).
* :func:`head_signature_counts` and :func:`max_top_coverage` implement the head
  signature ``u mod p^a lcm(H)`` together with an exact top-layer evaluator,
  so that a truncated head ``H`` can be evaluated without reconstructing ``U``
  (N1/N3).
"""

from __future__ import annotations

from math import gcd

from covering import divisors, sigma
from profile_optimizer import lift_color


def first_order_dual_status(N: int) -> dict:
    """The N0 no-go: the first-order point-weight dual is exactly abundance.

    The covering LP is infeasible iff ``sigma(N) < 2N``.  For abundant ``N`` the
    translation-averaged optimum is ``0``, so no positive Farkas certificate
    exists; for deficient ``N`` the optimum is unbounded in the positive
    direction, giving a certificate.
    """
    s = sigma(N)
    gap = 2 * N - s
    return {
        "N": N,
        "sigma": s,
        "abundant": s >= 2 * N,
        "symmetric_gap": gap,
        "first_order_certificate_exists": gap > 0,
    }


def _lcm_list(xs: list[int]) -> int:
    out = 1
    for x in xs:
        out = out // gcd(out, x) * x
    return out


def head_modulus(p: int, a: int, H: list[int]) -> int:
    """The head-signature modulus ``Q = p^a * lcm(H)``."""
    return p**a * _lcm_list(H)


def head_signature_counts(p: int, a: int, H: list[int], U: set[int]) -> dict[int, int]:
    """Counts of ``U`` in the head-signature cells ``u mod Q``.

    For every retained top modulus ``p^a e`` (``e in H``), the membership and
    diagonal lift color of a base depend only on ``u mod p^a e``.  Hence the
    common refinement is ``u mod p^a lcm(H)``, and these counts are sufficient
    for the exact top-layer evaluation over ``H``.
    """
    Q = head_modulus(p, a, H)
    counts: dict[int, int] = {}
    for u in U:
        c = u % Q
        counts[c] = counts.get(c, 0) + 1
    return counts


def max_top_coverage(
    p: int,
    a: int,
    M: int,
    U: set[int],
    allowed_es: list[int] | None = None,
) -> int:
    """Exact maximum number of lifts coverable by the top layer.

    Only top moduli ``p^a e`` with ``e in allowed_es`` are available (default:
    all ``e | M``).  The implementation enumerates residue-choice bitmasks and
    is intended for small test instances, not for the large seed.
    """
    U = list(U)
    lifts = [(u, s) for u in U for s in range(p)]
    idx = {lift: i for i, lift in enumerate(lifts)}
    full = (1 << len(lifts)) - 1

    es = divisors(M) if allowed_es is None else allowed_es
    candidates: list[list[int]] = []
    for e in es:
        mod = p**a * e
        masks: list[int] = []
        for r in range(mod):
            m = 0
            for i, (u, s) in enumerate(lifts):
                if lift_color(p, a, M, e, r, u) == s:
                    m |= 1 << i
            if m:
                masks.append(m)
        candidates.append(masks)

    # Order cheap/strong moduli first, then exhaustive DFS with memoization.
    order = sorted(range(len(es)), key=lambda i: len(candidates[i]))
    candidates = [candidates[i] for i in order]

    best = [0]
    memo: dict[tuple[int, int], int] = {}

    def upper_bound(k: int, mask: int) -> int:
        total = mask.bit_count()
        for j in range(k, len(candidates)):
            best_add = 0
            for m in candidates[j]:
                add = (m & ~mask).bit_count()
                if add > best_add:
                    best_add = add
            total += best_add
        return total

    def dfs(k: int, mask: int) -> int:
        key = (k, mask)
        if key in memo:
            return memo[key]
        if mask == full:
            memo[key] = full.bit_count()
            return memo[key]
        if k == len(candidates):
            memo[key] = mask.bit_count()
            return memo[key]
        if upper_bound(k, mask) <= best[0]:
            memo[key] = mask.bit_count()
            return memo[key]
        ans = mask.bit_count()
        # Skip this modulus.
        ans = max(ans, dfs(k + 1, mask))
        # Or choose one residue for it.
        for m in candidates[k]:
            if (m & ~mask) == 0:
                continue
            ans = max(ans, dfs(k + 1, mask | m))
        best[0] = max(best[0], ans)
        memo[key] = ans
        return ans

    return dfs(0, 0)


def tail_budget(p: int, a: int, M: int, U: set[int], T: list[int]) -> int:
    """The N1 safe tail budget ``sum_{e in T} min(M/e, |U|)``."""
    return sum(min(M // e, len(U)) for e in T)


def head_candidates(p: int, a: int, M: int) -> list[tuple[int, int, int, int]]:
    """All divisor-closed heads, sorted by signature modulus.

    For a divisor ``D0 | M`` the head is ``H = {e | D0}``, its signature modulus
    is ``Q = p^a D0``, and the raw tail budget is ``sum_{e|M, e not in H} M/e``.
    Returns rows ``(D0, |H|, Q, B_T)``.
    """
    all_es = divisors(M)
    rows: list[tuple[int, int, int, int]] = []
    for D0 in all_es:
        H = [e for e in all_es if D0 % e == 0]
        T = [e for e in all_es if e not in H]
        Q = p**a * D0
        B = sum(M // e for e in T)
        rows.append((D0, len(H), Q, B))
    rows.sort(key=lambda row: (row[2], row[3]))
    return rows


def _lower_uncovered(L: int, choice: list[tuple[int, int]]) -> set[int]:
    """Reconstruct ``U`` from lower-layer classes ``(modulus, residue)``."""
    covered: set[int] = set()
    for d, r in choice:
        for x in range(r, L, d):
            covered.add(x)
    return {x for x in range(L) if x not in covered}


def head_signature_barrier_witness() -> dict:
    """Explicit realizable barrier for the N3 head-signature feature.

    ``N = 36 = 3^2 * 4`` (so ``p=3, a=2, M=4, L=12``).  With the lossy head
    ``H = {1}`` (only the top modulus ``9``), two realizable lower-layer states
    have identical head-signature counts but different full top capacities:

    * ``U1 = {5,10,11}`` has full top capacity ``5``;
    * ``U2 = {2,5,10}`` has full top capacity ``4``.

    Both arise from valid distinct lower-layer classes below ``L=12``.  The
    ambiguity is resolved by the next tail signature (the modulus ``18``), so
    the minimal correlation missing from ``H={1}`` is the next head modulus.
    """
    p, a, M = 3, 2, 4
    L = p ** (a - 1) * M
    U1 = _lower_uncovered(L, [(3, 0), (4, 0), (6, 1), (12, 2)])
    U2 = _lower_uncovered(L, [(3, 0), (4, 0), (6, 1), (12, 11)])
    H = [1]
    c1 = head_signature_counts(p, a, H, U1)
    c2 = head_signature_counts(p, a, H, U2)
    v1 = max_top_coverage(p, a, M, U1, divisors(M))
    v2 = max_top_coverage(p, a, M, U2, divisors(M))
    return {
        "p": p,
        "a": a,
        "M": M,
        "L": L,
        "H": H,
        "U1": sorted(U1),
        "U2": sorted(U2),
        "head_counts_U1": c1,
        "head_counts_U2": c2,
        "full_top_capacity_U1": v1,
        "full_top_capacity_U2": v2,
        "is_barrier": c1 == c2 and v1 != v2,
    }


__all__ = [
    "first_order_dual_status",
    "head_candidates",
    "head_modulus",
    "head_signature_barrier_witness",
    "head_signature_counts",
    "max_top_coverage",
    "tail_budget",
]
