from m63_p322222_one_seed_reduction import (
    CANONICAL, HARD_SEED, PROFILE, SWAPPED,
    placement_scan, proof_branch, reduction_audit, reference_certificate,
)


def test_m63_placement_scan():
    out = placement_scan()
    assert out["verified"]
    assert out["assignment_count"] == 6
    assert out["directly_killed_placement_count"] == 4


def test_m63_reference_certificates():
    a2 = reference_certificate((3,5,7,11,13,17),SWAPPED)
    a3 = reference_certificate((3,5,7,11,13,19),CANONICAL)
    assert a2["summed_rho_margin"] > 0
    assert a3["summed_rho_margin"] > 0


def test_m63_reduction_to_one_seed():
    out = reduction_audit()
    assert out["profile"] == PROFILE
    assert out["hard_seed"] == HARD_SEED == 3**3*5**2*7**2*11**2*13**2*17**2
    assert out["all_other_profile_members_noncovering"]
    assert proof_branch((3,5,7,11,13,17),CANONICAL) == "M63-hard-seed"
