"""Milestone 13 (Q2): finite 27-fiber adversary for the first HN stage.

For ``N* = 11486475`` with ``Q0 = 27`` and ``M = 425425``, the pure 3-adic
moduli ``3, 9, 27`` first remove at most ``9 + 3 + 1`` of the 27 base fibers.
The remaining base fibers are the surviving residues ``r mod 27``.

For every ``m | M`` and surviving ``r``, the original moduli
``m, 3m, 9m, 27m`` induce at most

    k_m(r) <= 1 + 1[r ≡ c_{1,m} (mod 3)]
                + 1[r ≡ c_{2,m} (mod 9)]
                + 1[r ≡ c_{3,m} (mod 27)]

residue classes modulo ``m``, where the ``c_{j,m}`` are the adversary's 3-adic
residue choices.  Duplicate induced residues only reduce the load, so this
upper bound is safe.
"""

from __future__ import annotations


def pure3_choices():
    """All ``(c1 mod 3, c2 mod 9, c3 mod 27)`` choices."""
    for c1 in range(3):
        for c2 in range(9):
            for c3 in range(27):
                yield c1, c2, c3


def surviving_fibers(c1: int, c2: int, c3: int) -> set[int]:
    """Residues ``r mod 27`` not covered by the three pure 3-adic classes."""
    return {
        r
        for r in range(27)
        if r % 3 != c1 and r % 9 != c2 and r != c3
    }


def min_surviving_fibers() -> int:
    """The worst-case number of surviving base fibers."""
    return min(len(surviving_fibers(*c)) for c in pure3_choices())


def worst_total_load(S: set[int]) -> int:
    """Exact maximum of ``sum_{r in S} k_m(r)`` over the adversary choices.

    The three indicator sums are independent, so each is maximised by choosing
    the most frequent residue in the corresponding modulus.
    """
    if not S:
        return 0
    best1 = max(sum(1 for r in S if r % 3 == b) for b in range(3))
    best2 = max(sum(1 for r in S if r % 9 == b) for b in range(9))
    best3 = 1  # S consists of distinct residues mod 27.
    return len(S) + best1 + best2 + best3


def verify_pure3_bruteforce() -> dict:
    """Independent brute-force check of the Q2 survivor/load facts."""
    mn = 27
    for c in pure3_choices():
        mn = min(mn, len(surviving_fibers(*c)))
    # For every surviving set, compare the closed-form worst load to exhaustive
    # enumeration over all (c1,c2,c3).
    max_load_ok = True
    for c in pure3_choices():
        S = surviving_fibers(*c)
        brute = 0
        for d in pure3_choices():
            load = sum(
                1
                + (r % 3 == d[0])
                + (r % 9 == d[1])
                + (r == d[2])
                for r in S
            )
            brute = max(brute, load)
        if worst_total_load(S) != brute:
            max_load_ok = False
    return {
        "min_survivors": mn,
        "closed_form_matches_bruteforce": max_load_ok,
        "min_is_14": mn == 14,
    }


__all__ = [
    "min_surviving_fibers",
    "pure3_choices",
    "surviving_fibers",
    "verify_pure3_bruteforce",
    "worst_total_load",
]
