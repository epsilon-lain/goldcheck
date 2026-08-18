from m67_frontier_after_m66 import (
    MINIMAL_FRONTIER,P522,P432,P4222,P333,P3322,
    frontier_audit,minimal_frontier_dominator,profile_closed_after_m66,
)


def test_m67_frontier_audit():
    out=frontier_audit()
    assert out["verified"]
    assert out["frontier_size"]==5
    assert out["minimal_frontier"]==(P522,P432,P4222,P333,P3322)


def test_m67_frontier_points_are_open_and_minimal():
    for p in MINIMAL_FRONTIER:
        assert not profile_closed_after_m66(p)
        assert minimal_frontier_dominator(p)==p
