from m52_a4_special_coordinate_limits import (
    A4_FIVE_EXPECTED_ETA,
    A4_SEVEN_EXPECTED_ETA,
    a4_five_limit_certificate,
    a4_seven_limit_certificate,
)


def test_m52_a4_five_infinite_baseline():
    out = a4_five_limit_certificate()
    assert out["verified"]
    assert out["state_count"] == 5**6 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["summed_goodness_margin"] == A4_FIVE_EXPECTED_ETA > 0


def test_m52_a4_seven_infinite_baseline():
    out = a4_seven_limit_certificate()
    assert out["verified"]
    assert out["state_count"] == 5**6 * 2**9
    assert out["floor_slack_scaled"] > 0
    assert out["summed_goodness_margin"] == A4_SEVEN_EXPECTED_ETA > 0
