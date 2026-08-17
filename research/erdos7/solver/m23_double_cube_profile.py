"""M23: exact exclusion of the six-prime exponent profile (3,3,1,1,1,1)."""
from __future__ import annotations

from fractions import Fraction
from itertools import permutations

from m14_clique_shearer import J_MASK, coordinate_rhos
from m17_infinite_family import elementary_symmetric, is_prime
from m22_universal_direct_zones import universal_monotonicity_gap

MINIMAL_ODD_PRIMES=(3,5,7,11,13,17)
EXPONENT_PROFILE=(3,3,1,1,1,1)
SMALL_P=(17,19,23)

LAMBDA={
    1:Fraction(543,1000),2:Fraction(3641,10000),3:Fraction(3869,5000),
    4:Fraction(687,2500),5:Fraction(361,500),6:Fraction(3087,5000),
    7:Fraction(8643,10000),8:Fraction(2439,10000),9:Fraction(3541,5000),
    10:Fraction(1509,2500),11:Fraction(8503,10000),12:Fraction(4449,10000),
    13:Fraction(7983,10000),14:Fraction(1733,2500),15:Fraction(2353,2500),
    16:Fraction(131,625),17:Fraction(1027,2000),18:Fraction(4333,10000),
    19:Fraction(4161,5000),20:Fraction(493,1250),21:Fraction(3901,5000),
    22:Fraction(6751,10000),23:Fraction(9231,10000),24:Fraction(3553,10000),
    25:Fraction(3831,5000),26:Fraction(6611,10000),27:Fraction(9091,10000),
    28:Fraction(6091,10000),29:Fraction(8571,10000),30:Fraction(94,125),
    31:Fraction(1),
}

EXPECTED={
    17:{
        "C":Fraction(14220686241,21271250000),
        "lambda_b":Fraction(432013607,1251250000),
        "margin":Fraction(795361761,21271250000),
    },
    19:{
        "C":Fraction(790944733,1188687500),
        "lambda_b":Fraction(232200229,679250000),
        "margin":Fraction(58151681,679250000),
    },
    23:{
        "C":Fraction(1188435483,1798671875),
        "lambda_b":Fraction(9692561407,28778750000),
        "margin":Fraction(410035473,2616250000),
    },
}

DIRECT_A=Fraction(3294908,3378375)
DIRECT_B=Fraction(1933172,3378375)
DIRECT_THRESHOLD=Fraction(1933172,83467)
DIRECT_R29=Fraction(32495168,32657625)
NONCANONICAL_MAX_R=Fraction(37123796,37522485)
NONCANONICAL_MAX_ASSIGNMENT=(3,1,3,1,1,1)
CANONICAL_MINIMAL_R=Fraction(378736,375375)
OFFBASE_REPEATED_PRIMES_R=Fraction(377169536,427756329)
OFF_FAMILY_SIMPLE_R=Fraction(3091888,3108875)


def prime_power_x(p:int,a:int)->Fraction:
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))


def direct_bound(primes:tuple[int,...],exponents:tuple[int,...])->Fraction:
    xs=tuple(prime_power_x(p,a) for p,a in zip(primes,exponents))
    return (
        elementary_symmetric(xs,1)-elementary_symmetric(xs,3)
        -elementary_symmetric(xs,4)+2*elementary_symmetric(xs,5)
        +9*elementary_symmetric(xs,6)
    )


def baseline(mask:int,last_prime:int)->Fraction:
    base=(Fraction(31,125),Fraction(1,7),Fraction(1,11),Fraction(1,13),Fraction(1,last_prime))
    out=Fraction(1)
    for i,x in enumerate(base):
        if mask&(1<<i): out*=x
    return out


def affine_certificate(last_prime:int)->dict:
    if last_prime not in SMALL_P: raise ValueError("certified small primes are 17,19,23")
    non5=[m for m in range(1,32) if not (m&1)]
    best=None
    non5_clique_min=None
    for bits in range(1<<len(non5)):
        q0={
            mask:baseline(mask,last_prime)*(4 if bits&(1<<idx) else 1)
            for idx,mask in enumerate(non5)
        }
        rho=coordinate_rhos(q0,J_MASK)
        local_min=min(rho.values())
        if non5_clique_min is None or local_min<non5_clique_min:
            non5_clique_min=local_min

        value=rho[J_MASK]+sum(LAMBDA[m]*q0[m] for m in non5)
        for T in range(32):
            if T&~J_MASK: continue
            mask=1|T
            coeff=LAMBDA[mask]-rho[J_MASK^T]
            q5=baseline(mask,last_prime)*(4 if coeff<0 else 1)
            value+=coeff*q5
        if best is None or value<best: best=value

    assert best is not None and non5_clique_min is not None
    lambda_b=sum(LAMBDA[S]*baseline(S,last_prime) for S in range(1,32))
    margin=14*best-27*lambda_b
    exp=EXPECTED[last_prime]
    assert best==exp["C"]
    assert lambda_b==exp["lambda_b"]
    assert margin==exp["margin"]>0
    assert non5_clique_min>0
    return {
        "last_prime":last_prime,"C":best,"lambda_b":lambda_b,
        "margin":margin,"non5_clique_min":non5_clique_min,
        "noncovering_certified":True,
    }


