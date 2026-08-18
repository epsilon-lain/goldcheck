from m68_p4222_canonical_seed import certificate_audit as m68_audit
from m69_p4222_canonical_tail import certificate_audit as m69_audit
from m70_p4222_canonical_placement import theorem_audit


def test_m68_reference_exact_certificate():
    a=m68_audit()
    assert a["state_count"]==32_000_000
    assert a["floor_slack_scaled"]==3368
    assert a["summed_goodness_margin"]>0


def test_m69_reference_exact_certificate():
    a=m69_audit()
    assert a["state_count"]==32_000_000
    assert a["floor_slack_scaled"]==12099
    assert a["summed_goodness_margin"]>0


def test_m70_canonical_placement_closed():
    a=theorem_audit()
    assert a["reference_certificate_count"]==2
    assert a["all_odd_six_prime_numbers_with_this_placement_noncovering"]
