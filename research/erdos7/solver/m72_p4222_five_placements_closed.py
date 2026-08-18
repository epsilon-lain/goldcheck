"""M72: reduce the P4222 profile to four unresolved exponent placements.

The sorted profile is (4,2,2,2,1,1).  At the minimal odd prime tuple exactly
nine of the 60 exponent placements survive the universal McNew--Setty bound.

This module closes five of those nine placements:

* three placements by exact a=4 M66-style goodness reference certificates at
  (3,5,7,11,13,17), transported by M27 supportwise scaling;
* the canonical placement (4,2,2,2,1,1) by M68--M70;
* the placement (4,2,2,1,2,1) by M71.

Exactly four direct-survivor placements remain unresolved here.  This is a
profile reduction, not a closure of the full profile and not a solution of
Erdos Problem #7.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import permutations

from m17_infinite_family import is_prime
from m22_universal_direct_zones import universal_monotonicity_gap
from m25_cross_support_seed import CROSS, DIAGONAL, LAMBDA
from m26_minimal_frontier import direct_bound, sorted_profile
from m70_p4222_canonical_placement import theorem_audit as m70_audit
from m71_p4222_special13_placement import theorem_audit as m71_audit

PROFILE=(4,2,2,2,1,1)
MINIMAL_ODD_PRIMES=(3,5,7,11,13,17)
OFF3=(5,7,11,13,17,19)
J_MASK=0b11110
NON5=tuple(m for m in range(1,32) if not (m&1))
J_SUBSETS=tuple(T for T in range(32) if not (T&~J_MASK))
FIVE=tuple(1|T for T in J_SUBSETS)

G1=(4,1,2,1,2,2)
G2=(4,1,2,2,1,2)
G3=(4,1,2,2,2,1)
OPEN1=(4,2,1,1,2,2)
OPEN2=(4,2,1,2,1,2)
OPEN3=(4,2,1,2,2,1)
OPEN4=(4,2,2,1,1,2)
M71=(4,2,2,1,2,1)
M70=(4,2,2,2,1,1)

SURVIVING_PLACEMENTS=(G1,G2,G3,OPEN1,OPEN2,OPEN3,OPEN4,M71,M70)
GOODNESS_PLACEMENTS=(G1,G2,G3)
OPEN_PLACEMENTS=(OPEN1,OPEN2,OPEN3,OPEN4)
CLOSED_SURVIVOR_PLACEMENTS=(G1,G2,G3,M71,M70)

EXPECTED_SURVIVOR_R={
G1:Fraction(10699185556,10661746095),
G2:Fraction(533361658,530675145),
G3:Fraction(6944383078,6898776885),
OPEN1:Fraction(7759506158,7615532925),
OPEN2:Fraction(2656768,2603601),
OPEN3:Fraction(5035760564,4927697775),
OPEN4:Fraction(248183836,241215975),
M71:Fraction(65939392,63996075),
M70:Fraction(547573318,530675145),
}
EXPECTED_MAX_KILLED=((2,4,2,2,1,1),Fraction(113145118,113392125))
EXPECTED_OFF3={
G1:Fraction(18959306456,28719165475),
G2:Fraction(51947247492,78434695625),
G3:Fraction(325644362198,491248883125),
}
# pointwise C, summed-goodness margin, argmin non-special endpoint bits
GOODNESS_EXPECTED={
G1:(
Fraction(7274858595929123889875931233,19191027206273717314520000000),
Fraction(222591620880138610754590200697,940360333107412148411480000000),
21569),
G2:(
Fraction(1917989911819141021016351159,5049568060917020856114900000),
Fraction(58833770132728359473247079,388428312378232373547300000),
21569),
G3:(
Fraction(5082688618950259523693551,13361364704237995344900000),
Fraction(4103687720150083458129379,60262481625236672882100000),
21569),
}


def _ppx(p:int,a:int)->Fraction:
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))

def _coords(primes:tuple[int,...],exponents:tuple[int,...])->tuple[Fraction,...]:
    return tuple(_ppx(p,a) for p,a in zip(primes[1:],exponents[1:]))

def _baseline(coords:tuple[Fraction,...],mask:int)->Fraction:
    out=Fraction(1)
    for i,x in enumerate(coords):
        if mask&(1<<i):out*=x
    return out

def _rho(q:dict[int,Fraction])->dict[int,Fraction]:
    rho={0:Fraction(1)}
    for size in range(1,5):
        for Cmask in range(32):
            if Cmask&~J_MASK or Cmask.bit_count()!=size:continue
            pivot=Cmask&-Cmask;rest=Cmask^pivot
            value=rho[rest];T=rest
            while True:
                S=pivot|T
                value-=q.get(S,Fraction(0))*rho[Cmask^S]
                if T==0:break
                T=(T-1)&rest
            rho[Cmask]=value
    return rho

def _quadratic_min(linear:Fraction,quadratic:Fraction,lo:Fraction,hi:Fraction)->Fraction:
    x=-linear/(2*quadratic)
    if x<lo:x=lo
    elif x>hi:x=hi
    return linear*x+quadratic*x*x

@lru_cache(maxsize=None)
def goodness_reference(exponents:tuple[int,...])->dict:
    exponents=tuple(exponents)
    if exponents not in GOODNESS_PLACEMENTS:
        raise ValueError("not an M72 goodness placement")
    coords=_coords(MINIMAL_ODD_PRIMES,exponents)
    b={m:_baseline(coords,m) for m in range(1,32)}
    pcoord=sum(
        LAMBDA.get(1|T,Fraction(0))*b[1|T]+DIAGONAL[1|T]*b[1|T]**2
        for T in J_SUBSETS
    )
    best=None;argmin=None
    for bits in range(1<<len(NON5)):
        q0={m:b[m]*(5 if bits&(1<<i) else 1) for i,m in enumerate(NON5)}
        rho=_rho(q0)
        nonspecial=(
            sum(LAMBDA.get(m,Fraction(0))*q0[m] for m in NON5)
            +sum(mu*q0[s]*q0[t] for (s,t),mu in CROSS.items())
        )
        full=rho[J_MASK]
        for T in J_SUBSETS:
            m=1|T
            full+=_quadratic_min(
                LAMBDA.get(m,Fraction(0))-rho[J_MASK^T],
                DIAGONAL[m],b[m],5*b[m]
            )
        coordinate=min(v for Cmask,v in rho.items() if Cmask!=0)+pcoord
        value=nonspecial+min(full,coordinate)
        if best is None or value<best:
            best=value;argmin=bits
    assert best is not None and argmin is not None
    margin=(
        41*best
        -81*sum(LAMBDA.get(m,Fraction(0))*b[m] for m in range(1,32))
        -197*sum(DIAGONAL[m]*b[m]**2 for m in FIVE)
        -197*sum(mu*b[s]*b[t] for (s,t),mu in CROSS.items())
    )
    eC,eM,eA=GOODNESS_EXPECTED[exponents]
    assert best==eC and margin==eM>0 and argmin==eA
    return {"exponents":exponents,"C":best,"summed_goodness_margin":margin,
            "argmin_bits":argmin,"verified":True}


def placement_scan()->dict:
    assert universal_monotonicity_gap()>0
    assignments=tuple(sorted(set(permutations(PROFILE))))
    values={a:direct_bound(MINIMAL_ODD_PRIMES,a) for a in assignments}
    survivors=tuple(a for a in assignments if values[a]>=1)
    assert len(assignments)==60 and set(survivors)==set(SURVIVING_PLACEMENTS)
    assert {a:values[a] for a in survivors}==EXPECTED_SURVIVOR_R
    killed={a:v for a,v in values.items() if v<1}
    amax=max(killed,key=killed.get)
    assert (amax,killed[amax])==EXPECTED_MAX_KILLED
    return {"assignment_count":60,"survivor_count":9,
            "directly_killed_placement_count":51,
            "surviving_placements":survivors,"verified":True}


def _scale_check(primes:tuple[int,...],exponents:tuple[int,...])->None:
    actual=_coords(primes,exponents);ref=_coords(MINIMAL_ODD_PRIMES,exponents)
    assert all(x<=y for x,y in zip(actual,ref))
    for m in range(1,32):
        b=_baseline(actual,m);bbar=_baseline(ref,m);gamma=bbar/b
        assert gamma>=1 and gamma*b==bbar
    # The first/pair moment budgets transport exactly under supportwise scaling.
    for s,t in ((1,2),(3,12),(14,17),(30,31)):
        bs=_baseline(actual,s);bt=_baseline(actual,t)
        rs=_baseline(ref,s);rt=_baseline(ref,t)
        assert (rs/bs)*(rt/bt)*bs*bt==rs*rt


def proof_branch(primes:tuple[int,...],exponents:tuple[int,...])->str:
    primes=tuple(primes);exponents=tuple(exponents)
    if len(primes)!=6 or tuple(sorted(primes))!=primes or len(set(primes))!=6:
        raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p%2 for p in primes):
        raise ValueError("need six odd primes")
    if sorted_profile(exponents)!=PROFILE:
        raise ValueError("wrong exponent profile")
    assert universal_monotonicity_gap()>0

    if exponents not in SURVIVING_PLACEMENTS:
        base=direct_bound(MINIMAL_ODD_PRIMES,exponents)
        assert base<1 and direct_bound(primes,exponents)<=base
        return "McNew-Setty-placement"

    if exponents in GOODNESS_PLACEMENTS:
        if primes[0]!=3:
            assert all(p>=q for p,q in zip(primes,OFF3))
            expected=EXPECTED_OFF3[exponents]
            assert direct_bound(OFF3,exponents)==expected<1
            assert direct_bound(primes,exponents)<=expected
            return "McNew-Setty-goodness-off3"
        cert=goodness_reference(exponents)
        _scale_check(primes,exponents)
        assert cert["summed_goodness_margin"]>0
        return "M72-goodness-reference-scale"

    if exponents==M70:
        assert m70_audit()["all_odd_six_prime_numbers_with_this_placement_noncovering"]
        return "M70-canonical-placement"
    if exponents==M71:
        assert m71_audit()["all_odd_six_prime_numbers_with_this_placement_noncovering"]
        return "M71-special13-placement"

    assert exponents in OPEN_PLACEMENTS
    return "M72-open-placement"

@lru_cache(maxsize=1)
def reduction_audit()->dict:
    scan=placement_scan()
    refs={a:goodness_reference(a) for a in GOODNESS_PLACEMENTS}
    assert all(c["summed_goodness_margin"]>0 for c in refs.values())
    assert m70_audit()["verified"] and m71_audit()["verified"]
    assert proof_branch(MINIMAL_ODD_PRIMES,G1)=="M72-goodness-reference-scale"
    assert proof_branch(MINIMAL_ODD_PRIMES,M70)=="M70-canonical-placement"
    assert proof_branch(MINIMAL_ODD_PRIMES,M71)=="M71-special13-placement"
    assert {a for a in SURVIVING_PLACEMENTS if proof_branch(MINIMAL_ODD_PRIMES,a)=="M72-open-placement"}==set(OPEN_PLACEMENTS)
    return {"profile":PROFILE,"placement_scan":scan,
            "new_goodness_closed_placements":GOODNESS_PLACEMENTS,
            "previously_closed_placements":(M70,M71),
            "closed_direct_survivor_count":5,
            "open_direct_survivor_count":4,
            "open_placements":OPEN_PLACEMENTS,"verified":True}

__all__=["CLOSED_SURVIVOR_PLACEMENTS","GOODNESS_EXPECTED","GOODNESS_PLACEMENTS",
         "OPEN_PLACEMENTS","PROFILE","SURVIVING_PLACEMENTS","goodness_reference",
         "placement_scan","proof_branch","reduction_audit"]
