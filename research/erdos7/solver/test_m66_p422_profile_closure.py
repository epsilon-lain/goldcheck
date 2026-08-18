from m66_p422_profile_closure import (
    CANONICAL,
    EXCEPTIONAL,
    GOODNESS_EXPECTED,
    PROFILE,
    SURVIVING_PLACEMENTS,
    WEIGHTED,
    goodness_reference_certificate,
    placement_scan,
    proof_branch,
    theorem_audit,
    weighted_certificate_audit,
)


def test_m66_placement_scan():
    out = placement_scan()
    assert out["verified"]
    assert out["assignment_count"] == 60
    assert out["directly_killed_placement_count"] == 54
    assert set(out["surviving_placements"]) == set(SURVIVING_PLACEMENTS)


def test_m66_goodness_references():
    for key in GOODNESS_EXPECTED:
        out = goodness_reference_certificate(*key)
        assert out["verified"]
        assert out["summed_goodness_margin"] > 0


def test_m66_weighted_hard_certificates():
    for name in ("canonical", "exceptional"):
        out = weighted_certificate_audit(name)
        cfg = WEIGHTED[name]
        assert out["noncovering_certified"]
        assert out["state_count"] == 5**5 * 2**11 == 6_400_000
        assert out["floor_slack_scaled"] > 0
        assert out["exact_argmin_value"] > cfg["C"]
        assert out["summed_goodness_margin"] > 0


def test_m66_profile_closure():
    out = theorem_audit()
    assert out["verified"]
    assert out["profile"] == PROFILE
    assert out["all_odd_six_prime_numbers_with_profile_noncovering"]
    assert proof_branch((3,5,7,11,13,17), CANONICAL) == "M66-weighted-7-square-scale"
    assert proof_branch((3,5,7,11,13,17), EXCEPTIONAL) == "M66-weighted-11-square"
