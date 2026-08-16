"""Milestone 5: higher-order overlap certificate for the six-prime corner.

This module contains the two rigorous ingredients of the Milestone 5 brief:

1. the *coefficient-certificate lemma* (task I1), a pointwise-valid
   generalization of the forest inclusion--exclusion bound; and
2. an exact, machine-checkable **dual certificate** proving that the
   pair+triple overlap basis is insufficient at the extremal six-prime corner
   ``{3,5,7,11,13,17}``.

The dual certificate is emitted by ``certificates/omega6_overlap.json`` and is
verified here using only ``Fraction`` arithmetic (no floating point and no
external solver in the trusted path).
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. The coefficient-certificate lemma
# ---------------------------------------------------------------------------

def nonempty_subsets(n: int):
    """Yield every nonempty subset of ``{0, ..., n-1}`` as a frozenset."""
    for mask in range(1, 1 << n):
        yield frozenset(i for i in range(n) if (mask >> i) & 1)


def coefficient_certificate_premise(
    n: int, alpha: dict[frozenset[int], Fraction]
) -> bool:
    """Check ``sum_{empty != J <= T} alpha_J >= 1`` for every nonempty ``T``."""
    for T in nonempty_subsets(n):
        s = Fraction(0)
        for J, a in alpha.items():
            if J <= T:
                s += a
        if s < 1:
            return False
    return True


def coefficient_certificate_bound(sets: list[frozenset[int]], alpha) -> Fraction:
    """The certified upper bound ``sum_{empty != J <= V} alpha_J * |cap_{j in J} A_j|``."""
    n = len(sets)
    total = Fraction(0)
    for J, a in alpha.items():
        inter = None
        for j in J:
            inter = sets[j] if inter is None else (inter & sets[j])
        total += a * Fraction(len(inter))
    return total


# ---------------------------------------------------------------------------
# 2. The six-prime BFF overlap data
# ---------------------------------------------------------------------------

PRIMES_6 = [3, 5, 7, 11, 13, 17]


def z_values(n: int, primes: list[int]) -> dict[int, Fraction]:
    """Worst-case BFF parameters ``z_1, ..., z_n`` (see NOTES.md Section 13)."""
    z = {1: Fraction(1, primes[0] * (primes[0] - 2))}
    for i in range(2, n + 1):
        z[i] = Fraction(1, primes[i - 1] - 3)
    return z


def vertices(n: int) -> list[tuple[int, ...]]:
    """The 2-subsets of ``{1, ..., n}`` (the BFF vertex family)."""
    return [tuple(c) for c in combinations(range(1, n + 1), 2)]


def disjoint_pairs(n: int) -> list[tuple[int, int]]:
    """Vertex-index pairs whose two 2-subsets are disjoint (the ``KG(n,2)`` edges)."""
    vs = vertices(n)
    out = []
    for i in range(len(vs)):
        si = set(vs[i])
        for j in range(i + 1, len(vs)):
            if si.isdisjoint(vs[j]):
                out.append((i, j))
    return out


def pair_lower(n: int, z: dict[int, Fraction]) -> dict[tuple[int, int], Fraction]:
    """Exact lower bounds ``L_e`` for disjoint-pair intersections.

    For disjoint 2-subsets ``I, J`` the two product sets intersect in exactly
    ``prod_{i in I u J} z_i``.  Overlapping pairs have safe lower bound ``0`` and
    are therefore omitted (their multiplier is never useful).
    """
    vs = vertices(n)
    return {
        (i, j): _product_over_union(vs[i], vs[j], z)
        for i, j in disjoint_pairs(n)
    }


def triples(n: int) -> list[tuple[int, int, int]]:
    """All vertex-index triples (three 2-subsets)."""
    return list(combinations(range(len(vertices(n))), 3))


def quadruples(n: int) -> list[tuple[int, int, int, int]]:
    """All vertex-index quadruples (four 2-subsets)."""
    return list(combinations(range(len(vertices(n))), 4))


def triple_upper(n: int, z: dict[int, Fraction]) -> dict[tuple, Fraction]:
    """Certified upper bounds ``U_h = prod_{i in union} z_i`` for triples."""
    vs = vertices(n)
    return {
        t: _product_over_family([vs[i] for i in t], z)
        for t in triples(n)
    }


def quadruple_upper(n: int, z: dict[int, Fraction]) -> dict[tuple, Fraction]:
    """Certified upper bounds ``U_q = prod_{i in union} z_i`` for quadruples."""
    vs = vertices(n)
    return {
        q: _product_over_family([vs[i] for i in q], z)
        for q in quadruples(n)
    }


def _product_over_family(indices: list[tuple[int, ...]], z) -> Fraction:
    u = set()
    for idx in indices:
        u |= set(idx)
    wt = Fraction(1)
    for k in u:
        wt *= z[k]
    return wt


def intersection_oracle(indices: list[tuple[int, ...]], z) -> tuple[Fraction, Fraction]:
    """Return ``(L, U)`` certified bounds for ``|cap A_I|``.

    The BFF building block ``A_I`` is a product set whose ``i``-th coordinate is a
    single residue class when ``i in I`` (normalized factor ``z_i``) and is full
    otherwise.  Hence:

    * ``U = prod_{i in union} z_i`` is a certified upper bound (tight);
    * ``L = prod_{i in union} z_i`` is certified exactly when the index sets are
      pairwise disjoint (no shared coordinate can be split);
    * otherwise only the trivial ``L = 0`` is certified.
    """
    u = set()
    pairwise_disjoint = True
    for i, a in enumerate(indices):
        u |= set(a)
        for b in indices[i + 1:]:
            if set(a) & set(b):
                pairwise_disjoint = False
    U = Fraction(1)
    for k in u:
        U *= z[k]
    L = U if pairwise_disjoint else Fraction(0)
    return L, U


def _product_over_union(u: tuple[int, ...], v: tuple[int, ...], z) -> Fraction:
    wt = Fraction(1)
    for k in set(u) | set(v):
        wt *= z[k]
    return wt


def g1_value(primes: list[int], z: dict[int, Fraction]) -> Fraction:
    """The direct (pre-forest) term ``g1(w, z)`` at the worst-case bounds."""
    n = len(primes)
    w = Fraction(1, primes[0] - 2)
    prod = Fraction(1)
    for i in range(2, n + 1):
        prod *= 1 + z[i]
    s = sum((z[i] for i in range(2, n + 1)), Fraction(0))
    return (1 + w) * prod - w - (1 + w - z[1]) * s


# ---------------------------------------------------------------------------
# 3. Dual-certificate verification (pure rational arithmetic)
# ---------------------------------------------------------------------------

def load_certificate(path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def verify_certificate(cert: dict) -> dict:
    """Independently verify the omega6 dual certificate with ``Fraction`` only.

    Returns a dict of exact checks.  The certificate claims:

    * every dual weight ``d_T >= 0``;
    * for every disjoint pair ``e``, ``sum_{T containing e} d_T >= L_e``; and
    * the dual objective ``sum_T (|T|-1) d_T`` equals the stored ``F_star``.

    These imply ``max correction <= F_star``, hence ``g = g1 - F_star > 2``.
    """
    n = cert["n"]
    primes = cert["primes"]
    z = {int(k): Fraction(v) for k, v in cert["z"].items()}
    vs = vertices(n)
    vidx = {v: i for i, v in enumerate(vs)}

    L = pair_lower(n, z)

    entries = []
    for e in cert["dual_entries"]:
        T = frozenset(vidx[tuple(v)] for v in e["T"])
        entries.append((T, Fraction(e["d"])))

    nonneg = all(d >= 0 for _, d in entries)

    # For each disjoint pair e, sum of d_T over T containing e.
    covering = {pair: Fraction(0) for pair in L}
    for T, d in entries:
        for pair in L:
            if pair[0] in T and pair[1] in T:
                covering[pair] += d
    pair_ok = all(covering[pair] >= L[pair] for pair in L)

    dual_obj = sum(Fraction(len(T) - 1) * d for T, d in entries)
    F_star = Fraction(cert["F_star"])
    g1 = g1_value(primes, z)
    g = g1 - F_star

    return {
        "nonneg": nonneg,
        "pair_lower_ok": pair_ok,
        "dual_obj": dual_obj,
        "dual_obj_matches_F_star": dual_obj == F_star,
        "g1": g1,
        "g": g,
        "g_gt_2": g > 2,
        "residual_gap": g - 2,
    }


def verify_order4_certificate(cert: dict) -> dict:
    """Independently verify the order-4 (pair+triple+quadruple) dual certificate.

    The order-4 dual is ``min sum_T (|T|-1) d_T`` subject to, for all nonempty
    ``T``, ``d_T >= 0``, together with

        sum_{T containing e} d_T >= L_e      (disjoint pairs),
        sum_{T containing h} d_T <= U_h      (triples),
        sum_{T containing q} d_T <= U_q      (quadruples).
    """
    n = cert["n"]
    primes = cert["primes"]
    z = {int(k): Fraction(v) for k, v in cert["z"].items()}
    vs = vertices(n)
    vidx = {v: i for i, v in enumerate(vs)}

    L = pair_lower(n, z)
    U3 = triple_upper(n, z)
    U4 = quadruple_upper(n, z)

    entries = []
    for e in cert["dual_entries"]:
        T = frozenset(vidx[tuple(v)] for v in e["T"])
        entries.append((T, Fraction(e["d"])))

    nonneg = all(d >= 0 for _, d in entries)

    pair_sum = {p: Fraction(0) for p in L}
    tri_sum = {t: Fraction(0) for t in U3}
    quad_sum = {q: Fraction(0) for q in U4}
    for T, d in entries:
        for p in L:
            if p[0] in T and p[1] in T:
                pair_sum[p] += d
        for t in U3:
            if all(i in T for i in t):
                tri_sum[t] += d
        for q in U4:
            if all(i in T for i in q):
                quad_sum[q] += d

    pair_ok = all(pair_sum[p] >= L[p] for p in L)
    triple_ok = all(tri_sum[t] <= U3[t] for t in U3)
    quad_ok = all(quad_sum[q] <= U4[q] for q in U4)
    dual_obj = sum(Fraction(len(T) - 1) * d for T, d in entries)
    F_star = Fraction(cert["F_star"])
    g1 = g1_value(primes, z)
    g = g1 - F_star

    return {
        "nonneg": nonneg,
        "pair_lower_ok": pair_ok,
        "triple_upper_ok": triple_ok,
        "quadruple_upper_ok": quad_ok,
        "dual_obj": dual_obj,
        "dual_obj_matches_F_star": dual_obj == F_star,
        "g1": g1,
        "g": g,
        "g_gt_2": g > 2,
        "residual_gap": g - 2,
    }


__all__ = [
    "coefficient_certificate_bound",
    "coefficient_certificate_premise",
    "disjoint_pairs",
    "g1_value",
    "load_certificate",
    "intersection_oracle",
    "nonempty_subsets",
    "pair_lower",
    "quadruple_upper",
    "quadruples",
    "triple_upper",
    "triples",
    "verify_certificate",
    "verify_order4_certificate",
    "vertices",
    "z_values",
]
