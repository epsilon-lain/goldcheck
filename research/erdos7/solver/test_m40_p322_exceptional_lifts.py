from m40_p322_exceptional_lifts import (
    C,
    EXPECTED_ETA,
    EXPECTED_LIFT_GAPS,
    exceptional_seed_numbers,
    factorial_global_cost,
    pointwise_certificate,
    reference_margin,
    seed_audit,
    special_global_cost,
)


def test_m40_pointwise_reference_certificate():
    out = pointwise_certificate()
    assert out["verified"]
    assert out["state_count"] == 4**6 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C


def test_m40_quantitative_margin_and_lifts():
    assert special_global_cost() > 0
    assert factorial_global_cost() > 0
    assert reference_margin() == EXPECTED_ETA > 0
    out = seed_audit()
    assert out["reference_eta"] == EXPECTED_ETA
    assert out["lift_gaps"] == EXPECTED_LIFT_GAPS
    assert all(g > 0 for g in EXPECTED_LIFT_GAPS.values())
    assert out["exceptional_seed_count"] == 6
    assert len(exceptional_seed_numbers()) == 6
    assert out["all_exceptional_seeds_noncovering"]
