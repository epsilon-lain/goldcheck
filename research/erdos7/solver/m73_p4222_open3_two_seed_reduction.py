"""M73: reduce exponent placement (4,2,1,2,2,1) to two hard seeds.

For increasing odd primes p1<...<p6, direct McNew--Setty anchors force any
unresolved tuple for this placement to have prefix (3,5,7,11).  If p5>=19 a
direct anchor closes it.  Two exact M66-style goodness references close
p5=13 with p6>=23 and p5=17 with p6>=19, respectively.  Therefore only

    (3,5,7,11,13,17), (3,5,7,11,13,19)

remain unresolved for this placement.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache

from m17_infinite_family import is_prime
from m22_universal_direct_zones import universal_monotonicity_gap
from m25_cross_support_seed import CROSS,DIAGONAL,LAMBDA
from m26_minimal_frontier import direct_bound
from m72_p4222_five_placements_closed import (
    J_MASK,NON5,J_SUBSETS,FIVE,_coords,_baseline,_rho,_quadratic_min,
)

EXPONENTS=(4,2,1,2,2,1)
OFF3=(5,7,11,13,17,19)
OFF5=(3,7,11,13,17,19)
OFF7=(3,5,11,13,17,19)
OFF11=(3,5,7,13,17,19)
OFF13_17=(3,5,7,11,19,23)
EXPECTED_ANCHORS={
OFF3:Fraction(210670030458,312612925625),
OFF5:Fraction(4040925754,4501626129),
OFF7:Fraction(19842628706,20670732225),
OFF11:Fraction(4367161954,4384700775),
OFF13_17:Fraction(14196798158,14241098025),
}
REF13=(3,5,7,11,13,23)
REF17=(3,5,7,11,17,19)
HARD_SEEDS=((3,5,7,11,13,17),(3,5,7,11,13,19))
EXPECTED={
REF13:(
Fraction(15537396644207904142201838484667,39000910457186880649887440000000),
Fraction(3572573911745719375023766982387,39000910457186880649887440000000),
11894),
REF17:(
Fraction(29690251905470938104154426439256719,74483570900239983666158971920000000),
Fraction(8641667081450002389773953401647099,14896714180047996733231794384000000),
10854),
}

@lru_cache(maxsize=None)
def goodness_reference(primes:tuple[int,...])->dict:
    primes=tuple(primes)
    if primes not in EXPECTED:raise ValueError("not an M73 reference")
    coords=_coords(primes,EXPONENTS)
    b={m:_baseline(coords,m) for m in range(1,32)}
    pcoord=sum(LAMBDA.get(1|T,Fraction(0))*b[1|T]+DIAGONAL[1|T]*b[1|T]**2 for T in J_SUBSETS)
    best=None;argmin=None
    for bits in range(1<<len(NON5)):
        q0={m:b[m]*(5 if bits&(1<<i) else 1) for i,m in enumerate(NON5)}
        rho=_rho(q0)
        nonspecial=sum(LAMBDA.get(m,Fraction(0))*q0[m] for m in NON5)+sum(mu*q0[s]*q0[t] for (s,t),mu in CROSS.items())
        full=rho[J_MASK]
        for T in J_SUBSETS:
            m=1|T
            full+=_quadratic_min(LAMBDA.get(m,Fraction(0))-rho[J_MASK^T],DIAGONAL[m],b[m],5*b[m])
        coordinate=min(v for C,v in rho.items() if C!=0)+pcoord
        value=nonspecial+min(full,coordinate)
        if best is None or value<best:best=value;argmin=bits
    margin=(41*best
        -81*sum(LAMBDA.get(m,Fraction(0))*b[m] for m in range(1,32))
        -197*sum(DIAGONAL[m]*b[m]**2 for m in FIVE)
        -197*sum(mu*b[s]*b[t] for (s,t),mu in CROSS.items()))
    eC,eM,eA=EXPECTED[primes]
    assert best==eC and margin==eM>0 and argmin==eA
    return {"primes":primes,"C":best,"summed_goodness_margin":margin,"argmin_bits":argmin,"verified":True}


def _scale_check(primes:tuple[int,...],ref:tuple[int,...])->None:
    actual=_coords(primes,EXPONENTS);base=_coords(ref,EXPONENTS)
    assert all(x<=y for x,y in zip(actual,base))
    for m in range(1,32):
        b=_baseline(actual,m);bb=_baseline(base,m)
        assert bb/b>=1 and (bb/b)*b==bb


def proof_branch(primes:tuple[int,...])->str:
    primes=tuple(primes)
    if len(primes)!=6 or tuple(sorted(primes))!=primes or len(set(primes))!=6:raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p%2 for p in primes):raise ValueError("need six odd primes")
    assert universal_monotonicity_gap()>0
    for idx,(anchor,label) in enumerate(((OFF3,"off3"),(OFF5,"off5"),(OFF7,"off7"),(OFF11,"off11"))):
        if primes[idx] != (3,5,7,11)[idx]:
            assert all(p>=q for p,q in zip(primes,anchor))
            assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[anchor]<1
            return "McNew-Setty-"+label
    assert primes[:4]==(3,5,7,11)
    if primes[4]>=19:
        assert all(p>=q for p,q in zip(primes,OFF13_17))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF13_17]<1
        return "McNew-Setty-p5-tail"
    if primes[4]==17:
        assert primes[5]>=19
        _scale_check(primes,REF17)
        assert goodness_reference(REF17)["summed_goodness_margin"]>0
        return "M73-goodness-17-19-scale"
    assert primes[4]==13
    if primes[5]>=23:
        _scale_check(primes,REF13)
        assert goodness_reference(REF13)["summed_goodness_margin"]>0
        return "M73-goodness-13-23-scale"
    assert primes in HARD_SEEDS
    return "M73-hard-seed"

@lru_cache(maxsize=1)
def reduction_audit()->dict:
    for a,v in EXPECTED_ANCHORS.items():assert direct_bound(a,EXPONENTS)==v<1
    a=goodness_reference(REF13);b=goodness_reference(REF17)
    assert proof_branch(REF13)=="M73-goodness-13-23-scale"
    assert proof_branch(REF17)=="M73-goodness-17-19-scale"
    assert all(proof_branch(s)=="M73-hard-seed" for s in HARD_SEEDS)
    return {"exponent_placement":EXPONENTS,"goodness_references":(a,b),
            "hard_seed_prime_tuples":HARD_SEEDS,"hard_seed_count":2,"verified":True}

__all__=["EXPONENTS","HARD_SEEDS","EXPECTED","goodness_reference","proof_branch","reduction_audit"]
