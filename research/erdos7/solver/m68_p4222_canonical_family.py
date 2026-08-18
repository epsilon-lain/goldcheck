"""M68: close the canonical placement (4,2,2,2,1,1).

For increasing odd primes p1<...<p6, this module proves the placement

    p1^4 p2^2 p3^2 p4^2 p5 p6

is noncovering.

Direct McNew--Setty anchors force p1,p2,p3=(3,5,7) and p4 in {11,13}.
For p4=11 and p4=13, exact a=4 weighted two-square certificates retain
both exact-divisor activation pairs. The same nonnegative coefficient tensor
works for both references. Since the repeated primes are fixed inside each
branch, M27 supportwise scaling changes only the two simple coordinates and
preserves the exact normalized weighted activations and factorial features.

The standalone C++ verifier exhausts 25^2*5^2*2^11=32,000,000 states for each
reference with rigorous downward-rounded integer arithmetic.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import comb

from m17_infinite_family import is_prime
from m25_cross_support_seed import DIAGONAL, LAMBDA
from m26_minimal_frontier import direct_bound

EXPONENTS=(4,2,2,2,1,1)
Q=10**8
DEN=10_000
STATE_COUNT=25**2*5**2*2**11

OFF3=(5,7,11,13,17,19)
OFF5=(3,7,11,13,17,19)
OFF7=(3,5,11,13,17,19)
OFF11_13=(3,5,7,17,19,23)

EXPECTED_ANCHORS={
    OFF3:Fraction(1152611472,1699823125),
    OFF5:Fraction(24386608,27054027),
    OFF7:Fraction(12885744848,13375179675),
    OFF11_13:Fraction(12356852246,12531422925),
}

# Coefficients, all divided by DEN.
LINEAR=(0,0,3000,0,2412,2765,5069,0,2013,2066,4462,1333,3613,3802,6611)
PAIR_S=tuple(s for s in range(1,16) for t in range(s+1,16))
PAIR_T=tuple(t for s in range(1,16) for t in range(s+1,16))
PAIR=(
0,3826,0,4114,0,145,0,4289,0,624,0,2048,0,0,
0,0,0,1340,0,0,0,2717,0,0,0,629,0,
0,3653,0,10352,0,3251,0,13023,0,0,0,6601,
0,0,0,0,0,0,0,3332,0,0,0,
0,10258,0,2828,0,0,0,13048,0,2563,
0,0,0,4212,0,1367,0,8123,0,
0,0,0,64281,0,27620,0,39294,0,
0,0,2952,0,0,0,0,
10014,0,13273,0,0,0,
3481,0,5188,0,
0,21897,0,51384,
0,0,0,
0,0,
0
)
DIAG_MASKS=(1,2,4,8)
DIAG_NUMS=(1033,0,4463,0)
FACTORIAL=(170,94,29,12,103,78,7,8,3,0,62,30)

CONFIGS={
    11:{
        "primes":(3,5,7,11,13,17),
        "repeated":(7,11),
        "simple":(13,17),
        "C":Fraction(3531,10000),
        "floor_min":35_317_751,
        "floor_slack":7_751,
        "argmin":(1,1,3,3,2,2,1581),
        "exact_argmin":Fraction(1038113041167833283451,2939349364423472000000),
        "special_cost":Fraction(5146853782690471671,536534273587812500),
        "feature_cost":Fraction(5203883011543653,1073068547175625),
        "eta":Fraction(74660174783288691,2146137094351250000),
    },
    13:{
        "primes":(3,5,7,13,17,19),
        "repeated":(7,13),
        "simple":(17,19),
        "C":Fraction(3441,10000),
        "floor_min":34_417_676,
        "floor_slack":7_676,
        "argmin":(4,4,0,0,1,1,1370),
        "exact_argmin":Fraction(14070658945004398641,40882040606680000000),
        "special_cost":Fraction(19983308530450288293,2235736595677812500),
        "feature_cost":Fraction(3758021676155589,894294638271125),
        "eta":Fraction(1236361568367363279,1277563768958750000),
    },
}

UNSELECTED=(3,5,6,7,9,10,11,12,13,14,15)

def _baseline(cfg:dict,mask:int)->Fraction:
    p,q=cfg["repeated"]; r,s=cfg["simple"]
    coords=(Fraction(p+1,p*p),Fraction(q+1,q*q),Fraction(1,r),Fraction(1,s))
    out=Fraction(1)
    for i,x in enumerate(coords):
        if mask&(1<<i): out*=x
    return out

def _rho(q:dict[int,Fraction])->dict[int,Fraction]:
    rho={0:Fraction(1)}
    for size in range(1,5):
        for C in range(1,16):
            if C.bit_count()!=size: continue
            pivot=C&-C; rest=C^pivot
            value=rho[rest]; T=rest
            while True:
                S=pivot|T
                value-=q[S]*rho[C^S]
                if T==0: break
                T=(T-1)&rest
            rho[C]=value
    return rho

def _quadratic_min(linear:Fraction,quadratic:Fraction,lo:Fraction,hi:Fraction)->Fraction:
    x=-linear/(2*quadratic)
    if x<lo: x=lo
    elif x>hi: x=hi
    return linear*x+quadratic*x*x

def pointwise_exact(tag:int,state:tuple[int,...])->Fraction:
    cfg=CONFIGS[tag]
    p1,p2=cfg["repeated"]; s1,s2=cfg["simple"]
    A1,B1,A2,B2,z1,z2,bits=state
    q={
        1:Fraction(p1+1+p1*A1+B1,p1*p1),
        2:Fraction(p2+1+p2*A2+B2,p2*p2),
        4:Fraction(z1,s1),
        8:Fraction(z2,s2),
    }
    for j,m in enumerate(UNSELECTED):
        q[m]=_baseline(cfg,m)*(5 if bits&(1<<j) else 1)
    rho=_rho(q)
    pcoord=Fraction(0)
    full=rho[15]
    for T in range(16):
        sm=1|(T<<1)
        lo=Fraction(6,25)*_baseline(cfg,T)
        hi=5*lo
        pcoord+=LAMBDA.get(sm,Fraction(0))*lo+DIAGONAL[sm]*lo*lo
        full+=_quadratic_min(LAMBDA.get(sm,Fraction(0))-rho[15^T],DIAGONAL[sm],lo,hi)
    value=min(full,min(rho[C] for C in range(1,16))+pcoord)
    value+=sum(Fraction(c,DEN)*q[m] for m,c in enumerate(LINEAR,1) if c)
    value+=sum(Fraction(c,DEN)*q[s]*q[t] for s,t,c in zip(PAIR_S,PAIR_T,PAIR) if c)
    value+=sum(Fraction(c,DEN)*q[m]*q[m] for m,c in zip(DIAG_MASKS,DIAG_NUMS) if c)
    acts=(A1,B1,A2,B2,z1-1,z2-1)
    for j,A in enumerate(acts):
        value+=Fraction(FACTORIAL[2*j],DEN)*A
        value+=Fraction(FACTORIAL[2*j+1],DEN)*comb(A,2)
    return value

def _costs(tag:int)->tuple[Fraction,Fraction]:
    cfg=CONFIGS[tag]
    special=Fraction(0)
    for T in range(16):
        sm=1|(T<<1); b=Fraction(6,25)*_baseline(cfg,T)
        special+=81*LAMBDA.get(sm,Fraction(0))*b+197*DIAGONAL[sm]*b*b
    feature=81*sum(Fraction(c,DEN)*_baseline(cfg,m) for m,c in enumerate(LINEAR,1) if c)
    feature+=197*sum(Fraction(c,DEN)*_baseline(cfg,s)*_baseline(cfg,t) for s,t,c in zip(PAIR_S,PAIR_T,PAIR) if c)
    feature+=197*sum(Fraction(c,DEN)*_baseline(cfg,m)**2 for m,c in zip(DIAG_MASKS,DIAG_NUMS) if c)
    for j in range(6):
        feature+=40*Fraction(FACTORIAL[2*j],DEN)+18*Fraction(FACTORIAL[2*j+1],DEN)
    return special,feature

@lru_cache(maxsize=None)
def reference_audit(tag:int)->dict:
    cfg=CONFIGS[tag]
    assert STATE_COUNT==32_000_000
    assert cfg["floor_min"]-cfg["C"]*Q==cfg["floor_slack"]>0
    exact=pointwise_exact(tag,cfg["argmin"])
    assert exact==cfg["exact_argmin"]>cfg["C"]
    assert Fraction(cfg["floor_min"],Q)<=exact
    special,feature=_costs(tag)
    assert special==cfg["special_cost"]
    assert feature==cfg["feature_cost"]
    eta=41*cfg["C"]-special-feature
    assert eta==cfg["eta"]>0
    return {"tag":tag,"primes":cfg["primes"],"state_count":STATE_COUNT,
            "floor_min":cfg["floor_min"],"floor_slack":cfg["floor_slack"],
            "summed_goodness_margin":eta,"verified":True}

def proof_branch(primes:tuple[int,...])->str:
    primes=tuple(primes)
    if len(primes)!=6 or tuple(sorted(primes))!=primes or len(set(primes))!=6:
        raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p%2 for p in primes):
        raise ValueError("need six odd primes")
    if primes[0]!=3:
        assert all(p>=q for p,q in zip(primes,OFF3))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF3]<1
        return "direct-off3"
    if primes[1]!=5:
        assert all(p>=q for p,q in zip(primes,OFF5))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF5]<1
        return "direct-off5"
    if primes[2]!=7:
        assert all(p>=q for p,q in zip(primes,OFF7))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF7]<1
        return "direct-off7"
    if primes[3] not in (11,13):
        assert primes[3]>=17
        assert all(p>=q for p,q in zip(primes,OFF11_13))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF11_13]<1
        return "direct-off11-13"
    tag=primes[3]
    ref=CONFIGS[tag]["primes"]
    assert primes[:4]==ref[:4]
    assert primes[4]>=ref[4] and primes[5]>=ref[5]
    assert reference_audit(tag)["summed_goodness_margin"]>0
    return f"M68-weighted-{tag}-scale"

@lru_cache(maxsize=1)
def theorem_audit()->dict:
    for a,v in EXPECTED_ANCHORS.items():
        assert direct_bound(a,EXPONENTS)==v<1
    a=reference_audit(11); b=reference_audit(13)
    assert proof_branch((3,5,7,11,13,17))=="M68-weighted-11-scale"
    assert proof_branch((3,5,7,11,31,37))=="M68-weighted-11-scale"
    assert proof_branch((3,5,7,13,17,23))=="M68-weighted-13-scale"
    assert proof_branch(OFF11_13)=="direct-off11-13"
    return {"exponent_placement":EXPONENTS,"weighted_references":(a,b),
            "all_increasing_odd_prime_tuples_noncovering":True,"verified":True}

__all__=["CONFIGS","EXPONENTS","EXPECTED_ANCHORS","FACTORIAL","LINEAR","PAIR",
         "pointwise_exact","proof_branch","reference_audit","theorem_audit"]
