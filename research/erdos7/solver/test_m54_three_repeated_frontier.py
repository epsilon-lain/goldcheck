from m54_three_repeated_frontier import (
    MINIMAL_FRONTIER,
    P332,
    P3222,
    P422,
    frontier_audit,
    minimal_frontier_dominator,
    profile_closed_after_m53,
)


def test_m54_two_repeated_coordinates_never_reach_frontier():
    assert profile_closed_after_m53((100, 100, 1, 1, 1, 1))
    assert profile_closed_after_m53((17, 2, 1, 1, 1, 1))


def test_m54_exact_three_profile_frontier():
    out = frontier_audit()
    assert out["verified"]
    assert out["frontier_size"] == 3
    assert MINIMAL_FRONTIER == (P422, P332, P3222)
    for p in MINIMAL_FRONTIER:
        assert minimal_frontier_dominator(p) == p
