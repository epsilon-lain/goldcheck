from m53_two_repeated_coordinates import (
    EXPECTED_PAIR_LIMITS,
    TEMPLATES_35,
    TEMPLATES_37,
    anchor_audit,
    pair_limit_scan,
    propagated_gap,
    theorem_audit,
)


def test_m53_only_two_repeated_prime_pairs_survive_double_infinity():
    out = pair_limit_scan()
    assert out["verified"]
    assert out["pair_count"] == 15
    assert out["surviving_pairs"] == EXPECTED_PAIR_LIMITS
    assert out["max_killed_R"] < 1
    assert anchor_audit()["verified"]


def test_m53_all_universal_templates_are_closed_for_all_exponents():
    assert len(TEMPLATES_35) == 22
    assert len(TEMPLATES_37) == 2
    assert propagated_gap(6, 5) > 0
    assert propagated_gap(20, 5) > propagated_gap(6, 5)
    assert propagated_gap(6, 7) > 0
    assert propagated_gap(20, 7) > propagated_gap(6, 7)
    out = theorem_audit()
    assert out["verified"]
    assert out["universal_template_count"] == 24
    assert out["all_exactly_two_repeated_six_prime_numbers_noncovering"]
