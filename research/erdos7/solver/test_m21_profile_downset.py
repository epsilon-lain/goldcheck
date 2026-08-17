"""Regression tests for M21 profile down-set."""
from m21_profile_downset import (
    EXCLUDED_SORTED_PROFILES,
    dominant_m20_exponents,
    downset_proof_branch,
    profile_downset_audit,
)

def test_m21_exact_profile_list():
    assert EXCLUDED_SORTED_PROFILES==(
        (1,1,1,1,1,1),
        (2,1,1,1,1,1),
        (2,2,1,1,1,1),
        (3,1,1,1,1,1),
        (3,2,1,1,1,1),
        (4,1,1,1,1,1),
        (4,2,1,1,1,1),
    )

def test_m21_majorant_preserves_prime_assignment_and_divisibility():
    primes=(3,5,7,11,13,17)
    exponents=(1,3,1,2,1,1)
    major=dominant_m20_exponents(primes,exponents)
    assert major==(1,4,1,2,1,1)
    result=downset_proof_branch(primes,exponents)
    assert result["dominant_exponents"]==major
    assert result["N_tilde"]%result["N"]==0
    assert result["noncovering_by_divisibility"] is True

def test_m21_profile_downset_audit():
    result=profile_downset_audit()
    assert result["profile_count"]==7
    assert result["excluded_sorted_profiles"]==EXCLUDED_SORTED_PROFILES
    assert result["all_profiles_noncovering"] is True
