"""Tests for the coefficient-certificate lemma and the omega6 dual certificate."""

from fractions import Fraction
from itertools import combinations
from pathlib import Path

from higher_overlap import (
    coefficient_certificate_bound,
    coefficient_certificate_premise,
    disjoint_pairs,
    g1_value,
    nonempty_subsets,
    pair_lower,
    verify_certificate,
    vertices,
    z_values,
)


CERT = Path(__file__).resolve().parent.parent / "certificates" / "omega6_overlap.json"


def _union(sets):
    out = set()
    for s in sets:
        out |= s
    return out


def test_coefficient_certificate_lemma_pointwise():
    # For every coefficient vector with valid premise, the bound dominates the
    # union size, on a small 3-set instance over a 3-element universe.
    universe = {0, 1, 2}
    all_sets = []
    for r in range(1 << 3):
        all_sets.append({i for i in universe if (r >> i) & 1})
    n = 3
    # A few hand-picked coefficient vectors whose premise holds.
    alphas = [
        {frozenset({i}): Fraction(1) for i in range(n)},
        {frozenset({0}): Fraction(1), frozenset({1}): Fraction(1),
         frozenset({2}): Fraction(1), frozenset({0, 1}): Fraction(-1)},
        {frozenset({0}): Fraction(1), frozenset({1}): Fraction(1),
         frozenset({2}): Fraction(1), frozenset({0, 1}): Fraction(-1),
         frozenset({0, 2}): Fraction(-1)},
    ]
    for alpha in alphas:
        assert coefficient_certificate_premise(n, alpha)
        for r0 in range(1 << 3):
            for r1 in range(1 << 3):
                for r2 in range(1 << 3):
                    sets = [
                        {i for i in universe if (r0 >> i) & 1},
                        {i for i in universe if (r1 >> i) & 1},
                        {i for i in universe if (r2 >> i) & 1},
                    ]
                    bound = coefficient_certificate_bound(
                        [frozenset(s) for s in sets], alpha
                    )
                    assert len(_union(sets)) <= bound


def test_forest_special_case_recovers_bff():
    # alpha_v = 1, alpha_uv = -1 on a forest, all else 0, is a valid certificate.
    n = 4
    edges = [(0, 1), (1, 2), (2, 3)]
    alpha = {frozenset({i}): Fraction(1) for i in range(n)}
    for u, v in edges:
        alpha[frozenset({u, v})] = Fraction(-1)
    assert coefficient_certificate_premise(n, alpha)


def test_pair_lower_values():
    z = z_values(6, [3, 5, 7, 11, 13, 17])
    L = pair_lower(6, z)
    vs = vertices(6)
    assert len(L) == 45  # KG(6,2) has 45 edges
    for (i, j), val in L.items():
        u = set(vs[i]) | set(vs[j])
        expected = Fraction(1)
        for k in u:
            expected *= z[k]
        assert val == expected


def test_omega6_certificate_is_insufficient():
    import json

    cert = json.loads(CERT.read_text(encoding="utf-8"))
    result = verify_certificate(cert)
    assert result["nonneg"]
    assert result["pair_lower_ok"]
    assert result["dual_obj_matches_F_star"]
    assert result["g"] > 2
    assert result["residual_gap"] > 0

    g1 = g1_value([3, 5, 7, 11, 13, 17], z_values(6, [3, 5, 7, 11, 13, 17]))
    assert result["g1"] == g1
    assert result["g"] == g1 - Fraction(cert["F_star"])


def test_g1_matches_milestone4():
    z = z_values(6, [3, 5, 7, 11, 13, 17])
    g1 = g1_value([3, 5, 7, 11, 13, 17], z)
    assert g1 == Fraction(5989, 2688)
