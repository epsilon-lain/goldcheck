from m51_frontier_after_A3_ray import (
    MINIMAL_FRONTIER,
    frontier_audit,
    minimal_frontier_dominator,
    profile_closed_after_m50,
)


def test_m51_whole_A3_branch_is_closed():
    for A in (4, 5, 6, 10, 100):
        assert profile_closed_after_m50((A, 3, 1, 1, 1, 1))


def test_m51_exact_four_profile_frontier():
    out = frontier_audit()
    assert out["verified"]
    assert out["frontier_size"] == 4 == len(MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p
