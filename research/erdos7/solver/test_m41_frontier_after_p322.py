from m41_frontier_after_p322 import (
    MINIMAL_FRONTIER,
    P3222,
    P332,
    P422,
    frontier_audit,
    minimal_frontier_dominator,
)
from m38_p52_profile_closure import P53, P62


def test_m41_frontier_antichain():
    out = frontier_audit()
    assert out["verified"]
    assert out["minimal_frontier"] == (P62, P53, P422, P332, P3222)
    assert len(MINIMAL_FRONTIER) == 5


def test_m41_boundary_directions():
    assert minimal_frontier_dominator((6,2,1,1,1,1)) == P62
    assert minimal_frontier_dominator((5,3,1,1,1,1)) == P53
    assert minimal_frontier_dominator((4,2,2,1,1,1)) == P422
    assert minimal_frontier_dominator((3,3,2,1,1,1)) == P332
    assert minimal_frontier_dominator((3,2,2,2,1,1)) == P3222