def direct_family_bound(P:int)->Fraction:
    if P<=0: raise ValueError("P positive")
    return DIRECT_A+DIRECT_B/P


def assignment_scan()->dict:
    assignments=tuple(sorted(set(permutations(EXPONENT_PROFILE))))
    assert len(assignments)==15
    values={a:direct_bound(MINIMAL_ODD_PRIMES,a) for a in assignments}
    assert values[EXPONENT_PROFILE]==CANONICAL_MINIMAL_R>1
    noncanon={a:v for a,v in values.items() if a!=EXPONENT_PROFILE}
    amax=max(noncanon,key=noncanon.get)
    vmax=noncanon[amax]
    assert amax==NONCANONICAL_MAX_ASSIGNMENT
    assert vmax==NONCANONICAL_MAX_R<1
    return {
        "assignment_count":15,"canonical_R":CANONICAL_MINIMAL_R,
        "noncanonical_max_assignment":amax,"noncanonical_max_R":vmax,
        "all_noncanonical_directly_excluded":True,
    }


def _ordered(primes:tuple[int,...],exponents:tuple[int,...])->tuple[tuple[int,...],tuple[int,...]]:
    if len(primes)!=6 or len(exponents)!=6: raise ValueError("need six coordinates")
    if len(set(primes))!=6 or not all(is_prime(p) and p%2 for p in primes): raise ValueError("six distinct odd primes required")
    if tuple(sorted(exponents,reverse=True))!=EXPONENT_PROFILE: raise ValueError("wrong exponent profile")
    pairs=sorted(zip(primes,exponents))
    return tuple(p for p,_ in pairs),tuple(a for _,a in pairs)


def proof_branch(primes:tuple[int,...],exponents:tuple[int,...])->str:
    primes,exponents=_ordered(primes,exponents)
    assert universal_monotonicity_gap()>0
    if exponents!=EXPONENT_PROFILE:
        base=direct_bound(MINIMAL_ODD_PRIMES,exponents)
        assert base<=NONCANONICAL_MAX_R<1
        assert direct_bound(primes,exponents)<=base
        return "McNew-Setty-noncanonical-placement"

    if primes[:2]!=(3,5):
        anchor=(3,7,11,13,17,19)
        assert all(p>=q for p,q in zip(primes,anchor))
        assert direct_bound(anchor,EXPONENT_PROFILE)==OFFBASE_REPEATED_PRIMES_R<1
        assert direct_bound(primes,exponents)<=OFFBASE_REPEATED_PRIMES_R
        return "McNew-Setty-canonical-offbase"

    simples=primes[2:]
    if simples[:3]==(7,11,13):
        P=simples[3]
        if P in SMALL_P:
            assert affine_certificate(P)["noncovering_certified"] is True
            return "M23-affine"
        assert P>=29
        assert direct_family_bound(P)<=DIRECT_R29<1
        return "McNew-Setty-P-tail"

    anchor=(3,5,7,11,17,19)
    assert all(p>=q for p,q in zip(primes,anchor))
    assert direct_bound(anchor,EXPONENT_PROFILE)==OFF_FAMILY_SIMPLE_R<1
    assert direct_bound(primes,exponents)<=OFF_FAMILY_SIMPLE_R
    return "McNew-Setty-simple-offfamily"


def m23_audit()->dict:
    scan=assignment_scan()
    certs={P:affine_certificate(P) for P in SMALL_P}
    assert DIRECT_B>0
    assert DIRECT_THRESHOLD==DIRECT_B/(1-DIRECT_A)
    assert 23<DIRECT_THRESHOLD<29
    assert direct_family_bound(29)==DIRECT_R29<1
    assert 1-DIRECT_R29==Fraction(162457,32657625)
    assert proof_branch((3,5,7,11,13,17),EXPONENT_PROFILE)=="M23-affine"
    assert proof_branch((3,5,7,11,13,29),EXPONENT_PROFILE)=="McNew-Setty-P-tail"
    assert proof_branch((3,5,7,11,17,19),EXPONENT_PROFILE)=="McNew-Setty-simple-offfamily"
    assert proof_branch((3,7,11,13,17,19),EXPONENT_PROFILE)=="McNew-Setty-canonical-offbase"
    assert proof_branch((3,5,7,11,13,17),(3,1,3,1,1,1))=="McNew-Setty-noncanonical-placement"
    return {**scan,"small_certificates":certs,"direct_threshold":DIRECT_THRESHOLD,
            "all_odd_six_prime_numbers_with_profile_noncovering":True}


__all__=[
    "DIRECT_A","DIRECT_B","DIRECT_R29","DIRECT_THRESHOLD","EXPONENT_PROFILE",
    "LAMBDA","SMALL_P","affine_certificate","assignment_scan","baseline",
    "direct_bound","direct_family_bound","m23_audit","proof_branch",
]
