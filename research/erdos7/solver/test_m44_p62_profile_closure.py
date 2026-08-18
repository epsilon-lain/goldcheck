from m44_p62_profile_closure import (
    C,
    EXPECTED_ETA,
    P62,
    canonical_lift_gap,
    exceptional_lift_gap,
    penalty_global_cost,
    pointwise_goodness_certificate,
    profile_audit,
    reference_margin,
    seed_accounting,
    special_global_cost,
)


def test_m44_reference_a5_goodness_certificate():
    out = pointwise_goodness_certificate()
    assert out["verified"]
    assert out["state_count"] == 6**6 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C


def test_m44_quantitative_lifts_and_seed_accounting():
    assert special_global_cost() > 0
    assert penalty_global_cost() > 0
    assert reference_margin() == EXPECTED_ETA > 0
    assert canonical_lift_gap() > 0
    assert exceptional_lift_gap() > 0
    accounting = seed_accounting()
    assert accounting["canonical_seed_count"] == 7
    assert accounting["exceptional_seed_count"] == 1
    assert accounting["all_eight_seeds_accounted_for"]

    out = profile_audit()
    assert out["profile"] == P62
    assert out["all_P62_numbers_noncovering"]
