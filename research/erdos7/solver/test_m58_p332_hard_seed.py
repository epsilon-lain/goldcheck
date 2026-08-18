from m57_p332_one_seed_reduction import PROFILE
from m58_p332_hard_seed import (
    C,
    EXPECTED_ETA,
    EXPECTED_FLOOR_MIN,
    EXPECTED_STATE_COUNT,
    N,
    certificate_audit,
    profile_closure_audit,
)


def test_m58_exact_certificate_constants():
    out = certificate_audit()
    assert out["N"] == N == 3**3 * 5**3 * 7**2 * 11 * 13 * 17
    assert out["state_count"] == EXPECTED_STATE_COUNT == 67_108_864
    assert out["floor_min_scaled"] == EXPECTED_FLOOR_MIN
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C
    assert out["summed_rho_margin"] == EXPECTED_ETA > 0
    assert out["proper_non5_min"] > 0
    assert out["full_non5_min"] > 0
    assert out["noncovering_certified"]


def test_m58_complete_p332_profile_closure():
    out = profile_closure_audit()
    assert out["profile"] == PROFILE
    assert out["hard_seed"] == N
    assert out["hard_seed_noncovering"]
    assert out["all_other_profile_members_noncovering"]
    assert out["all_odd_six_prime_numbers_with_profile_noncovering"]
    assert out["verified"]
