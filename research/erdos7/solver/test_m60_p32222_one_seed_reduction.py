from m60_p32222_one_seed_reduction import (
    HARD_SEED,
    PROFILE,
    SURVIVING_PLACEMENTS,
    placement_scan,
    reduction_audit,
    reference_certificate,
)
from m60_p32222_one_seed_reduction import EXPECTED


def test_m60_placement_scan():
    out = placement_scan()
    assert out["verified"]
    assert out["assignment_count"] == 30
    assert out["directly_killed_placement_count"] == 25
    assert len(out["surviving_placements"]) == 5


def test_m60_reference_certificates():
    for key in EXPECTED:
        out = reference_certificate(*key)
        assert out["summed_rho_margin"] > 0
        assert out["proper_non5_min"] > 0
        assert out["full_non5_min"] > 0


def test_m60_one_seed_reduction():
    out = reduction_audit()
    assert out["verified"]
    assert out["profile"] == PROFILE
    assert out["reference_certificate_count"] == 5
    assert out["hard_seed"] == HARD_SEED == 3**3 * 5**2 * 7**2 * 11**2 * 13**2 * 17
    assert out["all_other_profile_members_noncovering"]
