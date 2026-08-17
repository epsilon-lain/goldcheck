"""Regression tests for M24 (4,3,1,1,1,1) frontier reduction."""
from fractions import Fraction

from m24_four_three_frontier import (
    CANONICAL_43,
    EXCEPTIONAL,
    REMAINING_N,
    SWAPPED_34,
    affine34,
    assignment_scan,
    direct34,
    direct43,
    m16_generalized,
    m24_audit,
    p19_diagonal,
)


def test_m24_direct_placement_scan_has_only_two_exceptions():
    result=assignment_scan()
    assert result["count"]==30
    assert result["exceptions"]==tuple(sorted((CANONICAL_43,SWAPPED_34)))
    assert result["nonexceptional_max"]==Fraction(112558664,112567455)<1


def test_m24_swapped_3_3_5_4_affine_certificates():
    expected={
        17:Fraction(12690063,3038750000),
        19:Fraction(274867563,6256250000),
        23:Fraction(227052153,2213750000),
    }
    for P,margin in expected.items():
        result=affine34(P)
        assert result["margin"]==margin>0
        assert result["clique_min"]>0
    assert direct34(29)==Fraction(44366614,44533125)<1


def test_m24_hard_side_generalized_m16_certificates():
    expected={
        (7,11,13,23):Fraction(2134682349002381,29351626992187500),
        (7,11,13,29):Fraction(1238712960918459209,4246331503476562500),
        (7,11,13,31):Fraction(1675429219652823839,4852228983164062500),
        (7,11,13,37):Fraction(464467129271395583,987468630585937500),
        (7,11,17,19):Fraction(63976862971583,200798554687500),
    }
    for simple,margin in expected.items():
        result=m16_generalized(simple)
        assert result["margin"]==margin>0
        assert result["completion_max"]<0
    assert direct43(41)==Fraction(138508738,138513375)<1


def test_m24_p19_all_diagonal_quadratic_certificate():
    result=p19_diagonal()
    assert result["margin"]==Fraction(
        1098589626561579134109123,
        39422315130808610000000000,
    )>0
    assert result["proper_non5_min"]==Fraction(1,91)>0
    assert result["completion_max"]==Fraction(-23641,2377375)<0


def test_m24_reduction_leaves_exactly_the_p17_seed():
    result=m24_audit()
    assert result["remaining_seed"]==REMAINING_N==172297125
    assert result["remaining_prime_tuple"]==(3,5,7,11,13,17)
    assert result["remaining_exponents"]==CANONICAL_43
    assert result["all_other_profile_members_excluded"] is True
    assert result["profile_fully_excluded"] is False
