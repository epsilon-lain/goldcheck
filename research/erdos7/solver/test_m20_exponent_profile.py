"""Regression tests for M20 exponent-profile exclusion."""
from fractions import Fraction
from m20_exponent_profile import (
    CANONICAL_OFFBASE_R,
    NONCANONICAL_MAX_ASSIGNMENT,
    NONCANONICAL_MAX_R,
    PROFILE_DERIVATIVE_GAP,
    assignment_scan,
    exponent_profile_audit,
    prime_power_x,
    profile_direct_bound,
    profile_monotonicity_derivative_lower_bound,
    proof_branch,
)

def test_m20_rank_bounds_and_derivative_gap_are_exact():
    assert prime_power_x(3,4)==Fraction(40,81)
    assert prime_power_x(5,4)==Fraction(156,625)
    assert profile_monotonicity_derivative_lower_bound()==PROFILE_DERIVATIVE_GAP
    assert PROFILE_DERIVATIVE_GAP==Fraction(719,1440)>0

def test_m20_all_30_exponent_placements_are_scanned():
    result=assignment_scan()
    assert result["assignment_count"]==30
    assert result["noncanonical_max_assignment"]==NONCANONICAL_MAX_ASSIGNMENT
    assert NONCANONICAL_MAX_ASSIGNMENT==(4,1,2,1,1,1)
    assert result["noncanonical_max_R"]==NONCANONICAL_MAX_R
    assert NONCANONICAL_MAX_R==Fraction(16047137,16081065)<1
    assert 1-NONCANONICAL_MAX_R==Fraction(33928,16081065)

def test_m20_canonical_offbase_anchor_is_exact():
    assert CANONICAL_OFFBASE_R==Fraction(54428893,61108047)<1
    assert 1-CANONICAL_OFFBASE_R==Fraction(6679154,61108047)
    assert profile_direct_bound((3,7,11,13,17,19),(4,2,1,1,1,1))==CANONICAL_OFFBASE_R

def test_m20_three_proof_branches():
    assert proof_branch((3,5,7,11,13,17),(4,2,1,1,1,1))=="M19-four-parameter"
    assert proof_branch((3,5,7,11,13,17),(4,1,2,1,1,1))=="McNew-Setty-noncanonical-placement"
    assert proof_branch((3,7,11,13,17,19),(4,2,1,1,1,1))=="McNew-Setty-canonical-offbase"
    # Unsorted input: exponents remain attached to their primes.  After sorting
    # this is (3,7,11,13,17,19) with placement (4,1,2,1,1,1).
    assert proof_branch((19,3,13,7,11,17),(1,4,1,1,2,1))=="McNew-Setty-noncanonical-placement"

def test_m20_profile_audit():
    result=exponent_profile_audit()
    assert result["profile"]==(4,2,1,1,1,1)
    assert result["all_odd_six_prime_numbers_with_profile_noncovering"] is True
