"""Regression tests for M34 minimal frontier after M33."""

from m34_frontier_after_m33 import (
    MINIMAL_FRONTIER,
    frontier_audit,
    minimal_frontier_dominator,
    profile_closed_after_m33,
)


def test_m34_minimal_antichain():
    assert MINIMAL_FRONTIER == (
        (5, 2, 1, 1, 1, 1),
        (3, 2, 2, 1, 1, 1),
    )
    assert minimal_frontier_dominator((8, 3, 1, 1, 1, 1)) == MINIMAL_FRONTIER[0]
    assert minimal_frontier_dominator((4, 4, 2, 1, 1, 1)) == MINIMAL_FRONTIER[1]


def test_m34_closed_regions():
    assert profile_closed_after_m33((4, 4, 1, 1, 1, 1))
    assert profile_closed_after_m33((2, 2, 2, 2, 2, 2))
    assert profile_closed_after_m33((99, 1, 1, 1, 1, 1))


def test_m34_seed_count():
    out = frontier_audit()
    assert out["seed_counts"] == {
        (5, 2, 1, 1, 1, 1): 7,
        (3, 2, 2, 1, 1, 1): 12,
    }
    assert out["total_direct_bound_seeds"] == 19
    assert out["verified"] is True
