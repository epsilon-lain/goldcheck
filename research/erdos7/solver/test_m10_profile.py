"""Tests for the Milestone 10 N0/N1/N3 primitives."""

import random

from covering import divisors
from m10_profile import (
    first_order_dual_status,
    head_signature_barrier_witness,
    head_signature_counts,
    max_top_coverage,
    tail_budget,
)


def test_first_order_dual_is_exactly_abundance():
    assert first_order_dual_status(3)["first_order_certificate_exists"] is True
    assert first_order_dual_status(4)["first_order_certificate_exists"] is True
    # 6 is not a covering number but sigma(6)=12=2*6, so the first-order dual
    # has zero gap and cannot certify it.
    assert first_order_dual_status(6)["first_order_certificate_exists"] is False
    # 12 is abundant (and is a covering number), so no certificate.
    assert first_order_dual_status(12)["first_order_certificate_exists"] is False
    assert first_order_dual_status(11_486_475)["first_order_certificate_exists"] is False


def test_head_tail_truncation_bound():
    p, a, M = 3, 2, 4
    rng = random.Random(0)
    all_es = divisors(M)
    for _ in range(200):
        U = {u for u in range(12) if rng.random() < 0.35}
        full = max_top_coverage(p, a, M, U, all_es)
        H = [e for e in all_es if rng.random() < 0.5]
        T = [e for e in all_es if e not in H]
        head = max_top_coverage(p, a, M, U, H)
        assert full <= head + tail_budget(p, a, M, U, T)


def test_head_signature_counts_are_sufficient():
    p, a, M = 3, 2, 4
    H = [1, 2]
    rng = random.Random(1)
    buckets: dict[tuple, list[set[int]]] = {}
    for _ in range(300):
        U = frozenset(u for u in range(12) if rng.random() < 0.4)
        counts = head_signature_counts(p, a, H, set(U))
        key = tuple(sorted(counts.items()))
        buckets.setdefault(key, []).append(set(U))
    for key, sets in buckets.items():
        vals = {max_top_coverage(p, a, M, U, H) for U in sets}
        assert len(vals) == 1


def test_head_signature_compression_barrier_is_realizable():
    w = head_signature_barrier_witness()
    assert w["len_U1"] == w["len_U2"] == 3
    assert w["head_counts_U1"] == w["head_counts_U2"]
    assert w["full_top_capacity_U1"] != w["full_top_capacity_U2"]
    assert w["is_barrier"] is True
    assert w["U1"] == [5, 10, 11]
    assert w["U2"] == [2, 5, 10]
