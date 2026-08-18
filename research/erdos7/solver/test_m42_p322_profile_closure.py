from m42_p322_profile_closure import (
    MINIMAL_FRONTIER,
    P332,
    P3222,
    P422,
    frontier_audit,
    minimal_frontier_dominator,
    p322_seed_closure_audit,
    profile_closed_after_m41,
)


def test_m42_all_twelve_p322_seeds_are_accounted_for():
    out = p322_seed_closure_audit()
    assert out["m26_seed_count"] == 12
    assert out["m40_exceptional_count"] == 6
    assert out["m41_canonical_count"] == 6
    assert out["all_m26_seeds_excluded"]


def test_m42_new_minimal_frontier():
    out = frontier_audit()
    assert out["verified"]
    assert len(MINIMAL_FRONTIER) == 5
    assert P422 in MINIMAL_FRONTIER
    assert P332 in MINIMAL_FRONTIER
    assert P3222 in MINIMAL_FRONTIER
    assert profile_closed_after_m41((3, 2, 2, 1, 1, 1))
    assert minimal_frontier_dominator(P422) == P422
    assert minimal_frontier_dominator(P332) == P332
    assert minimal_frontier_dominator(P3222) == P3222
