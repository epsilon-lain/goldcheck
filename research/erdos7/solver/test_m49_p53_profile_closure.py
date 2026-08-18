from m47_p53_direct_frontier import P53
from m49_p53_profile_closure import (
    MINIMAL_FRONTIER,
    frontier_audit,
    minimal_frontier_dominator,
    p53_seed_closure_audit,
    profile_closed_after_m49,
)


def test_m49_all_sixteen_p53_seeds_are_excluded():
    out = p53_seed_closure_audit()
    assert out["seed_count"] == 16
    assert out["all_m47_seeds_excluded"]
    assert sum(out["counts_by_placement"].values()) == 16


def test_m49_profile_closure_and_new_frontier():
    assert profile_closed_after_m49(P53)
    out = frontier_audit()
    assert out["verified"]
    assert out["frontier_size"] == 5 == len(MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p
