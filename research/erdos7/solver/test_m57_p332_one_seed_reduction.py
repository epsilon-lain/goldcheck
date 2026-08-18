from m57_p332_one_seed_reduction import (
    CANONICAL_REFERENCE_PRIMES,
    HARD_SEED,
    NONCANONICAL,
    PROFILE,
    placement_scan,
    reduction_audit,
    reference_certificate,
)
from m57_p332_one_seed_reduction import MINIMAL_ODD_PRIMES


def test_m57_placement_scan():
    out = placement_scan()
    assert out["verified"]
    assert out["assignment_count"] == 60
    assert out["directly_killed_placement_count"] == 52
    assert len(out["surviving_placements"]) == 8


def test_m57_reference_certificates():
    for exponents in NONCANONICAL:
        assert reference_certificate(MINIMAL_ODD_PRIMES, exponents)["summed_rho_margin"] > 0
    assert reference_certificate(CANONICAL_REFERENCE_PRIMES, PROFILE)["summed_rho_margin"] > 0


def test_m57_one_seed_reduction():
    out = reduction_audit()
    assert out["verified"]
    assert out["profile"] == PROFILE
    assert out["hard_seed"] == HARD_SEED == 3**3 * 5**3 * 7**2 * 11 * 13 * 17
    assert out["all_other_profile_members_noncovering"]
