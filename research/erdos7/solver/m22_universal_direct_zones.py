"""M22: universal McNew-Setty direct-bound zones for six odd primes."""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations

MINIMAL_ODD_PRIMES=(3,5,7,11,13,17)
UNIVERSAL_E23_CAP=Fraction(721,1440)
UNIVERSAL_DERIVATIVE_GAP=Fraction(719,1440)
ALL_EXPONENTS_TWO_R=Fraction(21635289362,21718371675)
ALL_EXPONENTS_TWO_GAP=Fraction(83082313,21718371675)
ONE_REPEATED_LIMITS=(
    Fraction(90,91),
    Fraction(409,462),
    Fraction(10492,12155),
    Fraction(98786,116025),
    Fraction(953,1122),
    Fraction(9253,10920),
)
LATE_HEAVY_WORST_R=Fraction(1593178541,1595635470)
LATE_HEAVY_GAP=Fraction(2456929,1595635470)


def elementary_symmetric(xs:tuple[Fraction,...], degree:int)->Fraction:
    total=Fraction(0)
    for subset in combinations(xs,degree):
        term=Fraction(1)
        for x in subset: term*=x
        total+=term
    return total


def direct_bound_x(xs:tuple[Fraction,...])->Fraction:
    if len(xs)!=6: raise ValueError("need six coordinates")
    return (
        elementary_symmetric(xs,1)
        - elementary_symmetric(xs,3)
        - elementary_symmetric(xs,4)
        + 2*elementary_symmetric(xs,5)
        + 9*elementary_symmetric(xs,6)
    )


def prime_power_x(p:int,a:int)->Fraction:
    if p<=1 or a<1: raise ValueError("p>1 and a>=1 required")
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))


def infinite_power_cap(p:int)->Fraction:
    if p<=2: raise ValueError("odd prime expected")
    return Fraction(1,p-1)


def universal_monotonicity_gap()->Fraction:
    U=(Fraction(1,2),Fraction(1,4),Fraction(1,6),Fraction(1,10),Fraction(1,12))
    cap=elementary_symmetric(U,2)+elementary_symmetric(U,3)
    assert cap==UNIVERSAL_E23_CAP
    gap=1-cap
    assert gap==UNIVERSAL_DERIVATIVE_GAP and gap>0
    return gap


def all_exponents_at_most_two_audit()->dict:
    xs=tuple(prime_power_x(p,2) for p in MINIMAL_ODD_PRIMES)
    anchor=direct_bound_x(xs)
    assert anchor==ALL_EXPONENTS_TWO_R<1
    assert 1-anchor==ALL_EXPONENTS_TWO_GAP
    return {
        "anchor_primes":MINIMAL_ODD_PRIMES,
        "anchor_exponents":(2,2,2,2,2,2),
        "anchor_R":anchor,
        "gap":1-anchor,
        "all_six_prime_exponents_le_2_noncovering":True,
    }


def one_repeated_prime_audit()->dict:
    values=[]
    for i,p in enumerate(MINIMAL_ODD_PRIMES):
        xs=[Fraction(1,q) for q in MINIMAL_ODD_PRIMES]
        xs[i]=infinite_power_cap(p)
        values.append(direct_bound_x(tuple(xs)))
    assert tuple(values)==ONE_REPEATED_LIMITS
    worst=max(values)
    assert worst==Fraction(90,91)<1
    return {
        "position_limits":tuple(values),
        "worst_limit":worst,
        "worst_gap":1-worst,
        "arbitrary_single_repeated_exponent_noncovering":True,
    }


def late_heavy_rank_audit()->dict:
    values={}
    for i in range(2,6):
        xs=[prime_power_x(p,2) for p in MINIMAL_ODD_PRIMES]
        xs[i]=infinite_power_cap(MINIMAL_ODD_PRIMES[i])
        values[i+1]=direct_bound_x(tuple(xs))
    worst_rank=max(values,key=values.get)
    worst=values[worst_rank]
    assert worst_rank==3
    assert worst==LATE_HEAVY_WORST_R<1
    assert 1-worst==LATE_HEAVY_GAP
    return {
        "rank_limits":values,
        "worst_rank":worst_rank,
        "worst_R":worst,
        "gap":1-worst,
        "arbitrary_exponent_on_rank_ge_3_with_others_le_2_noncovering":True,
    }


def m22_audit()->dict:
    gap=universal_monotonicity_gap()
    all2=all_exponents_at_most_two_audit()
    one=one_repeated_prime_audit()
    late=late_heavy_rank_audit()
    return {
        "universal_derivative_gap":gap,
        "all2":all2,
        "one_repeated":one,
        "late_heavy":late,
        "all_claims_exact":True,
    }


__all__=[
    "ALL_EXPONENTS_TWO_GAP","ALL_EXPONENTS_TWO_R",
    "LATE_HEAVY_GAP","LATE_HEAVY_WORST_R","MINIMAL_ODD_PRIMES",
    "ONE_REPEATED_LIMITS","UNIVERSAL_DERIVATIVE_GAP","UNIVERSAL_E23_CAP",
    "all_exponents_at_most_two_audit","direct_bound_x","elementary_symmetric",
    "infinite_power_cap","late_heavy_rank_audit","m22_audit",
    "one_repeated_prime_audit","prime_power_x","universal_monotonicity_gap",
]
