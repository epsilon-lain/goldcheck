from m71_p4222_special13_placement import certificate_audit, theorem_audit


def test_m71_exact_reference_certificate():
    a=certificate_audit()
    assert a["state_count"]==32_000_000
    assert a["floor_slack_scaled"]==3246
    assert a["summed_goodness_margin"]>0
    assert a["noncovering_certified"]


def test_m71_full_exponent_placement_closed():
    a=theorem_audit()
    assert a["anchors"]["anchor_count"]==3
    assert a["all_odd_six_prime_numbers_with_this_placement_noncovering"]
