from m37_p17_factorial_lift import (
    C,
    EXPECTED_LIFT_GAP,
    EXPECTED_SUMMED_RHO_MARGIN,
    N4,
    N5,
    factorial_global_cost,
    pointwise_certificate,
    seed_certificate,
    sigma_over_M,
    special_global_cost,
)


def test_m37_pointwise_factorial_certificate():
    out = pointwise_certificate()
    assert out["verified"]
    assert out["state_count"] == 8_000_000
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C


def test_m37_quantitative_margin_and_lift():
    out = seed_certificate()
    assert out["N4"] == N4 == 3**4 * 5**2 * 7 * 11 * 13 * 17
    assert out["N5"] == N5 == 3**5 * 5**2 * 7 * 11 * 13 * 17
    assert special_global_cost() > 0
    assert factorial_global_cost() > 0
    assert out["summed_rho_margin"] == EXPECTED_SUMMED_RHO_MARGIN > 0
    assert sigma_over_M() > 0
    assert out["normalized_lift_gap"] == EXPECTED_LIFT_GAP > 0
    assert out["deficiency_lower_bound_N5"] > 0
    assert out["noncovering_certified"]
