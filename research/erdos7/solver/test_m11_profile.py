"""Tests for the Milestone 11 sound head/tail abstraction (O0/O1)."""

from itertools import product

from covering import divisors
from full_bound import deficiency_bound
from m10_profile import head_signature_counts, max_top_coverage
from m11_profile import (
    abstract_noncovering_certificate,
    head_capacity_from_counts,
    head_envelope,
    pareto_heads,
    representative_U,
)


def _realizable_U(p: int, a: int, M: int):
    L = p ** (a - 1) * M
    lower_divs = [d for d in divisors(L) if d > 1]
    ranges = [list(range(-1, d)) for d in lower_divs]
    seen = set()
    for choice in product(*ranges):
        covered = set()
        for d, r in zip(lower_divs, choice):
            if r < 0:
                continue
            for x in range(r, L, d):
                covered.add(x)
        U = frozenset(x for x in range(L) if x not in covered)
        if U not in seen:
            seen.add(U)
            yield set(U)


def test_sound_envelope_bounds_every_realizable_state():
    p, a, M = 3, 2, 4
    H = [1]
    all_es = divisors(M)
    for U in _realizable_U(p, a, M):
        if not U:
            continue
        counts = head_signature_counts(p, a, H, U)
        size = len(U)
        env = head_envelope(p, a, M, H, counts, size)
        true = max_top_coverage(p, a, M, U, all_es)
        assert env >= true


def test_o0_witness_cell_is_killed_by_the_envelope():
    p, a, M = 3, 2, 4
    H = [1]
    counts = {1: 1, 2: 1, 5: 1}
    size = 3
    env = head_envelope(p, a, M, H, counts, size)
    # C_H = 2 (one top modulus 9 can cover one lift of two bases mod 3), tail
    # = min(2,3)+min(1,3) = 3, so the envelope is 5 < p*|U| = 9.
    assert env == 5
    assert env < p * size


def test_head_capacity_is_a_function_of_the_histogram():
    p, a, M = 3, 2, 4
    H = [1, 2]
    counts = {0: 1, 3: 1, 6: 1}
    U = representative_U(p, a, M, H, counts)
    assert head_capacity_from_counts(p, a, M, H, counts) == max_top_coverage(
        p, a, M, U, H
    )


def test_seed_arithmetic_and_near_full_heads():
    cases = [
        (3, 3, 425425, 3828825, 109072),
        (5, 2, 459459, 2297295, 62067),
    ]
    for p, a, M, L, expected_delta in cases:
        assert deficiency_bound(L) == expected_delta
        heads = pareto_heads(p, a, M)
        # The near-full head is the largest divisor below M.
        near_full = [r for r in heads if r[3] == 24192]
        assert len(near_full) == 1
        expected_D0 = M // 5 if p == 3 else M // 3
        assert near_full[0][0] == expected_D0


def test_lossy_abstraction_kills_small_odd_noncovering_instance():
    # N = 3^2 * 5 = 45, decomposition p=3, a=2, M=5, L=15.  The single-head
    # abstraction H={1} proves every realizable lower state non-coverable.
    cert = abstract_noncovering_certificate(3, 2, 5, [1])
    assert cert["all_killed"] is True
    assert cert["witness"] is None
