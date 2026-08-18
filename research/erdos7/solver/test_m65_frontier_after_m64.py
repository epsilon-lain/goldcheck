from m65_frontier_after_m64 import (
    MINIMAL_FRONTIER, P3322, P333, P422,
    frontier_audit, minimal_frontier_dominator, profile_closed_after_m64,
)


def test_m65_frontier_audit():
    out = frontier_audit()
    assert out["verified"]
    assert out["frontier_size"] == 3
    assert set(MINIMAL_FRONTIER) == {P422,P333,P3322}


def test_m65_p322222_branch_disappears():
    assert profile_closed_after_m64((3,2,2,2,2,2))
    assert minimal_frontier_dominator((4,2,2,2,2,2)) == P422
    assert minimal_frontier_dominator((3,3,2,2,2,2)) == P3322
