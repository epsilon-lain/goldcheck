"""M66: exact closure of the six-prime exponent profile (4,2,2,1,1,1).

The proof combines three mechanisms.

1. The universal McNew--Setty coordinate monotonicity kills 54 of the 60
   exponent placements at the minimal odd primes.
2. Five coarse reference families are handled by an exact M25-tensor
   *goodness* certificate.  Goodness is the minimum of the full five-coordinate
   rho polynomial and all non-special coordinate polynomials.  Therefore
   positive goodness automatically supplies every Shearer-region hypothesis
   needed for the quantitative completion step, even when a coarse box contains
   bad coordinate-polynomial corners.
3. The two remaining absolute-minimal hard seeds retain the exact two-level
   activation of their repeated non-special singleton (7^2 or 11^2), together
   with exact integral activation levels of the three simple singletons.
   Sparse rational linear/pair/factorial penalties are then certified by
   standalone exact C++ exhaustive verifiers.

This is a six-prime profile theorem, not a solution of the full odd distinct
covering-system problem.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import comb

from m17_infinite_family import is_prime
from m22_universal_direct_zones import universal_monotonicity_gap
from m25_cross_support_seed import CROSS, DIAGONAL, LAMBDA
from m26_minimal_frontier import direct_bound, family_number, sorted_profile
from m28_moment_hierarchy import moment_constant

PROFILE=(4,2,2,1,1,1)
MINIMAL_ODD_PRIMES=(3,5,7,11,13,17)
TAIL=(3,5,7,11,13,19)
OFF3=(5,7,11,13,17,19)
OFF5=(3,7,11,13,17,19)
OFF7=(3,5,11,13,17,19)

A=(4,1,2,1,2,1)
B=(4,1,2,2,1,1)
C1=(4,2,1,1,1,2)
D1=(4,2,1,1,2,1)
EXCEPTIONAL=(4,2,1,2,1,1)
CANONICAL=(4,2,2,1,1,1)
SURVIVING_PLACEMENTS=(A,B,C1,D1,EXCEPTIONAL,CANONICAL)
COARSE_MINIMAL=(A,B,C1,D1)

EXPECTED_SURVIVOR_R={
    A:Fraction(628100908,627161535),
    B:Fraction(33134,33033),
    C1:Fraction(117814,116025),
    D1:Fraction(2410402,2370225),
    EXCEPTIONAL:Fraction(128685584,126351225),
    CANONICAL:Fraction(693908,675675),
}
EXPECTED_MAX_KILLED=((4,1,2,1,1,2),Fraction(273358304,273378105))

J_MASK=0b11110
NON5=tuple(m for m in range(1,32) if not (m&1))
J_SUBSETS=tuple(T for T in range(32) if not (T&~J_MASK))
FIVE=tuple(1|T for T in J_SUBSETS)

# key -> (pointwise C, summed-goodness margin, argmin non-special corner bits)
GOODNESS_EXPECTED={
    ((3, 5, 7, 11, 13, 17),(4, 1, 2, 1, 2, 1)): (Fraction(3695650209289579916161459859,9761525949211890813960000000), Fraction(3313161021563217845565137419,9761525949211890813960000000), 21569),
    ((3, 5, 7, 11, 13, 17),(4, 1, 2, 2, 1, 1)): (Fraction(509896756737700639526207,1344042603384887105700000), Fraction(4468323394404661971598843,17472553844003532374100000), 21569),
    ((3, 5, 7, 11, 13, 17),(4, 2, 1, 1, 1, 2)): (Fraction(22698384661952311969858713,55877182623889586960000000), Fraction(313224687155483157274608273,949912104606122978320000000), 3202),
    ((3, 5, 7, 11, 13, 17),(4, 2, 1, 1, 2, 1)): (Fraction(33979290747376957621883542591,84446928063017020693192000000), Fraction(339453618635931788738350879959,5489050324096106345057480000000), 15228),
    ((3, 5, 7, 11, 13, 19),(4, 2, 1, 2, 1, 1)): (Fraction(188337828714674457787613400929,472455409057319177009520000000), Fraction(1462871206901910203799485621,94491081811463835401904000000), 10854),
}

def _ppx(p:int,a:int)->Fraction:
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))

def _coords(primes:tuple[int,...],exponents:tuple[int,...])->tuple[Fraction,...]:
    return tuple(_ppx(p,a) for p,a in zip(primes[1:],exponents[1:]))

def _baseline(coords:tuple[Fraction,...],mask:int)->Fraction:
    out=Fraction(1)
    for i,x in enumerate(coords):
        if mask&(1<<i): out*=x
    return out

def _rho(q:dict[int,Fraction])->dict[int,Fraction]:
    rho={0:Fraction(1)}
    for size in range(1,5):
        for Cmask in range(32):
            if Cmask&~J_MASK or Cmask.bit_count()!=size:
                continue
            pivot=Cmask&-Cmask
            rest=Cmask^pivot
            value=rho[rest]
            T=rest
            while True:
                S=pivot|T
                value-=q.get(S,Fraction(0))*rho[Cmask^S]
                if T==0: break
                T=(T-1)&rest
            rho[Cmask]=value
    return rho

def _quadratic_min(linear:Fraction,quadratic:Fraction,lo:Fraction,hi:Fraction)->Fraction:
    assert quadratic>0
    x=-linear/(2*quadratic)
    if x<lo: x=lo
    elif x>hi: x=hi
    return linear*x+quadratic*x*x

@lru_cache(maxsize=None)
def goodness_reference_certificate(primes:tuple[int,...],exponents:tuple[int,...])->dict:
    key=(tuple(primes),tuple(exponents))
    if key not in GOODNESS_EXPECTED:
        raise ValueError("not an M66 goodness reference")
    primes,exponents=key
    assert primes[0]==3 and exponents[0]==4
    assert moment_constant(4,1)==81
    assert moment_constant(4,2)==197
    factor=5
    selected=41
    coords=_coords(primes,exponents)
    b={m:_baseline(coords,m) for m in range(1,32)}
    pcoord=sum(
        LAMBDA.get(1|T,Fraction(0))*b[1|T]+DIAGONAL[1|T]*b[1|T]**2
        for T in J_SUBSETS
    )
    best=None
    argmin=None
    for bits in range(1<<len(NON5)):
        q0={m:b[m]*(factor if bits&(1<<i) else 1) for i,m in enumerate(NON5)}
        rho=_rho(q0)
        nonspecial=(
            sum(LAMBDA.get(m,Fraction(0))*q0[m] for m in NON5)
            +sum(mu*q0[s]*q0[t] for (s,t),mu in CROSS.items())
        )
        full_branch=rho[J_MASK]
        for T in J_SUBSETS:
            m=1|T
            linear=LAMBDA.get(m,Fraction(0))-rho[J_MASK^T]
            full_branch+=_quadratic_min(linear,DIAGONAL[m],b[m],factor*b[m])
        coordinate_branch=min(v for Cmask,v in rho.items() if Cmask!=0)+pcoord
        value=nonspecial+min(full_branch,coordinate_branch)
        if best is None or value<best:
            best=value
            argmin=bits
    assert best is not None and argmin is not None
    margin=(
        selected*best
        -81*sum(LAMBDA.get(m,Fraction(0))*b[m] for m in range(1,32))
        -197*sum(DIAGONAL[m]*b[m]**2 for m in FIVE)
        -197*sum(mu*b[s]*b[t] for (s,t),mu in CROSS.items())
    )
    eC,eM,eA=GOODNESS_EXPECTED[key]
    assert best==eC
    assert margin==eM>0
    assert argmin==eA
    return {
        "primes":primes,
        "exponents":exponents,
        "C":best,
        "summed_goodness_margin":margin,
        "argmin_bits":argmin,
        "verified":True,
    }

WEIGHTED={
    "canonical":{
        "primes":MINIMAL_ODD_PRIMES,
        "exponents":CANONICAL,
        "p0":7,
        "D":(49,11,13,17),
        "N":(8,1,1,1),
        "linear":{3:306, 5:256, 6:216, 7:339, 9:215, 10:228, 11:358, 12:211, 13:350, 14:199},
        "cross":{(1, 3):338, (1, 5):389, (1, 9):384, (2, 6):260, (3, 5):60, (3, 7):3079, (3, 9):184, (3, 10):312, (3, 11):1655, (3, 14):1277, (4, 12):12, (5, 7):2719, (5, 9):450, (6, 10):672, (7, 9):1040, (7, 12):10660, (9, 10):331, (9, 11):2885, (10, 13):11844, (11, 13):55709, (12, 14):7353},
        "factorial":(22, 16, 2, 3, 11, 6, 9, 4, 6, 3),
        "C":Fraction(1697,5000),
        "Q":10**7,
        "floor_min":3396094,
        "floor_slack":2094,
        "argmin":(3,3,1,1,1,1299),
        "exact_argmin":Fraction(51001982532390154600661059,150177322295567550984000000),
        "special_cost":Fraction(10474107609241998,1108541887578125),
        "feature_cost":Fraction(61248773103499,14189336161000),
        "eta":Fraction(666543097807133,4434167550312500),
    },
    "exceptional":{
        "primes":MINIMAL_ODD_PRIMES,
        "exponents":EXCEPTIONAL,
        "p0":11,
        "D":(121,7,13,17),
        "N":(12,1,1,1),
        "linear":{3:323, 5:175, 6:292, 7:271, 9:179, 10:197, 11:530, 12:191, 13:229, 14:207},
        "cross":{(1, 3):26, (1, 5):274, (1, 9):405, (2, 3):303, (2, 6):265, (2, 10):377, (2, 14):108, (3, 5):124, (3, 6):1, (3, 7):2096, (5, 6):221, (5, 7):7597, (5, 9):97, (5, 13):8000, (5, 14):6863, (6, 10):204, (6, 12):1067, (6, 14):1597, (7, 9):3173, (7, 10):3783, (7, 13):2047, (8, 12):54, (10, 12):450, (10, 14):7663, (11, 12):15, (12, 13):2292, (12, 15):130488},
        "factorial":(12, 6, 1, 1, 18, 17, 8, 5, 7, 3),
        "C":Fraction(1701,5000),
        "Q":10**7,
        "floor_min":3404158,
        "floor_slack":2158,
        "argmin":(1,1,3,3,2,1127),
        "exact_argmin":Fraction(20420576104903183899,59986721722928000000),
        "special_cost":Fraction(25090870341171861,2737419763203125),
        "feature_cost":Fraction(10007575113113,2502783783500),
        "eta":Fraction(17163381759764987,21899358105625000),
    },
}

_LOCAL_UNSELECTED=(3,5,6,7,9,10,11,12,13,14,15)

def _local_baseline(cfg:dict,mask:int)->Fraction:
    out=Fraction(1)
    for i,(n,d) in enumerate(zip(cfg["N"],cfg["D"])):
        if mask&(1<<i): out*=Fraction(n,d)
    return out

def _local_q(cfg:dict,state:tuple[int,...])->dict[int,Fraction]:
    A0,B0,z1,z2,z3,bits=state
    p0=cfg["p0"]
    D=cfg["D"]
    N=cfg["N"]
    q={
        1:Fraction(N[0]+p0*A0+B0,D[0]),
        2:Fraction(z1*N[1],D[1]),
        4:Fraction(z2*N[2],D[2]),
        8:Fraction(z3*N[3],D[3]),
    }
    for j,m in enumerate(_LOCAL_UNSELECTED):
        q[m]=_local_baseline(cfg,m)*(5 if bits&(1<<j) else 1)
    return q

def _local_rho(q:dict[int,Fraction])->dict[int,Fraction]:
    rho={0:Fraction(1)}
    for size in range(1,5):
        for Cmask in range(1,16):
            if Cmask.bit_count()!=size: continue
            pivot=Cmask&-Cmask
            rest=Cmask^pivot
            value=rho[rest]
            T=rest
            while True:
                S=pivot|T
                value-=q[S]*rho[Cmask^S]
                if T==0: break
                T=(T-1)&rest
            rho[Cmask]=value
    return rho

def weighted_pointwise_exact(name:str,state:tuple[int,...])->Fraction:
    cfg=WEIGHTED[name]
    q=_local_q(cfg,state)
    rho=_local_rho(q)
    pcoord=Fraction(0)
    full=rho[15]
    for T in range(16):
        sm=1|(T<<1)
        lo=Fraction(6,25)*_local_baseline(cfg,T)
        hi=5*lo
        pcoord+=LAMBDA.get(sm,Fraction(0))*lo+DIAGONAL[sm]*lo**2
        linear=LAMBDA.get(sm,Fraction(0))-rho[15^T]
        full+=_quadratic_min(linear,DIAGONAL[sm],lo,hi)
    coordinate=min(rho[Cmask] for Cmask in range(1,16))+pcoord
    value=min(full,coordinate)
    value+=sum(Fraction(c,1000)*q[m] for m,c in cfg["linear"].items())
    value+=sum(Fraction(c,1000)*q[s]*q[t] for (s,t),c in cfg["cross"].items())
    acts=(state[0],state[1],state[2]-1,state[3]-1,state[4]-1)
    fac=cfg["factorial"]
    for j,Aact in enumerate(acts):
        value+=Fraction(fac[2*j],1000)*Aact
        value+=Fraction(fac[2*j+1],1000)*comb(Aact,2)
    return value

def _weighted_special_cost(cfg:dict)->Fraction:
    out=Fraction(0)
    for T in range(16):
        sm=1|(T<<1)
        b=Fraction(6,25)*_local_baseline(cfg,T)
        out+=81*LAMBDA.get(sm,Fraction(0))*b
        out+=197*DIAGONAL[sm]*b*b
    return out

def _weighted_feature_cost(cfg:dict)->Fraction:
    out=81*sum(Fraction(c,1000)*_local_baseline(cfg,m) for m,c in cfg["linear"].items())
    out+=197*sum(
        Fraction(c,1000)*_local_baseline(cfg,s)*_local_baseline(cfg,t)
        for (s,t),c in cfg["cross"].items()
    )
    assert moment_constant(4,1)==81 and moment_constant(4,2)==197
    fac=cfg["factorial"]
    for j in range(5):
        out+=40*Fraction(fac[2*j],1000)+18*Fraction(fac[2*j+1],1000)
    return out

@lru_cache(maxsize=None)
def weighted_certificate_audit(name:str)->dict:
    cfg=WEIGHTED[name]
    assert cfg["floor_min"]-cfg["C"]*cfg["Q"]==cfg["floor_slack"]>0
    exact=weighted_pointwise_exact(name,cfg["argmin"])
    assert exact==cfg["exact_argmin"]>cfg["C"]
    assert Fraction(cfg["floor_min"],cfg["Q"])<=exact
    assert _weighted_special_cost(cfg)==cfg["special_cost"]
    assert _weighted_feature_cost(cfg)==cfg["feature_cost"]
    eta=41*cfg["C"]-cfg["special_cost"]-cfg["feature_cost"]
    assert eta==cfg["eta"]>0
    return {
        "name":name,
        "N":family_number(cfg["primes"],cfg["exponents"]),
        "state_count":5**5*2**11,
        "floor_min_scaled":cfg["floor_min"],
        "floor_slack_scaled":cfg["floor_slack"],
        "argmin":cfg["argmin"],
        "exact_argmin_value":exact,
        "summed_goodness_margin":eta,
        "noncovering_certified":True,
    }

def placement_scan()->dict:
    assert universal_monotonicity_gap()>0
    assignments=tuple(sorted(set(permutations(PROFILE))))
    values={a:direct_bound(MINIMAL_ODD_PRIMES,a) for a in assignments}
    survivors=tuple(a for a in assignments if values[a]>=1)
    assert len(assignments)==60
    assert set(survivors)==set(SURVIVING_PLACEMENTS)
    assert {a:values[a] for a in survivors}==EXPECTED_SURVIVOR_R
    killed={a:v for a,v in values.items() if a not in survivors}
    amax=max(killed,key=killed.get)
    assert (amax,killed[amax])==EXPECTED_MAX_KILLED
    for a in survivors:
        assert direct_bound(OFF3,a)<1
    return {
        "assignment_count":60,
        "surviving_placements":survivors,
        "directly_killed_placement_count":54,
        "max_killed_R":killed[amax],
        "verified":True,
    }

def _scale_check(primes:tuple[int,...],exponents:tuple[int,...],ref_primes:tuple[int,...])->None:
    actual=_coords(primes,exponents)
    ref=_coords(ref_primes,exponents)
    assert all(x<=y for x,y in zip(actual,ref))
    for m in (1,2,3,7,15,31):
        b=_baseline(actual,m)
        bbar=_baseline(ref,m)
        gamma=bbar/b
        assert gamma>=1 and gamma*b==bbar

def proof_branch(primes:tuple[int,...],exponents:tuple[int,...])->str:
    primes=tuple(primes);exponents=tuple(exponents)
    if len(primes)!=6 or tuple(sorted(primes))!=primes or len(set(primes))!=6:
        raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p%2 for p in primes):
        raise ValueError("need six distinct odd primes")
    if sorted_profile(exponents)!=PROFILE:
        raise ValueError("wrong exponent profile")
    assert universal_monotonicity_gap()>0

    if exponents not in SURVIVING_PLACEMENTS:
        base=direct_bound(MINIMAL_ODD_PRIMES,exponents)
        assert base<1 and direct_bound(primes,exponents)<=base
        return "McNew-Setty-placement"

    if primes[0]!=3:
        assert all(p>=q for p,q in zip(primes,OFF3))
        assert direct_bound(primes,exponents)<=direct_bound(OFF3,exponents)<1
        return "McNew-Setty-off3"

    if exponents in COARSE_MINIMAL:
        cert=goodness_reference_certificate(MINIMAL_ODD_PRIMES,exponents)
        _scale_check(primes,exponents,MINIMAL_ODD_PRIMES)
        assert cert["summed_goodness_margin"]>0
        return "M66-goodness-minimal-scale"

    if exponents==EXCEPTIONAL:
        if primes==MINIMAL_ODD_PRIMES:
            assert weighted_certificate_audit("exceptional")["noncovering_certified"]
            return "M66-weighted-11-square"
        assert all(p>=q for p,q in zip(primes,TAIL))
        cert=goodness_reference_certificate(TAIL,EXCEPTIONAL)
        _scale_check(primes,EXCEPTIONAL,TAIL)
        assert cert["summed_goodness_margin"]>0
        return "M66-goodness-exceptional-tail"

    assert exponents==CANONICAL
    if primes[1]!=5:
        assert all(p>=q for p,q in zip(primes,OFF5))
        assert direct_bound(primes,CANONICAL)<=direct_bound(OFF5,CANONICAL)<1
        return "McNew-Setty-canonical-off5"
    if primes[2]!=7:
        assert all(p>=q for p,q in zip(primes,OFF7))
        assert direct_bound(primes,CANONICAL)<=direct_bound(OFF7,CANONICAL)<1
        return "McNew-Setty-canonical-off7"

    assert primes[:3]==(3,5,7)
    assert weighted_certificate_audit("canonical")["noncovering_certified"]
    return "M66-weighted-7-square-scale"

@lru_cache(maxsize=1)
def theorem_audit()->dict:
    scan=placement_scan()
    refs={key:goodness_reference_certificate(*key) for key in GOODNESS_EXPECTED}
    assert all(c["summed_goodness_margin"]>0 for c in refs.values())
    wc=weighted_certificate_audit("canonical")
    we=weighted_certificate_audit("exceptional")
    assert proof_branch(MINIMAL_ODD_PRIMES,CANONICAL)=="M66-weighted-7-square-scale"
    assert proof_branch(MINIMAL_ODD_PRIMES,EXCEPTIONAL)=="M66-weighted-11-square"
    assert proof_branch(TAIL,EXCEPTIONAL)=="M66-goodness-exceptional-tail"
    assert proof_branch(MINIMAL_ODD_PRIMES,A)=="M66-goodness-minimal-scale"
    return {
        "profile":PROFILE,
        "placement_scan":scan,
        "goodness_reference_count":len(refs),
        "weighted_certificates":(wc,we),
        "all_odd_six_prime_numbers_with_profile_noncovering":True,
        "verified":True,
    }

__all__=[
    "CANONICAL","EXCEPTIONAL","GOODNESS_EXPECTED","PROFILE","SURVIVING_PLACEMENTS",
    "WEIGHTED","goodness_reference_certificate","placement_scan","proof_branch",
    "theorem_audit","weighted_certificate_audit","weighted_pointwise_exact",
]
