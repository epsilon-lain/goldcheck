from m48_special_coordinate_limits import (
    A3_EXPECTED_ETA,
    A5_FIVE_EXPECTED_ETA,
    A5_SEVEN_EXPECTED_ETA,
    a3_five_limit_certificate,
    a5_five_limit_certificate,
    a5_seven_limit_certificate,
)


def test_m48_a3_five_infinite_baseline():
    out = a3_five_limit_certificate()
    assert out["verified"]
    assert out["special_limit"] == 1 / 4
    assert out["state_count"] == 4**6 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["summed_rho_margin"] == A3_EXPECTED_ETA > 0


def test_m48_a5_five_infinite_baseline():
    out = a5_five_limit_certificate()
    assert out["verified"]
    assert out["state_count"] == 6**6 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["summed_goodness_margin"] == A5_FIVE_EXPECTED_ETA > 0


def test_m48_a5_seven_infinite_baseline():
    out = a5_seven_limit_certificate()
    assert out["verified"]
    assert out["state_count"] == 6**6 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["summed_goodness_margin"] == A5_SEVEN_EXPECTED_ETA > 0
