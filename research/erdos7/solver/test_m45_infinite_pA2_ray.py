from m45_infinite_pA2_ray import (
    EXPECTED_LIMIT_SURVIVORS,
    anchor_audit,
    limit_placement_scan,
    proof_branch,
    propagated_gap,
    ray_audit,
    universal_seed_templates,
)


def test_m45_infinite_exponent_direct_reduction():
    out = limit_placement_scan()
    assert out["verified"]
    assert out["placement_count"] == 30
    assert out["limit_survivors"] == EXPECTED_LIMIT_SURVIVORS
    assert out["max_killed_R"] < 1
    anchors = anchor_audit()
    assert anchors["verified"]


def test_m45_recurrence_closes_every_higher_exponent():
    assert propagated_gap(6) > 0
    assert propagated_gap(20) > propagated_gap(6)
    assert propagated_gap(6, exceptional=True) > 0
    assert propagated_gap(20, exceptional=True) > propagated_gap(6, exceptional=True)
    assert len(universal_seed_templates()) == 8
    out = ray_audit()
    assert out["verified"]
    assert out["all_ray_numbers_noncovering"]
