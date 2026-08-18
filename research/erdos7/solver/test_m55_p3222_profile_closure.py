from m55_p3222_profile_closure import (
    PROFILE,
    SURVIVING_PLACEMENTS,
    placement_scan,
    proof_branch,
    reference_certificate,
    theorem_audit,
)


def test_m55_placement_scan():
    out = placement_scan()
    assert out["verified"]
    assert out["assignment_count"] == 60
    assert out["directly_killed_placement_count"] == 54
    assert len(out["surviving_placements"]) == 6


def test_m55_reference_certificates():
    for exponents in SURVIVING_PLACEMENTS:
        out = reference_certificate(exponents)
        assert out["summed_rho_margin"] > 0
        assert out["proper_non5_min"] > 0
        assert out["full_non5_min"] > 0
        assert out["verified"]


def test_m55_profile_theorem_audit():
    out = theorem_audit()
    assert out["profile"] == PROFILE
    assert out["reference_certificate_count"] == 6
    assert out["minimum_reference_margin"] > 0
    assert out["all_odd_six_prime_numbers_with_profile_noncovering"]
