"""M24: reduce the six-prime exponent profile (4,3,1,1,1,1) to one seed.

Exact Fraction arithmetic only.  The only member of this profile not excluded
here is

    3^4 * 5^3 * 7 * 11 * 13 * 17 = 172297125.

This is a reduction, not a claim that the remaining seed covers.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import permutations

from m14_clique_shearer import J_MASK, coordinate_rhos
from m16_quadratic_frontier import LAMBDA as M16_LAMBDA, MU as M16_MU
from m17_infinite_family import elementary_symmetric
from m22_universal_direct_zones import universal_monotonicity_gap

PROFILE=(4,3,1,1,1,1)
CANONICAL_43=(4,3,1,1,1,1)
SWAPPED_34=(3,4,1,1,1,1)
EXCEPTIONAL=tuple(sorted((CANONICAL_43,SWAPPED_34)))
MIN_PRIMES=(3,5,7,11,13,17)
REMAINING_N=172297125

NONEXCEPTIONAL_MAX_ASSIGNMENT=(4,1,3,1,1,1)
NONEXCEPTIONAL_MAX_R=Fraction(112558664,112567455)

NON5=tuple(m for m in range(1,32) if not (m&1))
JSUBS=tuple(t for t in range(32) if not (t&~J_MASK))
FIVE=tuple(1|t for t in JSUBS)

AFFINE34={
1:Fraction(1067,2000),2:Fraction(3827,10000),3:Fraction(3869,5000),4:Fraction(1369,5000),
5:Fraction(361,500),6:Fraction(4969,10000),7:Fraction(8643,10000),8:Fraction(243,1000),
9:Fraction(3541,5000),10:Fraction(607,1250),11:Fraction(8503,10000),12:Fraction(1109,2500),
13:Fraction(7983,10000),14:Fraction(1729,2500),15:Fraction(2353,2500),16:Fraction(2087,10000),
17:Fraction(6903,10000),18:Fraction(4321,10000),19:Fraction(4161,5000),20:Fraction(983,2500),
21:Fraction(3901,5000),22:Fraction(1347,2000),23:Fraction(9231,10000),24:Fraction(1771,5000),
25:Fraction(3831,5000),26:Fraction(1319,2000),27:Fraction(9091,10000),28:Fraction(243,400),
29:Fraction(8571,10000),30:Fraction(469,625),31:Fraction(1),
}
AFFINE34_EXPECTED={
17:(Fraction(781125021,1168750000),Fraction(5263011241,15193750000),Fraction(12690063,3038750000),Fraction(941,17017)),
19:(Fraction(7176048177,10806250000),Fraction(3133586711,9143750000),Fraction(274867563,6256250000),Fraction(61,1001)),
23:(Fraction(18928670679,28778750000),Fraction(882322261,2616250000),Fraction(227052153,2213750000),Fraction(145,2093)),
}

P19_LAMBDA={
1:Fraction(0),2:Fraction(807,2500),3:Fraction(7799,10000),4:Fraction(2147,10000),5:Fraction(1359,5000),
6:Fraction(3117,5000),7:Fraction(544,625),8:Fraction(1873,10000),9:Fraction(1957,10000),10:Fraction(3961,10000),
11:Fraction(1713,2000),12:Fraction(1931,5000),13:Fraction(943,1250),14:Fraction(3497,5000),15:Fraction(9473,10000),
16:Fraction(29,200),17:Fraction(2691,10000),18:Fraction(5859,10000),19:Fraction(8321,10000),20:Fraction(1339,5000),
21:Fraction(7457,10000),22:Fraction(6751,10000),23:Fraction(923,1000),24:Fraction(2573,10000),25:Fraction(1843,2500),
26:Fraction(5573,10000),27:Fraction(909,1000),28:Fraction(513,1000),29:Fraction(2143,2500),30:Fraction(7521,10000),31:Fraction(4999,5000),
}
P19_MU={
1:Fraction(4149,10000),3:Fraction(0),5:Fraction(16599,5000),7:Fraction(1,2500),9:Fraction(4481,1000),
11:Fraction(3,10000),13:Fraction(5),15:Fraction(647,10000),17:Fraction(5),19:Fraction(19,10000),
21:Fraction(5),23:Fraction(329,5000),25:Fraction(5),27:Fraction(457,2500),29:Fraction(0),31:Fraction(5),
}
P19_EXPECTED=(
Fraction(332935515406714654293261,716769366014702000000000),
Fraction(772647693,4754750000),
Fraction(59981359082643,2018539960937500),
Fraction(1098589626561579134109123,39422315130808610000000000),
Fraction(1,91),Fraction(-236,19019),Fraction(-23641,2377375),
)

M16_MARGIN={
(7,11,13,23):Fraction(2134682349002381,29351626992187500),
(7,11,13,29):Fraction(1238712960918459209,4246331503476562500),
(7,11,13,31):Fraction(1675429219652823839,4852228983164062500),
(7,11,13,37):Fraction(464467129271395583,987468630585937500),
(7,11,17,19):Fraction(63976862971583,200798554687500),
}
M16_COMPLETION={
(7,11,13,23):Fraction(-34633,2877875),(7,11,13,29):Fraction(-7303,518375),
(7,11,13,31):Fraction(-5147,352625),(7,11,13,37):Fraction(-14621,925925),
(7,11,17,19):Fraction(-46369,3108875),
}

A34=Fraction(5498761,5630625); B34=Fraction(1377221,2413125)
A43=Fraction(9995309,10135125); B43=Fraction(163387,289575)
TH34=Fraction(9640547,395592); TH43=Fraction(5718545,139816)
R34_29=Fraction(44366614,44533125); R43_41=Fraction(138508738,138513375)


def xpa(p:int,a:int)->Fraction:
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))


def direct_bound(primes:tuple[int,...],exps:tuple[int,...])->Fraction:
    xs=tuple(xpa(p,a) for p,a in zip(primes,exps))
    return elementary_symmetric(xs,1)-elementary_symmetric(xs,3)-elementary_symmetric(xs,4)+2*elementary_symmetric(xs,5)+9*elementary_symmetric(xs,6)


def baseline(coords:tuple[Fraction,...])->dict[int,Fraction]:
    out={}
    for mask in range(1,32):
        z=Fraction(1)
        for i,x in enumerate(coords):
            if mask&(1<<i): z*=x
        out[mask]=z
    return out


def assignment_scan()->dict:
    ass=tuple(sorted(set(permutations(PROFILE))))
    vals={a:direct_bound(MIN_PRIMES,a) for a in ass}
    exc=tuple(a for a in ass if vals[a]>=1)
    assert exc==EXCEPTIONAL
    rest={a:v for a,v in vals.items() if a not in exc}
    amax=max(rest,key=rest.get); vmax=rest[amax]
    assert amax==NONEXCEPTIONAL_MAX_ASSIGNMENT and vmax==NONEXCEPTIONAL_MAX_R<1
    return {"count":len(ass),"exceptions":exc,"nonexceptional_max":vmax}


@lru_cache(maxsize=None)
def affine34(P:int)->dict:
    if P not in AFFINE34_EXPECTED: raise ValueError("P must be 17,19,23")
    b=baseline((Fraction(156,625),Fraction(1,7),Fraction(1,11),Fraction(1,13),Fraction(1,P)))
    best=None; cmin=None
    for bits in range(1<<15):
        q0={m:b[m]*(4 if bits&(1<<i) else 1) for i,m in enumerate(NON5)}
        rho=coordinate_rhos(q0,J_MASK)
        cmin=min(rho.values()) if cmin is None else min(cmin,min(rho.values()))
        v=rho[J_MASK]+sum(AFFINE34[m]*q0[m] for m in NON5)
        for T in JSUBS:
            m=1|T; c=AFFINE34[m]-rho[J_MASK^T]
            v+=c*b[m]*(4 if c<0 else 1)
        best=v if best is None or v<best else best
    lb=sum(AFFINE34[s]*b[s] for s in range(1,32)); margin=14*best-27*lb
    assert (best,lb,margin,cmin)==AFFINE34_EXPECTED[P] and margin>0 and cmin>0
    return {"P":P,"C":best,"lambda_b":lb,"margin":margin,"clique_min":cmin}


def _diag(simple:tuple[int,int,int,int],L:dict[int,Fraction],MU:dict[int,Fraction])->tuple:
    b=baseline((Fraction(31,125),)+tuple(Fraction(1,p) for p in simple))
    best=proper=full=comp=None; alpha=5*b[1]-1
    for bits in range(1<<15):
        q0={m:b[m]*(5 if bits&(1<<i) else 1) for i,m in enumerate(NON5)}
        rho=coordinate_rhos(q0,J_MASK)
        for C,v in rho.items():
            if C==J_MASK: full=v if full is None or v<full else full
            else: proper=v if proper is None or v<proper else proper
        u=-alpha*rho[J_MASK]-sum(b[1|T]*rho[J_MASK^T] for T in JSUBS if T)
        comp=u if comp is None or u>comp else comp
        v=rho[J_MASK]+sum(L[m]*q0[m] for m in NON5)
        for T in JSUBS:
            m=1|T; c=L[m]-rho[J_MASK^T]; mu=MU.get(m,Fraction(0)); lo=b[m]; hi=5*b[m]
            if mu: q=min(max(-c/(2*mu),lo),hi)
            else: q=hi if c<0 else lo
            v+=c*q+mu*q*q
        best=v if best is None or v<best else best
    lb=sum(L[s]*b[s] for s in range(1,32)); mb=sum(MU.get(s,Fraction(0))*b[s]*b[s] for s in FIVE)
    margin=41*best-81*lb-197*mb
    assert proper>0 and comp<0 and margin>0
    return best,lb,mb,margin,proper,full,comp


@lru_cache(maxsize=None)
def p19_diagonal()->dict:
    got=_diag((7,11,13,19),P19_LAMBDA,P19_MU)
    assert got==P19_EXPECTED
    return {"C":got[0],"margin":got[3],"proper_non5_min":got[4],"completion_max":got[6]}


@lru_cache(maxsize=None)
def m16_generalized(simple:tuple[int,int,int,int])->dict:
    if simple not in M16_MARGIN: raise ValueError("unsupported exact base")
    got=_diag(simple,M16_LAMBDA,{1:M16_MU})
    assert got[3]==M16_MARGIN[simple] and got[6]==M16_COMPLETION[simple]
    return {"simple":simple,"margin":got[3],"completion_max":got[6]}


def direct34(P:int)->Fraction: return A34+B34/P

def direct43(P:int)->Fraction: return A43+B43/P


def m24_audit()->dict:
    scan=assignment_scan()
    assert universal_monotonicity_gap()==Fraction(719,1440)>0

    # Swapped placement 3^3*5^4: three small affine cases, direct tail at 29,
    # and the two minimal monotone off-family/off-base anchors.
    assert TH34==B34/(1-A34) and 24<TH34<29 and direct34(29)==R34_29<1
    for P in (17,19,23): assert affine34(P)["margin"]>0
    assert direct_bound((3,5,7,11,17,19),SWAPPED_34)==Fraction(417922976,419698125)<1
    assert direct_bound((3,7,11,13,17,19),SWAPPED_34)==Fraction(139011214,157594437)<1

    # Hard placement 3^4*5^3.  Direct monotonicity leaves only seven simple
    # prime tuples.  Five are killed by the M16 quadratic certificate, P=19
    # by the new all-diagonal certificate, and P=17 remains.
    assert TH43==B43/(1-A43) and 40<TH43<41 and direct43(41)==R43_41<1
    assert direct_bound((3,5,11,13,17,19),CANONICAL_43)==Fraction(1511818,1574625)<1
    assert direct_bound((3,5,7,13,17,19),CANONICAL_43)==Fraction(59303774,59520825)<1
    assert direct_bound((3,5,7,11,17,23),CANONICAL_43)==Fraction(101590976,101611125)<1
    for s in M16_MARGIN: assert m16_generalized(s)["margin"]>0
    assert p19_diagonal()["margin"]>0

    return {**scan,
        "profile":PROFILE,
        "remaining_seed":REMAINING_N,
        "remaining_prime_tuple":MIN_PRIMES,
        "remaining_exponents":CANONICAL_43,
        "all_other_profile_members_excluded":True,
        "profile_fully_excluded":False,
    }


__all__=["CANONICAL_43","EXCEPTIONAL","PROFILE","REMAINING_N","SWAPPED_34",
"affine34","assignment_scan","direct34","direct43","direct_bound","m16_generalized","m24_audit","p19_diagonal"]
