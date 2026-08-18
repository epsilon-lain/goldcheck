from m59_frontier_after_p332 import (
    MINIMAL_FRONTIER,
    P32222,
    P3322,
    P333,
    P422,
    frontier_audit,
    minimal_frontier_dominator,
    profile_closed_after_m58,
)


def test_m59_frontier_antichain():
    out = frontier_audit()
    assert out["verified"]
    assert out["minimal_frontier"] == (P422, P333, P3322, P32222)
    assert out["frontier_size"] == 4


def test_m59_m22_regression_and_boundaries():
    assert profile_closed_after_m58((2,2,2,2,2,2))
    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P333) == P333
    assert minimal_frontier_dominator(P3322) == P3322
    assert minimal_frontier_dominator(P32222) == P32222
