"""Milestone 9 (M9.3): exact top-layer lift-coverage primitive.

The top layer of the deficiency recurrence has one modulus ``p^a e`` for each
``e | M``.  A top class ``r mod p^a e`` projects to a base class
``b = r mod p^{a-1}e`` and, on the ``p x p`` CRT box of one such base fiber,
is not a horizontal row but a *diagonal*: the lift color ``s`` of a base
``u = b + t p^{a-1}e`` is an affine function of ``t``.

This module states and machine-checks that exact diagonal law.  It is the exact
primitive from which any lcm-histogram profile optimizer must be built, and it
is the precise reason a base-count-only profile state cannot in general decide
top-layer coverability: it discards the diagonal coupling between the base
index ``t`` and the lift color ``s``.
"""

from __future__ import annotations

from math import gcd
from itertools import product

from covering import divisors


def lift_color(p: int, a: int, M: int, e: int, r: int, u: int) -> int | None:
    """The unique lift ``s`` of base ``u`` covered by ``r mod p^a e``, if any.

    Here ``N = p^a M``, ``gcd(p, M) = 1``, ``e | M``, and bases ``u`` live in
    ``Z/LZ`` with ``L = p^{a-1} M``.  Returns ``None`` when the class meets no
    lift of ``u``.

    The proof of the formula is the CRT computation in ``NOTES.md`` Section 20:
    writing ``d = p^{a-1}e``, ``b = r mod d``, ``c = (r-b)/d``, and
    ``t = (u-b)/d``, the congruence ``u + s p^{a-1}M == r (mod p^a e)`` is
    equivalent to ``t + s(M/e) == c (mod p)``.
    """
    d = p ** (a - 1) * e
    b = r % d
    if u % d != b:
        return None
    c = (r - b) // d
    t = (u - b) // d
    m = M // e
    # m is invertible mod p because gcd(p, M) = 1 and e | M.
    return ((c - t) % p) * pow(m % p, -1, p) % p


def top_class_lifts(
    p: int, a: int, M: int, e: int, r: int, U: set[int]
) -> set[tuple[int, int]]:
    """All ``(u, s)`` lifts covered by the top class ``r mod p^a e`` for ``u in U``."""
    out: set[tuple[int, int]] = set()
    for u in U:
        s = lift_color(p, a, M, e, r, u)
        if s is not None:
            out.add((u, s))
    return out


def top_layer_lifts(
    p: int, a: int, M: int, U: set[int], choices: dict[int, int]
) -> set[tuple[int, int]]:
    """Union of lifts covered by one chosen residue for each selected top modulus.

    ``choices`` maps ``e`` (a divisor of ``M``) to a residue ``r mod p^a e``.
    """
    out: set[tuple[int, int]] = set()
    for e, r in choices.items():
        if M % e != 0:
            raise ValueError(f"{e} does not divide {M}")
        out |= top_class_lifts(p, a, M, e, r, U)
    return out


def brute_top_class_lifts(
    p: int, a: int, M: int, e: int, r: int, U: set[int]
) -> set[tuple[int, int]]:
    """Independent brute-force verifier for :func:`top_class_lifts`."""
    L = p ** (a - 1) * M
    mod = p**a * e
    out: set[tuple[int, int]] = set()
    for u in U:
        for s in range(p):
            if (u + s * L) % mod == r:
                out.add((u, s))
    return out


def top_layer_covers_all(
    p: int, a: int, M: int, U: set[int], choices: dict[int, int]
) -> bool:
    """Whether the chosen top classes cover every ``p|U|`` lift of ``U``."""
    return top_layer_lifts(p, a, M, U, choices) == {
        (u, s) for u in U for s in range(p)
    }


def scalar_profile_vector(p: int, a: int, M: int, U: set[int]) -> tuple[int, ...]:
    """The Task-F1 scalar profile ``mu_{p^{a-1}e}(U)`` for every ``e | M``."""
    vec: list[int] = []
    for e in divisors(M):
        d = p ** (a - 1) * e
        bins: dict[int, int] = {}
        for u in U:
            b = u % d
            bins[b] = bins.get(b, 0) + 1
        vec.append(max(bins.values()) if bins else 0)
    return tuple(vec)


def top_layer_coverable_bruteforce(p: int, a: int, M: int, U: set[int]) -> bool:
    """Brute-force decide whether the top layer can cover all ``p|U|`` lifts.

    This is exponential and intended only for small test instances.
    """
    L = p ** (a - 1) * M
    target = {(u, s) for u in U for s in range(p)}
    candidates: list[list[int]] = []
    for e in divisors(M):
        mod = p**a * e
        good = []
        for r in range(mod):
            if any((u + s * L) % mod == r for u in U for s in range(p)):
                good.append(r)
        candidates.append(good)
    for choice in product(*candidates):
        cov: set[tuple[int, int]] = set()
        for e, r in zip(divisors(M), choice):
            cov |= top_class_lifts(p, a, M, e, r, U)
        if cov == target:
            return True
    return False


def scalar_profile_insufficient_witness() -> dict:
    """Explicit machine-checkable witness that the scalar profile is insufficient.

    For ``p=3, a=2, M=4`` (so ``L=12``), the two sets ``U1={0}`` and
    ``U2={0,1}`` have identical Task-F1 scalar profiles ``(1,1,1)``, yet the top
    layer covers all lifts of ``U1`` and cannot cover all lifts of ``U2``.
    """
    p, a, M = 3, 2, 4
    U1 = {0}
    U2 = {0, 1}
    v1 = scalar_profile_vector(p, a, M, U1)
    v2 = scalar_profile_vector(p, a, M, U2)
    c1 = top_layer_coverable_bruteforce(p, a, M, U1)
    c2 = top_layer_coverable_bruteforce(p, a, M, U2)
    return {
        "p": p,
        "a": a,
        "M": M,
        "U1": sorted(U1),
        "U2": sorted(U2),
        "profile_U1": v1,
        "profile_U2": v2,
        "U1_coverable": c1,
        "U2_coverable": c2,
        "is_insufficient_witness": v1 == v2 and c1 != c2,
    }


__all__ = [
    "brute_top_class_lifts",
    "lift_color",
    "scalar_profile_insufficient_witness",
    "scalar_profile_vector",
    "top_class_lifts",
    "top_layer_covers_all",
    "top_layer_coverable_bruteforce",
    "top_layer_lifts",
]
