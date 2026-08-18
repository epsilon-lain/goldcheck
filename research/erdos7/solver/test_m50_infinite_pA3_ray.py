from m50_infinite_pA3_ray import (
    EXPECTED_LIMIT_SURVIVORS,
    TEMPLATES_05,
    TEMPLATES_07,
    TEMPLATES_35,
    anchor_audit,
    limit_placement_scan,
    propagated_gap,
    ray_audit,
)


def test_m50_infinite_exponent_direct_reduction():
    out = limit_placement_scan()
    assert out["verified"]
    assert out["placement_count"] == 30
    assert out["limit_survivors"] == EXPECTED_LIMIT_SURVIVORS
    assert out["max_killed_R"] < 1
    assert anchor_audit()["verified"]
    assert len(TEMPLATES_05) + len(TEMPLATES_07) + len(TEMPLATES_35) == 22


def test_m50_recurrence_and_direct_limit_certificates():
    assert propagated_gap(6) > 0
    assert propagated_gap(20) > propagated_gap(6)
    assert propagated_gap(6, cube_on_7=True) > 0
    assert propagated_gap(20, cube_on_7=True) > propagated_gap(6, cube_on_7=True)
    out = ray_audit()
    assert out["verified"]
    assert out["all_ray_numbers_noncovering"]
