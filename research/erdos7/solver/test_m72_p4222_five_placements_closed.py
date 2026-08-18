from fractions import Fraction

from m72_p4222_five_placements_closed import (
    GOODNESS_EXPECTED,
    GOODNESS_PLACEMENTS,
    OPEN_PLACEMENTS,
    PROFILE,
    goodness_reference,
    placement_scan,
    proof_branch,
    reduction_audit,
)

MINP=(3,5,7,11,13,17)


def test_placement_scan_is_exact():
    scan=placement_scan()
    assert scan["assignment_count"]==60
    assert scan["survivor_count"]==9
    assert scan["directly_killed_placement_count"]==51


def test_three_new_goodness_references_are_exact_positive():
    for exponents in GOODNESS_PLACEMENTS:
        cert=goodness_reference(exponents)
        C,margin,argmin=GOODNESS_EXPECTED[exponents]
        assert cert["C"]==C
        assert cert["summed_goodness_margin"]==margin>0
        assert cert["argmin_bits"]==argmin==21569


def test_existing_m70_m71_and_new_goodness_leave_four():
    audit=reduction_audit()
    assert audit["profile"]==PROFILE
    assert audit["closed_direct_survivor_count"]==5
    assert audit["open_direct_survivor_count"]==4
    assert tuple(audit["open_placements"])==OPEN_PLACEMENTS


def test_open_placements_are_exactly_classified_open_at_minimal_tuple():
    assert all(proof_branch(MINP,a)=="M72-open-placement" for a in OPEN_PLACEMENTS)


def test_new_goodness_scaling_branch_on_larger_tuple():
    assert proof_branch((3,7,11,13,17,19),GOODNESS_PLACEMENTS[0])=="M72-goodness-reference-scale"


def test_off3_goodness_branch_is_direct():
    assert proof_branch((5,7,11,13,17,19),GOODNESS_PLACEMENTS[1])=="McNew-Setty-goodness-off3"
