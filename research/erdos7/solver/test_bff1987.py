"""Tests for the audited BFF 1987 forest-method reconstruction."""

from fractions import Fraction
from itertools import combinations

from bff1987 import (
    bff_bound,
    bff_g1,
    edge_weight,
    forest_union_bound,
    is_forest,
    kneser_edges,
    kneser_vertices,
    max_weight_spanning_tree,
    verify_spanning_tree,
    worst_case_params,
)


def _union(sets):
    out = set()
    for s in sets:
        out |= s
    return out


def test_forest_lemma_bruteforce():
    # The forest inequality |U S_v| <= sum |S_v| - sum_{edges} |S_u n S_v|.
    universe = {0, 1, 2, 3}
    # A path on 4 vertices (a forest).
    edges = [(0, 1), (1, 2), (2, 3)]
    for r0 in range(1 << 4):
        for r1 in range(1 << 4):
            for r2 in range(1 << 4):
                for r3 in range(1 << 4):
                    sets = [
                        {i for i in universe if (r0 >> i) & 1},
                        {i for i in universe if (r1 >> i) & 1},
                        {i for i in universe if (r2 >> i) & 1},
                        {i for i in universe if (r3 >> i) & 1},
                    ]
                    sizes = {v: Fraction(len(sets[v])) for v in range(4)}
                    overlaps = {
                        (u, v): Fraction(len(sets[u] & sets[v])) for u, v in edges
                    }
                    bound = forest_union_bound(sizes, overlaps)
                    assert len(_union(sets)) <= bound


def test_is_forest():
    assert is_forest(4, [(0, 1), (1, 2), (2, 3)])
    assert not is_forest(3, [(0, 1), (1, 2), (2, 0)])


def test_kneser_graph_counts():
    assert len(kneser_vertices(5)) == 10
    assert len(kneser_edges(5)) == 15
    assert len(kneser_vertices(6)) == 15
    assert len(kneser_edges(6)) == 45


def test_max_spanning_tree_is_forest_of_right_size():
    for n, primes in [(5, [3, 5, 7, 11, 13]), (6, [3, 5, 7, 11, 13, 17])]:
        w, z = worst_case_params(primes)
        edges, weight = max_weight_spanning_tree(n, z)
        assert len(edges) == len(kneser_vertices(n)) - 1
        ok, recomputed = verify_spanning_tree(n, edges, z)
        assert ok
        assert recomputed == weight


def test_worst_case_params_satisfy_domain():
    w, z = worst_case_params([3, 5, 7, 11, 13])
    assert w > 0 and all(z[i] > 0 for i in range(1, 6))
    assert w >= 3 * z[1]
    assert z[2] < 1 and z[3] < 1
    assert z[4] < Fraction(1, 3) and z[5] < Fraction(1, 3)


def test_g1_matches_1986_f_in_the_z1_zero_limit():
    # With (w, z_2, ..., z_n) = (x_1, ..., x_n), g1 = f(x) - (w - z_1) * sum z_i,
    # where f is the 1986 polynomial f(x) = prod(1+x_i) - sum x_i.
    w, z = worst_case_params([3, 5, 7])
    f = (1 + w) * (1 + z[2]) * (1 + z[3]) - w - z[2] - z[3]
    assert bff_g1(w, z) == f - (w - z[1]) * (z[2] + z[3])


def test_bff_bound_reproduces_omega_ge_6():
    # The reconstructed necessary condition g >= 2 fails for every odd support
    # with at most 5 primes, and holds for the smallest 6-prime support.
    assert bff_bound([3, 5, 7, 11]) < 2
    assert bff_bound([3, 5, 7, 11, 13]) < 2
    assert bff_bound([3, 5, 7, 11, 13, 17]) > 2


def test_edge_weight_is_product_over_union():
    z = {1: Fraction(1, 3), 2: Fraction(1, 2), 3: Fraction(1, 4), 4: Fraction(1, 8)}
    assert edge_weight((1, 2), (3, 4), z) == z[1] * z[2] * z[3] * z[4]
