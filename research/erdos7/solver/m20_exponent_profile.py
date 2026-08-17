"""M20: exact exclusion of the six-prime exponent multiset {4,2,1,1,1,1}."""
from __future__ import annotations
from fractions import Fraction
from itertools import permutations
from m17_infinite_family import elementary_symmetric, is_prime
from m19_four_parameter_family import proof_branch as m19_proof_branch

EXPONENT_MULTISET=(4,2,1,1,1,1)
CANONICAL_ASSIGNMENT=(4,2,1,1,1,1)
MINIMAL_ODD_PRIMES=(3,5,7,11,13,17)
CANONICAL_OFFBASE_PRIMES=(3,7,11,13,17,19)
PROFILE_E23_CAP=Fraction(721,1440)
PROFILE_DERIVATIVE_GAP=Fraction(719,1440)
CANONICAL_MINIMAL_R=Fraction(293467,289575)
NONCANONICAL_MAX_ASSIGNMENT=(4,1,2,1,1,1)
NONCANONICAL_MAX_R=Fraction(16047137,16081065)
CANONICAL_OFFBASE_R=Fraction(54428893,61108047)

def prime_power_x(p:int,a:int)->Fraction:
    if p<=1 or a<1: raise ValueError("p>1 and a>=1 required")
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))

def profile_direct_bound(primes:tuple[int,...], exponents:tuple[int,...])->Fraction:
    if len(primes)!=6 or len(exponents)!=6: raise ValueError("need six coordinates")
    xs=tuple(prime_power_x(p,a) for p,a in zip(primes,exponents))
    return (elementary_symmetric(xs,1)-elementary_symmetric(xs,3)-elementary_symmetric(xs,4)+2*elementary_symmetric(xs,5)+9*elementary_symmetric(xs,6))

def profile_monotonicity_derivative_lower_bound()->Fraction:
    assert prime_power_x(3,4)==Fraction(40,81)<Fraction(1,2)
    assert prime_power_x(5,4)==Fraction(156,625)<Fraction(1,4)
    assert prime_power_x(7,4)==Fraction(400,2401)<Fraction(1,6)
    assert prime_power_x(11,4)==Fraction(1464,14641)<Fraction(1,10)
    assert prime_power_x(13,4)==Fraction(2380,28561)<Fraction(1,12)
    U=(Fraction(1,2),Fraction(1,4),Fraction(1,6),Fraction(1,10),Fraction(1,12))
    cap=elementary_symmetric(U,2)+elementary_symmetric(U,3)
    assert cap==PROFILE_E23_CAP
    gap=1-cap
    assert gap==PROFILE_DERIVATIVE_GAP and gap>0
    return gap

def assignment_scan()->dict:
    assignments=tuple(sorted(set(permutations(EXPONENT_MULTISET))))
    assert len(assignments)==30
    values={a:profile_direct_bound(MINIMAL_ODD_PRIMES,a) for a in assignments}
    assert values[CANONICAL_ASSIGNMENT]==CANONICAL_MINIMAL_R>1
    noncanon={a:v for a,v in values.items() if a!=CANONICAL_ASSIGNMENT}
    amax=max(noncanon,key=noncanon.get); vmax=noncanon[amax]
    assert amax==NONCANONICAL_MAX_ASSIGNMENT
    assert vmax==NONCANONICAL_MAX_R<1
    assert 1-vmax==Fraction(33928,16081065)
    return {"assignment_count":30,"canonical_assignment":CANONICAL_ASSIGNMENT,"canonical_minimal_R":CANONICAL_MINIMAL_R,"noncanonical_max_assignment":amax,"noncanonical_max_R":vmax,"all_noncanonical_directly_excluded":True}

def _ordered(primes:tuple[int,...], exponents:tuple[int,...])->tuple[tuple[int,...],tuple[int,...]]:
    if len(primes)!=6 or len(exponents)!=6: raise ValueError("need six coordinates")
    if len(set(primes))!=6 or not all(is_prime(p) and p%2==1 for p in primes): raise ValueError("need six distinct odd primes")
    if tuple(sorted(exponents,reverse=True))!=EXPONENT_MULTISET: raise ValueError("wrong exponent multiset")
    pairs=sorted(zip(primes,exponents))
    return tuple(p for p,_ in pairs),tuple(a for _,a in pairs)

def proof_branch(primes:tuple[int,...], exponents:tuple[int,...])->str:
    primes,exponents=_ordered(primes,exponents)
    assert profile_monotonicity_derivative_lower_bound()>0
    if exponents!=CANONICAL_ASSIGNMENT:
        scan=assignment_scan(); base=profile_direct_bound(MINIMAL_ODD_PRIMES,exponents)
        assert base<=scan["noncanonical_max_R"]<1
        assert all(p>=p0 for p,p0 in zip(primes,MINIMAL_ODD_PRIMES))
        assert profile_direct_bound(primes,exponents)<=base
        return "McNew-Setty-noncanonical-placement"
    if primes[:2]==(3,5):
        assert m19_proof_branch(*primes[2:]) in ("M18-three-parameter","McNew-Setty-full-divisor")
        return "M19-four-parameter"
    assert all(p>=p0 for p,p0 in zip(primes,CANONICAL_OFFBASE_PRIMES))
    anchor=profile_direct_bound(CANONICAL_OFFBASE_PRIMES,CANONICAL_ASSIGNMENT)
    assert anchor==CANONICAL_OFFBASE_R<1
    assert 1-anchor==Fraction(6679154,61108047)
    assert profile_direct_bound(primes,exponents)<=anchor
    return "McNew-Setty-canonical-offbase"

def exponent_profile_audit()->dict:
    gap=profile_monotonicity_derivative_lower_bound(); scan=assignment_scan()
    assert profile_direct_bound(CANONICAL_OFFBASE_PRIMES,CANONICAL_ASSIGNMENT)==CANONICAL_OFFBASE_R<1
    assert proof_branch((3,5,7,11,13,17),(4,2,1,1,1,1))=="M19-four-parameter"
    assert proof_branch((3,5,7,11,13,17),(4,1,2,1,1,1))=="McNew-Setty-noncanonical-placement"
    assert proof_branch((3,7,11,13,17,19),(4,2,1,1,1,1))=="McNew-Setty-canonical-offbase"
    return {**scan,"profile":EXPONENT_MULTISET,"coordinate_derivative_lower_bound":gap,"canonical_offbase_R":CANONICAL_OFFBASE_R,"canonical_offbase_gap":1-CANONICAL_OFFBASE_R,"all_odd_six_prime_numbers_with_profile_noncovering":True}
