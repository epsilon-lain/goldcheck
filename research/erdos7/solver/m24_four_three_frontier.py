"""M24: exact reduction of the six-prime (4,3,1,1,1,1) profile to one seed.

Everything in this module is exact Fraction arithmetic.  It combines:

* the universal coordinate monotonicity from M22;
* a new factor-4 affine Clique-Shearer certificate for the swapped placement
  3^3*5^4;
* the M16 diagonal second-moment certificate on the a=4 side;
* a new all-five-support diagonal quadratic certificate for P=19.

The only profile member not excluded here is

    3^4 * 5^3 * 7 * 11 * 13 * 17 = 172297125.

This is a frontier reduction, not a proof that the remaining seed covers.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import permutations

from m14_clique_shearer import J_MASK, coordinate_rhos
from m16_quadratic_frontier import LAMBDA as M16_LAMBDA, MU as M16_MU
from m17_infinite_family import elementary_symmetric, is_prime
from m22_universal_direct_zones import universal_monotonicity_gap

MINIMAL_ODD_PRIMES=(3,5,7,11,13,17)
PROFILE=(4,3,1,1,1,1)
CANONICAL_43=(4,3,1,1,1,1)
SWAPPED_34=(3,4,1,1,1,1)
DIRECT_EXCEPTIONAL_PLACEMENTS=(CANONICAL_43,SWAPPED_34)
NONEXCEPTIONAL_MAX_ASSIGNMENT=(4,1,3,1,1,1)
NONEXCEPTIONAL_MAX_R=Fraction(112558664,112567455)
REMAINING_P=17
REMAINING_N=172297125

# Swapped 3^3*5^4 factor-4 affine certificate.
AFFINE_34_LAMBDA={
    1:Fraction(1067,2000),2:Fraction(3827,10000),3:Fraction(3869,5000),
    4:Fraction(1369,5000),5:Fraction(361,500),6:Fraction(4969,10000),
    7:Fraction(8643,10000),8:Fraction(243,1000),9:Fraction(3541,5000),
    10:Fraction(607,1250),11:Fraction(8503,10000),12:Fraction(1109,2500),
    13:Fraction(7983,10000),14:Fraction(1729,2500),15:Fraction(2353,2500),
    16:Fraction(2087,10000),17:Fraction(6903,10000),18:Fraction(4321,10000),
    19:Fraction(4161,5000),20:Fraction(983,2500),21:Fraction(3901,5000),
    22:Fraction(1347,2000),23:Fraction(9231,10000),24:Fraction(1771,5000),
    25:Fraction(3831,5000),26:Fraction(1319,2000),27:Fraction(9091,10000),
    28:Fraction(243,400),29:Fraction(8571,10000),30:Fraction(469,625),31:Fraction(1),
}
AFFINE_34_EXPECTED={
    17:(Fraction(781125021,1168750000),Fraction(5263011241,15193750000),Fraction(12690063,3038750000),Fraction(941,17017)),
    19:(Fraction(7176048177,10806250000),Fraction(3133586711,9143750000),Fraction(274867563,6256250000),Fraction(61,1001)),
    23:(Fraction(18928670679,28778750000),Fraction(882322261,2616250000),Fraction(227052153,2213750000),Fraction(145,2093)),
}

# New P=19 diagonal quadratic certificate on the hard 3^4*5^3 side.
P19_LAMBDA={
    1:Fraction(0),2:Fraction(807,2500),3:Fraction(7799,10000),4:Fraction(2147,10000),
    5:Fraction(1359,5000),6:Fraction(3117,5000),7:Fraction(544,625),8:Fraction(1873,10000),
    9:Fraction(1957,10000),10:Fraction(3961,10000),11:Fraction(1713,2000),12:Fraction(1931,5000),
    13:Fraction(943,1250),14:Fraction(3497,5000),15:Fraction(9473,10000),16:Fraction(29,200),
    17:Fraction(2691,10000),18:Fraction(5859,10000),19:Fraction(8321,10000),20:Fraction(1339,5000),
    21:Fraction(7457,10000),22:Fraction(6751,10000),23:Fraction(923,1000),24:Fraction(2573,10000),
    25:Fraction(1843,2500),26:Fraction(5573,10000),27:Fraction(909,1000),28:Fraction(513,1000),
    29:Fraction(2143,2500),30:Fraction(7521,10000),31:Fraction(4999,5000),
}
P19_DIAGONAL_MU={
    1:Fraction(4149,10000),3:Fraction(0),5:Fraction(16599,5000),7:Fraction(1,2500),
    9:Fraction(4481,1000),11:Fraction(3,10000),13:Fraction(5),15:Fraction(647,10000),
    17:Fraction(5),19:Fraction(19,10000),21:Fraction(5),23:Fraction(329,5000),
    25:Fraction(5),27:Fraction(457,2500),29:Fraction(0),31:Fraction(5),
}
P19_EXPECTED={
    "C":Fraction(332935515406714654293261,716769366014702000000000),
    "lambda_b":Fraction(772647693,4754750000),
    "mu_b2":Fraction(59981359082643,2018539960937500),
    "margin":Fraction(1098589626561579134109123,39422315130808610000000000),
    "proper_non5_min":Fraction(1,91),
    "full_non5_min":Fraction(-236,19019),
    "completion_upper_max":Fraction(-23641,2377375),
}

# Direct one-parameter bridges.
A34=Fraction(5498761,5630625)
B34=Fraction(1377221,2413125)
THRESHOLD34=Fraction(9640547,395592)
R34_29=Fraction(44366614,44533125)
A43=Fraction(9995309,10135125)
B43=Fraction(163387,289575)
THRESHOLD43=Fraction(5718545,139816)
R43_41=Fraction(138508738,138513375)

# Direct monotone anchors.
OFFBASE_34=Fraction(139011214,157594437)
OFFFAMILY_34=Fraction(417922976,419698125)
OFFBASE_43=Fraction(1146071594,1283268987)
ANCHOR_43_7_13=Fraction(59303774,59520825)
ANCHOR_43_7_11_17_23=Fraction(101590976,101611125)

M16_HARD_MARGINS={
    (7,11,13,23):Fraction(2134682349002381,29351626992187500),
    (7,11,13,29):Fraction(1238712960918459209,4246331503476562500),
    (7,11,13,31):Fraction(1675429219652823839,4852228983164062500),
    (7,11,13,37):Fraction(464467129271395583,987468630585937500),
    (7,11,17,19):Fraction(63976862971583,200798554687500),
}
M16_HARD_COMPLETION_MAX={
    (7,11,13,23):Fraction(-34633,2877875),
    (7,11,13,29):Fraction(-7303,518375),
    (7,11,13,31):Fraction(-5147,352625),
    (7,11,13,37):Fraction(-14621,925925),
    (7,11,17,19):Fraction(-46369,3108875),
}

NON5_MASKS=tuple(m for m in range(1,32) if not (m&1))
J_SUBSETS=tuple(T for T in range(32) if not (T&~J_MASK))
FIVE_MASKS=tuple(1|T for T in J_SUBSETS)


def prime_power_x(p:int,a:int)->Fraction:
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))


def direct_bound(primes:tuple[int,...],exponents:tuple[int,...])->Fraction:
    xs=tuple(prime_power_x(p,a) for p,a in zip(primes,exponents))
    return (elementary_symmetric(xs,1)-elementary_symmetric(xs,3)
            -elementary_symmetric(xs,4)+2*elementary_symmetric(xs,5)
            +9*elementary_symmetric(xs,6))


def baseline_from_coordinates(coords:tuple[Fraction,...])->dict[int,Fraction]:
    if len(coords)!=5: raise ValueError("need five post-3 coordinates")
    out={}
    for mask in range(1,32):
        value=Fraction(1)
        for i,x in enumerate(coords):
            if mask&(1<<i): value*=x
        out[mask]=value
    return out


def _clip(x:Fraction,lo:Fraction,hi:Fraction)->Fraction:
    return min(max(x,lo),hi)


def assignment_scan()->dict:
    assignments=tuple(sorted(set(permutations(PROFILE))))
    assert len(assignments)==30
    values={a:direct_bound(MINIMAL_ODD_PRIMES,a) for a in assignments}
    exceptions=tuple(a for a in assignments if values[a]>=1)
    assert exceptions==DIRECT_EXCEPTIONAL_PLACEMENTS
    others={a:v for a,v in values.items() if a not in exceptions}
    amax=max(others,key=others.get)
    vmax=others[amax]
    assert amax==NONEXCEPTIONAL_MAX_ASSIGNMENT
    assert vmax==NONEXCEPTIONAL_MAX_R<1
    assert 1-vmax==Fraction(8791,112567455)
    return {"assignment_count":30,"direct_exceptions":exceptions,
            "nonexceptional_max_assignment":amax,"nonexceptional_max_R":vmax}


@lru_cache(maxsize=None)
def affine_34_certificate(P:int)->dict:
    if P not in AFFINE_34_EXPECTED: raise ValueError("P must be 17,19,23")
    b=baseline_from_coordinates((Fraction(156,625),Fraction(1,7),Fraction(1,11),Fraction(1,13),Fraction(1,P)))
    best=None; clique_min=None
    for bits in range(1<<len(NON5_MASKS)):
        q0={m:b[m]*(4 if bits&(1<<idx) else 1) for idx,m in enumerate(NON5_MASKS)}
        rho=coordinate_rhos(q0,J_MASK)
        local=min(rho.values())
        if clique_min is None or local<clique_min: clique_min=local
        value=rho[J_MASK]+sum(AFFINE_34_LAMBDA[m]*q0[m] for m in NON5_MASKS)
        for T in J_SUBSETS:
            mask=1|T
            coeff=AFFINE_34_LAMBDA[mask]-rho[J_MASK^T]
            q=b[mask]*(4 if coeff<0 else 1)
            value+=coeff*q
        if best is None or value<best: best=value
    assert best is not None and clique_min is not None
    lambda_b=sum(AFFINE_34_LAMBDA[s]*b[s] for s in range(1,32))
    margin=14*best-27*lambda_b
    exp=AFFINE_34_EXPECTED[P]
    assert (best,lambda_b,margin,clique_min)==exp
    assert clique_min>0 and margin>0
    return {"P":P,"C":best,"lambda_b":lambda_b,"margin":margin,
            "non5_clique_min":clique_min,"noncovering_certified":True}


def direct_family_34(P:int)->Fraction:
    return A34+B34/P


def direct_family_43(P:int)->Fraction:
    return A43+B43/P


@lru_cache(maxsize=None)
def diagonal_certificate(simple_primes:tuple[int,int,int,int],kind:str)->dict:
    """Exact factor-5 diagonal quadratic certificate for one a=4 base.

    ``kind='m16'`` uses the old M16 q_{5}^2 penalty only.
    ``kind='p19'`` uses the new 16 diagonal penalties.
    """
    if len(simple_primes)!=4: raise ValueError("need four simple primes")
    if kind=="m16":
        L=M16_LAMBDA
        Mus={1:M16_MU}
    elif kind=="p19":
        if simple_primes!=(7,11,13,19): raise ValueError("p19 certificate has one certified base")
        L=P19_LAMBDA
        Mus=P19_DIAGONAL_MU
    else:
        raise ValueError("unknown certificate kind")

    b=baseline_from_coordinates((Fraction(31,125),)+tuple(Fraction(1,p) for p in simple_primes))
    best=None; proper_min=None; full_min=None; completion_max=None
    alpha=5*b[1]-1
    for bits in range(1<<len(NON5_MASKS)):
        q0={m:b[m]*(5 if bits&(1<<idx) else 1) for idx,m in enumerate(NON5_MASKS)}
        rho=coordinate_rhos(q0,J_MASK)
        for Cmask,value in rho.items():
            if Cmask==J_MASK:
                if full_min is None or value<full_min: full_min=value
            else:
                if proper_min is None or value<proper_min: proper_min=value
        completion=-alpha*rho[J_MASK]-sum(b[1|T]*rho[J_MASK^T] for T in J_SUBSETS if T)
        if completion_max is None or completion>completion_max: completion_max=completion

        value=rho[J_MASK]+sum(L[m]*q0[m] for m in NON5_MASKS)
        for T in J_SUBSETS:
            mask=1|T
            coeff=L[mask]-rho[J_MASK^T]
            mu=Mus.get(mask,Fraction(0))
            lo,hi=b[mask],5*b[mask]
            if mu:
                q=_clip(-coeff/(2*mu),lo,hi)
            else:
                q=hi if coeff<0 else lo
            value+=coeff*q+mu*q*q
        if best is None or value<best: best=value

    assert best is not None and proper_min is not None and full_min is not None and completion_max is not None
    lambda_b=sum(L[s]*b[s] for s in range(1,32))
    mu_b2=sum(Mus.get(s,Fraction(0))*b[s]*b[s] for s in FIVE_MASKS)
    margin=41*best-81*lambda_b-197*mu_b2
    assert proper_min>0 and completion_max<0 and margin>0

    if kind=="p19":
        exp=P19_EXPECTED
        assert best==exp["C"] and lambda_b==exp["lambda_b"] and mu_b2==exp["mu_b2"]
        assert margin==exp["margin"] and proper_min==exp["proper_non5_min"]
        assert full_min==exp["full_non5_min"] and completion_max==exp["completion_upper_max"]
    else:
        assert simple_primes in M16_HARD_MARGINS
        assert margin==M16_HARD_MARGINS[simple_primes]
        assert completion_max==M16_HARD_COMPLETION_MAX[simple_primes]

    return {"simple_primes":simple_primes,"kind":kind,"C":best,"lambda_b":lambda_b,
            "mu_b2":mu_b2,"margin":margin,"proper_non5_min":proper_min,
            "full_non5_min":full_min,"completion_upper_max":completion_max,
            "noncovering_certified":True}


def _ordered(primes:tuple[int,...],exponents:tuple[int,...])->tuple[tuple[int,...],tuple[int,...]]:
    if len(primes)!=6 or len(exponents)!=6: raise ValueError("need six coordinates")
    if len(set(primes))!=6 or not all(is_prime(p) and p%2 for p in primes):
        raise ValueError("six distinct odd primes required")
    if tuple(sorted(exponents,reverse=True))!=PROFILE: raise ValueError("wrong exponent profile")
    pairs=sorted(zip(primes,exponents))
    return tuple(p for p,_ in pairs),tuple(a for _,a in pairs)


def proof_branch(primes:tuple[int,...],exponents:tuple[int,...])->str:
    primes,exponents=_ordered(primes,exponents)
    assert universal_monotonicity_gap()>0

    if exponents not in DIRECT_EXCEPTIONAL_PLACEMENTS:
        base=direct_bound(MINIMAL_ODD_PRIMES,exponents)
        assert base<=NONEXCEPTIONAL_MAX_R<1
        assert direct_bound(primes,exponents)<=base
        return "McNew-Setty-nonexceptional-placement"

    if primes[:2]!=(3,5):
        anchor=(3,7,11,13,17,19)
        value=OFFBASE_43 if exponents==CANONICAL_43 else OFFBASE_34
        assert direct_bound(anchor,exponents)==value<1
        assert all(p>=q for p,q in zip(primes,anchor))
        assert direct_bound(primes,exponents)<=value
        return "McNew-Setty-offbase-repeated-primes"

    simples=primes[2:]
    if exponents==SWAPPED_34:
        if simples[:3]==(7,11,13):
            P=simples[3]
            if P in AFFINE_34_EXPECTED:
                assert affine_34_certificate(P)["noncovering_certified"] is True
                return "M24-affine-3^3-5^4"
            assert P>=29 and direct_family_34(P)<=R34_29<1
            return "McNew-Setty-3^3-5^4-tail"
        anchor=(3,5,7,11,17,19)
        assert direct_bound(anchor,SWAPPED_34)==OFFFAMILY_34<1
        assert all(p>=q for p,q in zip(primes,anchor))
        assert direct_bound(primes,exponents)<=OFFFAMILY_34
        return "McNew-Setty-3^3-5^4-offfamily"

    # Hard orientation: 3^4*5^3 times four simple primes.
    assert exponents==CANONICAL_43
    if simples[0]>=11:
        anchor=(3,5,11,13,17,19)
        value=direct_bound(anchor,CANONICAL_43)
        assert value==Fraction(1511818,1574625)<1
        assert direct_bound(primes,exponents)<=value
        return "McNew-Setty-43-first-simple-large"
    if simples[1]>=13:
        anchor=(3,5,7,13,17,19)
        assert direct_bound(anchor,CANONICAL_43)==ANCHOR_43_7_13<1
        assert direct_bound(primes,exponents)<=ANCHOR_43_7_13
        return "McNew-Setty-43-second-simple-large"

    assert simples[:2]==(7,11)
    if simples[2]==13:
        P=simples[3]
        if P==17:
            return "M24-remaining-seed"
        if P==19:
            assert diagonal_certificate((7,11,13,19),"p19")["noncovering_certified"] is True
            return "M24-P19-diagonal"
        if P in (23,29,31,37):
            assert diagonal_certificate((7,11,13,P),"m16")["noncovering_certified"] is True
            return "M16-quadratic-generalized-base"
        assert P>=41 and direct_family_43(P)<=R43_41<1
        return "McNew-Setty-43-tail"

    assert simples[2]>=17
    if simples==(7,11,17,19):
        assert diagonal_certificate(simples,"m16")["noncovering_certified"] is True
        return "M16-quadratic-offfamily"
    anchor=(3,5,7,11,17,23)
    assert simples[3]>=23
    assert direct_bound(anchor,CANONICAL_43)==ANCHOR_43_7_11_17_23<1
    assert direct_bound(primes,exponents)<=ANCHOR_43_7_11_17_23
    return "McNew-Setty-43-third-simple-large"


def m24_audit()->dict:
    scan=assignment_scan()
    assert universal_monotonicity_gap()==Fraction(719,1440)>0

    assert THRESHOLD34==B34/(1-A34) and 24<THRESHOLD34<29
    assert direct_family_34(29)==R34_29<1
    for P in (17,19,23): assert affine_34_certificate(P)["margin"]>0

    assert THRESHOLD43==B43/(1-A43) and 40<THRESHOLD43<41
    assert direct_family_43(41)==R43_41<1
    for P in (23,29,31,37): assert diagonal_certificate((7,11,13,P),"m16")["margin"]>0
    assert diagonal_certificate((7,11,17,19),"m16")["margin"]>0
    assert diagonal_certificate((7,11,13,19),"p19")["margin"]>0

    assert proof_branch((3,5,7,11,13,17),CANONICAL_43)=="M24-remaining-seed"
    assert proof_branch((3,5,7,11,13,19),CANONICAL_43)=="M24-P19-diagonal"
    assert proof_branch((3,5,7,11,13,23),CANONICAL_43)=="M16-quadratic-generalized-base"
    assert proof_branch((3,5,7,11,13,41),CANONICAL_43)=="McNew-Setty-43-tail"
    assert proof_branch((3,5,7,11,17,19),CANONICAL_43)=="M16-quadratic-offfamily"
    assert proof_branch((3,5,7,11,17,23),CANONICAL_43)=="McNew-Setty-43-third-simple-large"
    assert proof_branch((3,5,7,11,13,17),SWAPPED_34)=="M24-affine-3^3-5^4"

    return {**scan,
            "profile":PROFILE,
            "remaining_seed":REMAINING_N,
            "remaining_prime_tuple":MINIMAL_ODD_PRIMES,
            "remaining_exponents":CANONICAL_43,
            "all_other_profile_members_excluded":True,
            "profile_fully_excluded":False}


__all__=[
    "AFFINE_34_EXPECTED","AFFINE_34_LAMBDA","CANONICAL_43","P19_DIAGONAL_MU",
    "P19_EXPECTED","P19_LAMBDA","PROFILE","REMAINING_N","REMAINING_P","SWAPPED_34",
    "affine_34_certificate","assignment_scan","diagonal_certificate","direct_bound",
    "direct_family_34","direct_family_43","m24_audit","proof_branch",
]
