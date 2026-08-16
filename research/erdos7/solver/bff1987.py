"""Audited reconstruction of Berger--Felzenbaum--Fraenkel (1987), ``II``.

Source audited directly: Acta Arith. 48 (1987) 73--79, DOI 10.4064/aa-48-1-73-79
(scanned PDF ``https://matwbn.icm.edu.pl/ksiazki/aa/aa48/aa4816.pdf``, read via
OCR).  The paper's new necessary condition is ``g(w, z) >= 2`` for an
incongruent covering system with odd moduli, where the polynomial is obtained
from the direct product-set union bound by subtracting a *forest* correction.

This module contains:

1. the forest lemma (proved in ``NOTES.md``);
2. the Kneser-graph / 2-subset forest engine, with an exact max-weight spanning
   tree and an independent acyclicity/weight verifier;
3. the reconstructed polynomial ``g = g1 - F`` and the monotonicity worst-case
   parameter values, which reproduce the published ``omega(N) >= 6`` result.

Everything is exact rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


# ---------------------------------------------------------------------------
# 1. The forest lemma
# ---------------------------------------------------------------------------

def is_forest(num_vertices: int, edges: list[tuple[int, int]]) -> bool:
    """Return True when ``edges`` form an acyclic graph on ``0..num_vertices-1``.

    Uses union--find: an edge joining two already-connected vertices would close
    a cycle.
    """
    parent = list(range(num_vertices))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        if not (0 <= u < num_vertices and 0 <= v < num_vertices):
            return False
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def forest_union_bound(
    sizes: dict[int, Fraction], edge_overlaps: dict[tuple[int, int], Fraction]
) -> Fraction:
    """The forest upper bound ``sum |S_v| - sum_{uv in E} |S_u ∩ S_v|``.

    For a forest ``G`` and any family of sets ``{S_v}``,
    ``|∪_v S_v| <= sum_v |S_v| - sum_{uv in E(G)} |S_u ∩ S_v|``.  ``edge_overlaps``
    stores each undirected edge exactly once, with ``(min, max)`` keys.
    """
    return sum(sizes.values(), Fraction(0)) - sum(
        edge_overlaps.values(), Fraction(0)
    )


# ---------------------------------------------------------------------------
# 2. The Kneser-graph forest engine
# ---------------------------------------------------------------------------

def kneser_vertices(n: int) -> list[tuple[int, ...]]:
    """All 2-subsets of ``{1, ..., n}`` (the vertices of ``KG(n, 2)``)."""
    return [tuple(c) for c in combinations(range(1, n + 1), 2)]


def kneser_edges(n: int) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """All disjoint pairs of 2-subsets (the edges of ``KG(n, 2)``)."""
    verts = kneser_vertices(n)
    out = []
    for i, u in enumerate(verts):
        su = set(u)
        for v in verts[i + 1:]:
            if su.isdisjoint(v):
                out.append((u, v))
    return out


def edge_weight(
    u: tuple[int, ...], v: tuple[int, ...], z: dict[int, Fraction]
) -> Fraction:
    """The certified pairwise-overlap weight ``prod_{i in u ∪ v} z_i``."""
    wt = Fraction(1)
    for i in set(u) | set(v):
        wt *= z[i]
    return wt


def max_weight_spanning_tree(
    n: int, z: dict[int, Fraction]
) -> tuple[list[tuple[tuple[int, ...], tuple[int, ...]]], Fraction]:
    """A maximum-weight spanning tree of ``KG(n, 2)`` (Kruskal, exact rationals)."""
    verts = kneser_vertices(n)
    index = {v: i for i, v in enumerate(verts)}
    weighted = sorted(
        ((edge_weight(u, v, z), u, v) for u, v in kneser_edges(n)),
        key=lambda t: t[0],
        reverse=True,
    )
    parent = list(range(len(verts)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    chosen: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    total = Fraction(0)
    for wt, u, v in weighted:
        ru, rv = find(index[u]), find(index[v])
        if ru != rv:
            parent[ru] = rv
            chosen.append((u, v))
            total += wt
    return chosen, total


def verify_spanning_tree(
    n: int,
    edges: list[tuple[tuple[int, ...], tuple[int, ...]]],
    z: dict[int, Fraction],
) -> tuple[bool, Fraction]:
    """Independently verify acyility, disjointness, and recompute the weight."""
    verts = kneser_vertices(n)
    index = {v: i for i, v in enumerate(verts)}
    ok = True
    for u, v in edges:
        if u not in index or v not in index or not set(u).isdisjoint(v):
            ok = False
    if not is_forest(len(verts), [(index[u], index[v]) for u, v in edges]):
        ok = False
    weight = sum((edge_weight(u, v, z) for u, v in edges), Fraction(0))
    return ok, weight


# ---------------------------------------------------------------------------
# 3. The reconstructed necessary polynomial
# ---------------------------------------------------------------------------

def worst_case_params(primes: list[int]) -> tuple[Fraction, dict[int, Fraction]]:
    """Monotonicity worst-case ``(w, z)`` for ``g`` over the BFF domain.

    With ``N = prod p_i^{s_i}``, ``g`` is increasing on the domain
    ``w, z_1, ..., z_n > 0;  w >= 3 z_1;  z_2, z_3 < 1;  z_4, z_5 < 1/3``, so its
    maximum is approached at the bounds (13)/(14) of the paper:

        w -> 1/(p_1 - 2),   z_1 -> 1/(p_1(p_1 - 2)),   z_i -> 1/(p_i - 3).
    """
    n = len(primes)
    w = Fraction(1, primes[0] - 2)
    z = {1: Fraction(1, primes[0] * (primes[0] - 2))}
    for i in range(2, n + 1):
        z[i] = Fraction(1, primes[i - 1] - 3)
    return w, z


def bff_g1(w: Fraction, z: dict[int, Fraction]) -> Fraction:
    """The direct (pre-forest) term ``g1(w, z)`` of the BFF polynomial."""
    n = len(z)
    prod = Fraction(1)
    for i in range(2, n + 1):
        prod *= 1 + z[i]
    s = sum((z[i] for i in range(2, n + 1)), Fraction(0))
    return (1 + w) * prod - w - (1 + w - z[1]) * s


def bff_forest_correction(
    n: int, z: dict[int, Fraction]
) -> tuple[list[tuple[tuple[int, ...], tuple[int, ...]]], Fraction]:
    """The maximum-weight forest (tree) correction for ``n`` prime coordinates."""
    return max_weight_spanning_tree(n, z)


def bff_bound(primes: list[int]) -> Fraction:
    """The reconstructed necessary-condition value ``g(w,z)`` at the worst case.

    ``g = g1 - F`` where ``F`` is the max-weight spanning-tree overlap sum on
    ``KG(n, 2)``.  ``g < 2`` rules out an odd incongruent cover with the given
    prime support.
    """
    w, z = worst_case_params(primes)
    n = len(primes)
    _, F = bff_forest_correction(n, z)
    return bff_g1(w, z) - F


__all__ = [
    "bff_bound",
    "bff_forest_correction",
    "bff_g1",
    "edge_weight",
    "forest_union_bound",
    "is_forest",
    "kneser_edges",
    "kneser_vertices",
    "max_weight_spanning_tree",
    "verify_spanning_tree",
    "worst_case_params",
]
