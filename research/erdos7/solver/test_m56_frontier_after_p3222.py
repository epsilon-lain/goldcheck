from m54_three_repeated_frontier import P422, P332, P3222
from m56_frontier_after_p3222 import (
    MINIMAL_FRONTIER,
    P32222,
    frontier_audit,
    minimal_frontier_dominator,
    profile_closed_after_m55,
)


def test_m56_frontier_antichain():
    out = frontier_audit()
    assert out["verified"]
    assert out["minimal_frontier"] == (P422, P332, P32222)
    assert out["frontier_size"] == 3


def test_m56_boundary_directions():
    assert profile_closed_after_m55(P3222)
    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P332) == P332
    assert minimal_frontier_dominator(P32222) == P32222
