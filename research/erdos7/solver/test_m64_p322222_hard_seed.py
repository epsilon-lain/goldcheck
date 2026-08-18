from m64_p322222_hard_seed import (
    C, EXPECTED_ETA, EXPECTED_FLOOR_MIN, EXPECTED_STATE_COUNT, N,
    certificate_audit, feature_global_cost, pointwise_exact,
    profile_closure_audit, special_global_cost,
)


def test_m64_recorded_fast_verifier_certificate():
    out = certificate_audit()
    assert out["N"] == N == 3**3*5**2*7**2*11**2*13**2*17**2
    assert out["state_count"] == EXPECTED_STATE_COUNT == 134_217_728
    assert out["floor_min_scaled"] == EXPECTED_FLOOR_MIN
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C
    assert out["summed_rho_margin"] == EXPECTED_ETA > 0
    assert special_global_cost() > 0
    assert feature_global_cost() > 0


def test_m64_profile_closure():
    out = profile_closure_audit()
    assert out["verified"]
    assert out["all_odd_six_prime_numbers_with_profile_noncovering"]
