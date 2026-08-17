"""Milestone 11 (O0/O1): sound lossy head/tail abstraction.

The Milestone 10 barrier showed that the exact top capacity is not a function of
``phi_H(U)=(|U|,h_Q(U))``.  It does **not** show that ``phi_H`` is useless: a
sound abstraction may over-approximate the shared cell by the worst possible
full top capacity and still prove every member of the cell is non-coverable.

This module implements exactly that sound envelope:

    Cbar_H(|U|, h_Q) := C_H(h_Q) + sum_{e in T} min(M/e, |U|),

where ``C_H(h_Q)`` is the exact head capacity computed from the histogram
alone, and ``T`` is the discarded tail of top divisors.
"""

from __future__ import annotations

from itertools import product

from covering import divisors
from m10_profile import (
    head_candidates,
    head_modulus,
    head_signature_counts,
    max_top_coverage,
)


def representative_U(p: int, a: int, M: int, H: list[int], counts: dict[int, int]) -> set[int]:
    """A concrete base set realising histogram ``counts`` modulo ``Q``.

    For each residue ``c`` with count ``k`` the representative uses
    ``c, c+Q, c+2Q, ...`` below ``L = p^{a-1}M``.  Any two representatives of
    the same histogram have the same retained-top-class incidences, so
    ``C_H`` is well-defined on ``counts``.
    """
    Q = head_modulus(p, a, H)
    L = p ** (a - 1) * M
    out: set[int] = set()
    for c, k in counts.items():
        for j in range(k):
            u = c + j * Q
            if u >= L:
                raise ValueError("count exceeds the number of bases in this residue cell")
            out.add(u)
    return out


def head_capacity_from_counts(
    p: int, a: int, M: int, H: list[int], counts: dict[int, int]
) -> int:
    """Exact ``C_H`` from the head-signature histogram alone."""
    U = representative_U(p, a, M, H, counts)
    return max_top_coverage(p, a, M, U, H)


def tail_budget_from_size(p: int, a: int, M: int, H: list[int], size: int) -> int:
    """``sum_{e|M, e not in H} min(M/e, size)``."""
    Hset = set(H)
    return sum(min(M // e, size) for e in divisors(M) if e not in Hset)


def head_envelope(
    p: int, a: int, M: int, H: list[int], counts: dict[int, int], size: int
) -> int:
    """The sound lossy capacity envelope ``C_H(h_Q) + tail_budget(|U|)``."""
    return head_capacity_from_counts(p, a, M, H, counts) + tail_budget_from_size(
        p, a, M, H, size
    )


def pareto_heads(p: int, a: int, M: int) -> list[tuple[int, int, int, int]]:
    """Nondominated divisor-closed heads under ``(Q, B_T)``.

    A head is kept unless another head has both a no-larger signature modulus
    and a no-larger raw tail budget, with at least one strict.
    """
    rows = head_candidates(p, a, M)
    pareto: list[tuple[int, int, int, int]] = []
    for D0, size, Q, B in rows:
        dominated = any(
            Q2 <= Q and B2 <= B and (Q2 < Q or B2 < B)
            for _, _, Q2, B2 in pareto
        )
        if dominated:
            continue
        pareto = [
            r
            for r in pareto
            if not (Q <= r[2] and B <= r[3] and (Q < r[2] or B < r[3]))
        ]
        pareto.append((D0, size, Q, B))
    pareto.sort(key=lambda r: (r[2], r[3]))
    return pareto


def realizable_lower_states(p: int, a: int, M: int):
    """Yield every nonempty realizable lower-uncovered set for small ``L``.

    A lower layer chooses, for each divisor ``d | L, d > 1``, one residue class
    or no class.  This exhaustive generator is for small toy instances only.
    """
    L = p ** (a - 1) * M
    lower_divs = [d for d in divisors(L) if d > 1]
    ranges = [list(range(-1, d)) for d in lower_divs]
    seen: set[frozenset[int]] = set()
    for choice in product(*ranges):
        covered: set[int] = set()
        for d, r in zip(lower_divs, choice):
            if r < 0:
                continue
            for x in range(r, L, d):
                covered.add(x)
        U = frozenset(x for x in range(L) if x not in covered)
        if not U or U in seen:
            continue
        seen.add(U)
        yield set(U)


def abstract_noncovering_certificate(p: int, a: int, M: int, H: list[int]) -> dict:
    """Exhaustively verify the lossy head/tail envelope kills a small instance.

    Returns ``{"states": n, "all_killed": bool}`` where ``all_killed`` means the
    envelope ``Cbar_H(phi_H(U)) < p|U|`` holds for every realizable ``U``.
    """
    all_es = divisors(M)
    states = 0
    for U in realizable_lower_states(p, a, M):
        states += 1
        counts = head_signature_counts(p, a, H, U)
        size = len(U)
        env = head_envelope(p, a, M, H, counts, size)
        true = max_top_coverage(p, a, M, U, all_es)
        if env < true:
            raise AssertionError("envelope is not an upper bound")
        if env >= p * size:
            return {"states": states, "all_killed": False, "witness": sorted(U)}
    return {"states": states, "all_killed": True, "witness": None}


__all__ = [
    "abstract_noncovering_certificate",
    "head_capacity_from_counts",
    "head_envelope",
    "pareto_heads",
    "realizable_lower_states",
    "representative_U",
    "tail_budget_from_size",
]
