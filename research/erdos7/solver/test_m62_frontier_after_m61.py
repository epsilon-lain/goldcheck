from m62_frontier_after_m61 import (
    MINIMAL_FRONTIER, P322222, frontier_audit,
    minimal_frontier_dominator, profile_closed_after_m61,
)


def test_m62_frontier_audit():
    out = frontier_audit()
    assert out["verified"]
    assert out["frontier_size"] == 4
    assert P322222 in MINIMAL_FRONTIER


def test_m62_closed_and_open_boundary():
    assert profile_closed_after_m61((3,2,2,2,2,1))
    assert not profile_closed_after_m61((3,2,2,2,2,2))
    assert minimal_frontier_dominator((3,2,2,2,2,2)) == P322222
