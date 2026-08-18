from fractions import Fraction

from m30_centered_moments import factorial_spike_cap
from m36_a5_exceptional_goodness import (
    C,
    EXPECTED_GLOBAL_MARGIN,
    EXPECTED_STATE_COUNT,
    N,
    factorial_global_cost,
    pointwise_goodness_certificate,
    seed_certificate,
    special_global_cost,
    special_point_min,
)


def test_a5_factorial_caps_used_by_m36():
    assert factorial_spike_cap(5, 1) == 121
    assert factorial_spike_cap(5, 2) == 58
    assert tuple(factorial_spike_cap(5, t) for t in range(1, 6)) == (
        121, 58, 24, 7, 1
    )


def test_m36_pointwise_integer_certificate():
    out = pointwise_goodness_certificate()
    assert out["verified"]
    assert out["state_count"] == EXPECTED_STATE_COUNT == 23_887_872
    assert out["floor_min"] > C
    assert out["floor_slack_scaled"] > 0
    assert out["exact_argmin_value"] > C


def test_m36_global_goodness_margin():
    out = seed_certificate()
    assert out["N"] == N == 3**5 * 5 * 7**2 * 11 * 13 * 17
    assert special_point_min() > 0
    assert special_global_cost() > 0
    assert factorial_global_cost() > 0
    assert out["summed_goodness_margin"] == EXPECTED_GLOBAL_MARGIN > 0
    assert out["noncovering_certified"]
