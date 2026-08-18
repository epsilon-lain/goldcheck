from m41_p322_canonical_weighted import (
    C,
    EXPECTED_ETA,
    canonical_seed_numbers,
    coordinate_box_minimum,
    factorial_global_cost,
    pointwise_certificate,
    reference_margin,
    seed_audit,
    special_global_cost,
)


def test_m41_weighted_pointwise_certificate():
    out = pointwise_certificate()
    assert out["verified"]
    assert out["state_count"] == 16 * 4**5 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C


def test_m41_completion_margin_and_seed_scaling():
    assert coordinate_box_minimum() > 0
    assert special_global_cost() > 0
    assert factorial_global_cost() > 0
    assert reference_margin() == EXPECTED_ETA > 0
    out = seed_audit()
    assert out["reference_eta"] == EXPECTED_ETA
    assert out["canonical_seed_count"] == 6
    assert len(canonical_seed_numbers()) == 6
    assert out["all_canonical_seeds_noncovering"]
