"""Regression tests for M23 double-cube profile exclusion."""
from fractions import Fraction
from m23_double_cube_profile import (
    DIRECT_R29,
    DIRECT_THRESHOLD,
    EXPONENT_PROFILE,
    NONCANONICAL_MAX_ASSIGNMENT,
    NONCANONICAL_MAX_R,
    SMALL_P,
    affine_certificate,
    assignment_scan,
    direct_family_bound,
    m23_audit,
    proof_branch,
)


def test_m23_only_one_minimal_assignment_survives_direct_bound():
    result=assignment_scan()
    assert result["assignment_count"]==15
    assert result["noncanonical_max_assignment"]==NONCANONICAL_MAX_ASSIGNMENT
    assert NONCANONICAL_MAX_ASSIGNMENT==(3,1,3,1,1,1)
    assert result["noncanonical_max_R"]==NONCANONICAL_MAX_R
    assert NONCANONICAL_MAX_R==Fraction(37123796,37522485)<1


def test_m23_three_small_affine_certificates_have_positive_margin():
    expected={
        17:Fraction(795361761,21271250000),
        19:Fraction(58151681,679250000),
        23:Fraction(410035473,2616250000),
    }
    for P in SMALL_P:
        result=affine_certificate(P)
        assert result["margin"]==expected[P]>0
        assert result["non5_clique_min"]>0
        assert result["noncovering_certified"] is True


def test_m23_direct_tail_threshold_is_exact():
    assert DIRECT_THRESHOLD==Fraction(1933172,83467)
    assert 23<DIRECT_THRESHOLD<29
    assert direct_family_bound(29)==DIRECT_R29
    assert DIRECT_R29==Fraction(32495168,32657625)<1
    assert 1-DIRECT_R29==Fraction(162457,32657625)


def test_m23_all_proof_branches():
    assert proof_branch((3,5,7,11,13,17),EXPONENT_PROFILE)=="M23-affine"
    assert proof_branch((3,5,7,11,13,29),EXPONENT_PROFILE)=="McNew-Setty-P-tail"
    assert proof_branch((3,5,7,11,17,19),EXPONENT_PROFILE)=="McNew-Setty-simple-offfamily"
    assert proof_branch((3,7,11,13,17,19),EXPONENT_PROFILE)=="McNew-Setty-canonical-offbase"
    assert proof_branch((3,5,7,11,13,17),(3,1,3,1,1,1))=="McNew-Setty-noncanonical-placement"


def test_m23_complete_profile_audit():
    result=m23_audit()
    assert result["all_odd_six_prime_numbers_with_profile_noncovering"] is True
