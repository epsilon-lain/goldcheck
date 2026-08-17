"""Regression tests for M22 universal direct-bound zones."""
from fractions import Fraction
from m22_universal_direct_zones import (
    ALL_EXPONENTS_TWO_GAP,
    ALL_EXPONENTS_TWO_R,
    LATE_HEAVY_GAP,
    LATE_HEAVY_WORST_R,
    ONE_REPEATED_LIMITS,
    UNIVERSAL_DERIVATIVE_GAP,
    all_exponents_at_most_two_audit,
    late_heavy_rank_audit,
    m22_audit,
    one_repeated_prime_audit,
    universal_monotonicity_gap,
)


def test_universal_monotonicity_is_exact_and_positive():
    assert universal_monotonicity_gap()==UNIVERSAL_DERIVATIVE_GAP
    assert UNIVERSAL_DERIVATIVE_GAP==Fraction(719,1440)>0


def test_all_exponents_at_most_two_anchor():
    result=all_exponents_at_most_two_audit()
    assert result["anchor_R"]==ALL_EXPONENTS_TWO_R
    assert ALL_EXPONENTS_TWO_R==Fraction(21635289362,21718371675)<1
    assert result["gap"]==ALL_EXPONENTS_TWO_GAP
    assert ALL_EXPONENTS_TWO_GAP==Fraction(83082313,21718371675)>0
    assert result["all_six_prime_exponents_le_2_noncovering"] is True


def test_arbitrary_single_repeated_prime_limits():
    result=one_repeated_prime_audit()
    assert result["position_limits"]==ONE_REPEATED_LIMITS
    assert max(ONE_REPEATED_LIMITS)==Fraction(90,91)<1
    assert result["arbitrary_single_repeated_exponent_noncovering"] is True


def test_rank_three_or_later_arbitrary_exponent_zone():
    result=late_heavy_rank_audit()
    assert result["worst_rank"]==3
    assert result["worst_R"]==LATE_HEAVY_WORST_R
    assert LATE_HEAVY_WORST_R==Fraction(1593178541,1595635470)<1
    assert result["gap"]==LATE_HEAVY_GAP
    assert LATE_HEAVY_GAP==Fraction(2456929,1595635470)>0
    assert result["arbitrary_exponent_on_rank_ge_3_with_others_le_2_noncovering"] is True


def test_m22_combined_audit():
    result=m22_audit()
    assert result["all_claims_exact"] is True
