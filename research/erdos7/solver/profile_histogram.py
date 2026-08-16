"""Milestone 7 (K5): lcm-bin histogram state and CRT joint intersections.

The richer profile state suggested by the brief is the *lcm-bin histogram*

    h_d(b; U) = |{ u in U : u ≡ b (mod d) }|.

It resolves the obstruction diagnosed in Milestone 6: individual overlapping
intersections have no positive unconditional lower bound, but a *joint* system
of projected top classes is either CRT-compatible (giving one lcm-bin count) or
has zero common base.  This module states and brute-force-validates that exact
formula on small instances.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def histogram(U: list[int], d: int) -> dict[int, int]:
    """``h_d(b; U)`` as a dict ``b -> count``."""
    out: dict[int, int] = {}
    for u in U:
        b = u % d
        out[b] = out.get(b, 0) + 1
    return out


def crt_combine(residues: list[tuple[int, int]]) -> tuple[int, int] | None:
    """Combine pairwise-congruence data to a single residue modulo the lcm.

    Returns ``(modulus, residue)`` or ``None`` when the system is incompatible.
    """
    if not residues:
        return 1, 0
    m, r = residues[0]
    for d, b in residues[1:]:
        g = gcd(m, d)
        if (r - b) % g != 0:
            return None
        # Solve m*t + r == b (mod d).
        # m*t == (b - r) (mod d); divide by g.
        mm, dd, rhs = m // g, d // g, (b - r) // g
        # mm is invertible mod dd (gcd(mm, dd) = 1).
        t = (rhs * pow(mm, -1, dd)) % dd
        r = r + m * t
        m = lcm(m, d)
        r %= m
    return m, r


def joint_intersection_count(U: list[int], residues: list[tuple[int, int]]) -> int:
    """Exact count of ``u in U`` satisfying ``u ≡ b (mod d)`` for every pair."""
    combined = crt_combine(residues)
    if combined is None:
        return 0
    m, r = combined
    return histogram(U, m).get(r, 0)


def brute_force_joint_count(U: list[int], residues: list[tuple[int, int]]) -> int:
    return sum(
        1
        for u in U
        if all(u % d == b for d, b in residues)
    )


def top_lifts_joint_count(
    U: list[int],
    p: int,
    a: int,
    lower_period: int,
    projected: list[tuple[int, int]],
) -> int:
    """Number of lifts ``u + t·lower_period`` (``u in U``, ``0 <= t < p``)
    covered jointly by full-``p``-adic classes whose projections are ``projected``.

    A base ``u`` contributes exactly one of its ``p`` lifts to a top class
    ``mod p^a e`` iff ``u ≡ r (mod p^{a-1} e)``; two lifts of the same base are
    always distinct modulo ``p^a e``.  Hence the joint count is the number of
    CRT-compatible bases, i.e. ``joint_intersection_count(U, projected)``.
    """
    return joint_intersection_count(U, projected)


__all__ = [
    "brute_force_joint_count",
    "crt_combine",
    "histogram",
    "joint_intersection_count",
    "lcm",
    "top_lifts_joint_count",
]
