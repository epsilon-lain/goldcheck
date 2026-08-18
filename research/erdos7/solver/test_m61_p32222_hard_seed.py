from m60_p32222_one_seed_reduction import PROFILE
from m61_p32222_hard_seed import (
    C,
    EXPECTED_ETA,
    EXPECTED_FLOOR_MIN,
    EXPECTED_STATE_COUNT,
    N,
    certificate_audit,
    profile_closure_audit,
)


def test_m61_exact_hard_seed_constants():
    out = certificate_audit()
    assert out["N"] == N == 3**3 * 5**2 * 7**2 * 11**2 * 13**2 * 17
    assert out["state_count"] == EXPECTED_STATE_COUNT == 33_554_432
    assert out["floor_min_scaled"] == EXPECTED_FLOOR_MIN
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C
    assert out["summed_rho_margin"] == EXPECTED_ETA > 0
    assert out["proper_non5_min"] > 0
    assert out["full_non5_min"] > 0
    assert out["noncovering_certified"]


def test_m61_complete_p32222_profile_closure():
    out = profile_closure_audit()
    assert out["profile"] == PROFILE
    assert out["hard_seed"] == N
    assert out["all_other_profile_members_noncovering"]
    assert out["all_odd_six_prime_numbers_with_profile_noncovering"]
    assert out["verified"]
