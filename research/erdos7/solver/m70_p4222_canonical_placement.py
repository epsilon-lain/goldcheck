"""M70: close the canonical exponent placement (4,2,2,2,1,1).

This is one of the nine direct-bound survivor placements of the sorted profile
(4,2,2,2,1,1).  M68 and M69 give exact weighted double-square references for
the only two possible repeated fourth primes that are not already killed by
the direct McNew--Setty bound.
"""
from __future__ import annotations

from fractions import Fraction

from m17_infinite_family import is_prime
from m22_universal_direct_zones import universal_monotonicity_gap
from m26_minimal_frontier import direct_bound
from m68_p4222_canonical_seed import certificate_audit as m68_audit
from m69_p4222_canonical_tail import certificate_audit as m69_audit

EXPONENTS=(4,2,2,2,1,1)
OFF3=(5,7,11,13,17,19)
OFF5=(3,7,11,13,17,19)
OFF7=(3,5,11,13,17,19)
OFF11=(3,5,7,17,19,23)
EXPECTED_ANCHORS={
    OFF3:Fraction(1152611472,1699823125),
    OFF5:Fraction(24386608,27054027),
    OFF7:Fraction(12885744848,13375179675),
    OFF11:Fraction(12356852246,12531422925),
}


def anchor_audit()->dict:
    assert universal_monotonicity_gap()>0
    for primes,expected in EXPECTED_ANCHORS.items():
        assert direct_bound(primes,EXPONENTS)==expected<1
    return {"anchor_count":len(EXPECTED_ANCHORS),"verified":True}


def proof_branch(primes:tuple[int,...])->str:
    primes=tuple(primes)
    if len(primes)!=6 or tuple(sorted(primes))!=primes or len(set(primes))!=6:
        raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p%2 for p in primes):
        raise ValueError("need six odd primes")
    assert universal_monotonicity_gap()>0

    if primes[0]!=3:
        assert all(p>=q for p,q in zip(primes,OFF3))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF3]<1
        return "McNew-Setty-off3"
    if primes[1]!=5:
        assert all(p>=q for p,q in zip(primes,OFF5))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF5]<1
        return "McNew-Setty-off5"
    if primes[2]!=7:
        assert all(p>=q for p,q in zip(primes,OFF7))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF7]<1
        return "McNew-Setty-off7"

    # Prefix is now exactly (3,5,7).  If the next repeated prime is 11 or 13,
    # M27 supportwise scaling changes only the two simple coordinates.  The
    # weighted normalized activation laws for 7^2 and the fourth-prime square
    # are therefore unchanged, while every support baseline scales exactly.
    if primes[3]==11:
        assert primes[4]>=13 and primes[5]>=17
        assert m68_audit()["summed_goodness_margin"]>0
        return "M68-double-square-scale"
    if primes[3]==13:
        assert primes[4]>=17 and primes[5]>=19
        assert m69_audit()["summed_goodness_margin"]>0
        return "M69-double-square-scale"

    assert primes[3]>=17
    assert all(p>=q for p,q in zip(primes,OFF11))
    assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF11]<1
    return "McNew-Setty-fourth-prime-tail"


def theorem_audit()->dict:
    anchors=anchor_audit()
    a68=m68_audit(); a69=m69_audit()
    assert a68["noncovering_certified"] and a69["noncovering_certified"]
    assert proof_branch((3,5,7,11,13,17))=="M68-double-square-scale"
    assert proof_branch((3,5,7,11,29,31))=="M68-double-square-scale"
    assert proof_branch((3,5,7,13,17,19))=="M69-double-square-scale"
    assert proof_branch((3,5,7,13,19,23))=="M69-double-square-scale"
    assert proof_branch(OFF11)=="McNew-Setty-fourth-prime-tail"
    return {
        "exponent_placement":EXPONENTS,
        "anchors":anchors,
        "reference_certificate_count":2,
        "all_odd_six_prime_numbers_with_this_placement_noncovering":True,
        "verified":True,
    }


__all__=["EXPONENTS","anchor_audit","proof_branch","theorem_audit"]
