"""M26: exact minimal exponent-frontier census after M25.

M22 and M25 leave a profile-level closed region for sorted six-prime exponent
profiles.  The componentwise-minimal profiles outside that region are exactly

    (5,2,1,1,1,1), (4,4,1,1,1,1), (3,2,2,1,1,1).

This module verifies that structural antichain and then applies the universal
McNew--Setty coordinate monotonicity from M22 to reduce those three profiles to
30 explicit prime/exponent seeds in total: 7, 11, and 12 respectively.

This is a frontier reduction only; none of the 30 seeds is asserted to cover.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import permutations
from m17_infinite_family import elementary_symmetric, is_prime
from m22_universal_direct_zones import universal_monotonicity_gap

MINIMAL_ODD_PRIMES=(3,5,7,11,13,17)
M25_PROFILE_MAJORANT=(4,3,1,1,1,1)
P52=(5,2,1,1,1,1); P514=(5,1,2,1,1,1)
P44=(4,4,1,1,1,1); P414=(4,1,4,1,1,1)
P322=(3,2,2,1,1,1); P3212=(3,2,1,2,1,1)
P32112=(3,2,1,1,2,1); P321112=(3,2,1,1,1,2)
MINIMAL_FRONTIER=(P52,P44,P322)
EXCEPTIONAL_PLACEMENTS={P52:(P52,P514),P44:(P44,P414),P322:(P322,P3212,P32112,P321112)}
EXPECTED_MINIMAL_VALUES={
 P52:{P52:Fraction(6184054,6081075),P514:Fraction(9662260,9648639)},
 P44:{P44:Fraction(51718819,50675625),P414:Fraction(788139353,787972185)},
 P322:{P322:Fraction(1602803,1576575),P3212:Fraction(42456287,42117075),P32112:Fraction(5566549,5530525),P321112:Fraction(38867,38675)},
}
EXPECTED_MAX_DIRECTLY_KILLED={
 P52:((5,1,1,2,1,1),Fraction(2655728,2675673)),
 P44:((4,1,1,4,1,1),Fraction(1815414127,1834619787)),
 P322:((3,1,2,2,1,1),Fraction(1300549,1310309)),
}
SEEDS={
 P52:tuple([((3,5,7,11,13,p),P52) for p in (17,19,23,29,31)]+[((3,5,7,11,17,19),P52),((3,5,7,11,13,17),P514)]),
 P44:tuple([((3,5,7,11,13,p),P44) for p in (17,19,23,29,31,37,41,43)]+[((3,5,7,11,17,p),P44) for p in (19,23)]+[((3,5,7,11,13,17),P414)]),
 P322:tuple([((3,5,7,11,13,p),P322) for p in (17,19,23,29,31)]+[((3,5,7,11,17,19),P322)]+[((3,5,7,11,13,p),e) for e in (P3212,P32112,P321112) for p in (17,19)]),
}
KILL_ANCHORS={
 P52:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,13,37),(3,5,7,11,17,23),(3,5,7,11,19,23)),
 P514:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,17,19),(3,5,7,11,13,19)),
 P44:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,13,47),(3,5,7,11,17,29),(3,5,7,11,19,23)),
 P414:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,17,19),(3,5,7,11,13,19)),
 P322:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,13,37),(3,5,7,11,17,23),(3,5,7,11,19,23)),
 P3212:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,17,19),(3,5,7,11,13,23)),
 P32112:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,17,19),(3,5,7,11,13,23)),
 P321112:((5,7,11,13,17,19),(3,7,11,13,17,19),(3,5,11,13,17,19),(3,5,7,13,17,19),(3,5,7,11,17,19),(3,5,7,11,13,23)),
}

def prime_power_x(p,a):
    return sum((Fraction(1,p**j) for j in range(1,a+1)),Fraction(0))

def direct_bound(primes,exponents):
    xs=tuple(prime_power_x(p,a) for p,a in zip(primes,exponents))
    return elementary_symmetric(xs,1)-elementary_symmetric(xs,3)-elementary_symmetric(xs,4)+2*elementary_symmetric(xs,5)+9*elementary_symmetric(xs,6)

def sorted_profile(profile):
    if len(profile)!=6 or any(a<1 for a in profile): raise ValueError("need six positive exponents")
    return tuple(sorted(profile,reverse=True))

def profile_closed_before_m26(profile):
    p=sorted_profile(profile)
    if p[0]<=2: return True
    if p[1]==1: return True
    return all(a<=b for a,b in zip(p,M25_PROFILE_MAJORANT))

def minimal_frontier_dominator(profile):
    p=sorted_profile(profile)
    if profile_closed_before_m26(p): return None
    assert p[1]>=2
    if p[0]>=5: out=P52
    elif p[1]>=4: out=P44
    else:
        assert p[0]>=3 and p[2]>=2
        out=P322
    assert all(a<=b for a,b in zip(out,p))
    return out

def placement_scan(profile):
    p=sorted_profile(profile)
    assignments=tuple(sorted(set(permutations(p))))
    values={a:direct_bound(MINIMAL_ODD_PRIMES,a) for a in assignments}
    exceptions=tuple(a for a in assignments if values[a]>=1)
    assert set(exceptions)==set(EXCEPTIONAL_PLACEMENTS[p])
    assert {a:values[a] for a in exceptions}==EXPECTED_MINIMAL_VALUES[p]
    killed={a:v for a,v in values.items() if a not in exceptions}
    amax=max(killed,key=killed.get); vmax=killed[amax]
    ea,ev=EXPECTED_MAX_DIRECTLY_KILLED[p]
    assert amax==ea and vmax==ev<1
    return {"assignment_count":len(assignments),"exceptional_placements":exceptions,"max_directly_killed_assignment":amax,"max_directly_killed_R":vmax}

def family_number(primes,exponents):
    out=1
    for p,a in zip(primes,exponents): out*=p**a
    return out

def direct_reduction_branch(primes,exponents):
    if len(primes)!=6 or tuple(sorted(primes))!=tuple(primes) or len(set(primes))!=6 or not all(is_prime(p) and p%2 for p in primes): raise ValueError("need six increasing distinct odd primes")
    profile=sorted_profile(exponents)
    if profile not in MINIMAL_FRONTIER: raise ValueError("wrong exponent profile")
    assert universal_monotonicity_gap()>0
    if tuple(exponents) not in EXCEPTIONAL_PLACEMENTS[profile]:
        base=direct_bound(MINIMAL_ODD_PRIMES,tuple(exponents)); assert base<1
        assert direct_bound(tuple(primes),tuple(exponents))<=base
        return "McNew-Setty-placement"
    item=(tuple(primes),tuple(exponents))
    if item in SEEDS[profile]:
        assert direct_bound(*item)>=1
        return "seed"
    dominating=[a for a in KILL_ANCHORS[tuple(exponents)] if all(p>=q for p,q in zip(primes,a))]
    assert dominating
    anchor=min(dominating)
    assert direct_bound(anchor,tuple(exponents))<1
    assert direct_bound(tuple(primes),tuple(exponents))<=direct_bound(anchor,tuple(exponents))
    return "McNew-Setty-anchor"

def frontier_census():
    assert universal_monotonicity_gap()>0
    assert all(not profile_closed_before_m26(p) for p in MINIMAL_FRONTIER)
    for p in MINIMAL_FRONTIER:
        for q in MINIMAL_FRONTIER:
            if p!=q: assert not all(a<=b for a,b in zip(p,q))
    scans={p:placement_scan(p) for p in MINIMAL_FRONTIER}
    counts={p:len(SEEDS[p]) for p in MINIMAL_FRONTIER}
    assert counts=={P52:7,P44:11,P322:12} and sum(counts.values())==30
    for p,seeds in SEEDS.items():
        for primes,exp in seeds: assert direct_reduction_branch(primes,exp)=="seed"
    return {"minimal_frontier":MINIMAL_FRONTIER,"placement_scans":scans,"seed_counts":counts,"total_direct_bound_seeds":30,"seed_numbers":{p:tuple(family_number(pr,e) for pr,e in SEEDS[p]) for p in MINIMAL_FRONTIER},"verified":True}

__all__=["MINIMAL_FRONTIER","SEEDS","direct_bound","direct_reduction_branch","frontier_census","minimal_frontier_dominator","placement_scan","profile_closed_before_m26"]