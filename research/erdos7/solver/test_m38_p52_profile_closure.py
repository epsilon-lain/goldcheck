from m26_minimal_frontier import P52, P322
from m38_p52_profile_closure import (
    MINIMAL_FRONTIER,
    P53,
    P62,
    frontier_audit,
    minimal_frontier_dominator,
    p52_seed_closure_audit,
    profile_closed_after_m37,
)


def test_all_seven_p52_seeds_are_accounted_for():
    out = p52_seed_closure_audit()
    assert out["profile"] == P52
    assert out["m26_seed_count"] == 7
    assert out["m35_lifted_count"] == 5
    assert out["all_m26_seeds_excluded"]


def test_new_minimal_exponent_frontier_is_three_way():
    out = frontier_audit()
    assert out["verified"]
    assert out["minimal_frontier"] == MINIMAL_FRONTIER == (P62, P53, P322)
    assert profile_closed_after_m37(P52)
    assert minimal_frontier_dominator((7, 2, 1, 1, 1, 1)) == P62
    assert minimal_frontier_dominator((5, 7, 1, 1, 1, 1)) == P53
    assert minimal_frontier_dominator((3, 2, 2, 1, 1, 1)) == P322
