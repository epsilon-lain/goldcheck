from m46_frontier_after_ray import (
    MINIMAL_FRONTIER,
    frontier_audit,
    minimal_frontier_dominator,
    profile_closed_after_m45,
)


def test_m46_former_A2_branch_is_gone():
    for A in (6, 7, 20, 100):
        assert profile_closed_after_m45((A, 2, 1, 1, 1, 1))


def test_m46_exact_four_profile_frontier():
    out = frontier_audit()
    assert out["verified"]
    assert out["frontier_size"] == 4 == len(MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p
