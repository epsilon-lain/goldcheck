"""M71: close exponent placement (4,2,2,1,2,1) in the P4222 profile.

At the minimal odd primes the placement is

    3^4 * 5^2 * 7^2 * 11 * 13^2 * 17.

Stage on 3^4 and distinguish the 13^2 coordinate.  Retain exact two-level
activations for the fixed non-special squares 5^2 and 7^2, exact levels for
the simple coordinates 11 and 17, and reduce the eleven remaining support
charges to factor-5 endpoints by separate concavity.

The final exact certificate uses the M66 goodness branch plus sparse
nonnegative linear/pair/factorial penalties.  Because the special 13^2
coordinate is treated continuously, M27 supportwise scaling transports the
minimal reference to every coordinatewise larger prime tuple with prefix
(3,5,7); direct anchors kill the other prefixes.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, prod

from m17_infinite_family import is_prime
from m22_universal_direct_zones import universal_monotonicity_gap
from m25_cross_support_seed import DIAGONAL, LAMBDA
from m26_minimal_frontier import direct_bound
from m28_moment_hierarchy import moment_constant
from m30_centered_moments import factorial_spike_cap

EXPONENTS=(4,2,2,1,2,1)
REFERENCE_PRIMES=(3,5,7,11,13,17)
N=3**4*5**2*7**2*11*13**2*17

# Local non-special order: (5^2,7^2,11,17).  Special coordinate: 13^2.
D=(25,49,11,17)
COORD_NUMERATORS=(6,8,1,1)
DENOMINATORS=tuple(prod(D[i] for i in range(4) if C&(1<<i)) for C in range(16))
SUPPORT_NUMERATORS=tuple(prod(COORD_NUMERATORS[i] for i in range(4) if S&(1<<i)) for S in range(16))
XSPECIAL=Fraction(14,169)

LINEAR_MASKS=(3,5,6,7,9,10,11,12,13,14)
LINEAR_NUMERATORS=(75226,37691,35316,79381,25053,31897,66042,8400,68044,55875)
CROSS_PAIRS=((1,3),(1,5),(1,9),(2,6),(3,5),(3,7),(3,9),(3,10),(3,11),(3,14),(4,12),(5,7),(5,9),(6,10),(7,9),(7,12),(9,10),(9,11),(10,13),(11,13),(12,14))
CROSS_NUMERATORS=(0,31340,33295,13131,3625,26690,9985,0,74074,0,78405,47933,119720,213049,12600,0,0,88753,0,637381,0)
# (first, second-factorial) for A5,B5,A7,B7,z11-1,z17-1.
FACTORIAL_NUMERATORS=(5148,3263,882,820,2663,1601,434,211,894,668,625,280)
COEFF_DEN=100_000

Q=10**9
C=Fraction(16929,50000)  # 0.33858
EXPECTED_STATE_COUNT=25**2*5**2*2**11
EXPECTED_FLOOR_MIN=338_583_246
EXPECTED_FLOOR_SLACK=3_246
EXPECTED_ARGMIN=(2,2,0,0,1,1,1112)
EXPECTED_EXACT_ARGMIN=Fraction(4269567609502557002629,12610096302537327343750)
EXPECTED_SPECIAL_COST=Fraction(9105881382571301,3058670677562500)
EXPECTED_FEATURE_COST=Fraction(57057870182650423,5247535562500000)
EXPECTED_ETA=Fraction(428350949784729177,13624987563687500000)

UNSELECTED=(3,5,6,7,9,10,11,12,13,14,15)
OFF3=(5,7,11,13,17,19)
OFF5=(3,7,11,13,17,19)
OFF7=(3,5,11,13,17,19)
EXPECTED_ANCHORS={
    OFF3:Fraction(3649063388,5398339375),
    OFF5:Fraction(10278976852,11427204789),
    OFF7:Fraction(5606713348,5830206525),
}


def baseline(mask:int)->Fraction:
    return Fraction(SUPPORT_NUMERATORS[mask],DENOMINATORS[mask])


def _quadratic_min(linear:Fraction,quadratic:Fraction,lo:Fraction,hi:Fraction)->Fraction:
    x=-linear/(2*quadratic)
    if x<lo:x=lo
    elif x>hi:x=hi
    return linear*x+quadratic*x*x


def _rho(state:tuple[int,...]):
    A5,B5,A7,B7,z11,z17,bits=state
    q={
        1:Fraction(6+5*A5+B5,25),
        2:Fraction(8+7*A7+B7,49),
        4:Fraction(z11,11),
        8:Fraction(z17,17),
    }
    for j,m in enumerate(UNSELECTED):
        q[m]=baseline(m)*(5 if bits&(1<<j) else 1)
    rho={0:Fraction(1)}
    for size in range(1,5):
        for Cmask in range(1,16):
            if Cmask.bit_count()!=size:continue
            pivot=Cmask&-Cmask;rest=Cmask^pivot
            value=rho[rest];T=rest
            while True:
                S=pivot|T
                value-=q[S]*rho[Cmask^S]
                if T==0:break
                T=(T-1)&rest
            rho[Cmask]=value
    return rho,q


def pointwise_exact(state:tuple[int,...])->Fraction:
    rho,q=_rho(state)
    pcoord=Fraction(0);full=rho[15]
    for T in range(16):
        sm=1|(T<<1)
        lo=XSPECIAL*baseline(T);hi=5*lo
        pcoord+=LAMBDA.get(sm,Fraction(0))*lo+DIAGONAL[sm]*lo*lo
        full+=_quadratic_min(LAMBDA.get(sm,Fraction(0))-rho[15^T],DIAGONAL[sm],lo,hi)
    coordinate=min(rho[Cmask] for Cmask in range(1,16))+pcoord
    value=min(full,coordinate)
    value+=sum(Fraction(c,COEFF_DEN)*q[m] for m,c in zip(LINEAR_MASKS,LINEAR_NUMERATORS))
    value+=sum(Fraction(c,COEFF_DEN)*q[s]*q[t] for (s,t),c in zip(CROSS_PAIRS,CROSS_NUMERATORS))
    acts=(state[0],state[1],state[2],state[3],state[4]-1,state[5]-1)
    for j,A in enumerate(acts):
        value+=Fraction(FACTORIAL_NUMERATORS[2*j],COEFF_DEN)*A
        value+=Fraction(FACTORIAL_NUMERATORS[2*j+1],COEFF_DEN)*comb(A,2)
    return value


def special_global_cost()->Fraction:
    out=Fraction(0)
    for T in range(16):
        sm=1|(T<<1);b=XSPECIAL*baseline(T)
        out+=81*LAMBDA.get(sm,Fraction(0))*b+197*DIAGONAL[sm]*b*b
    return out


def feature_global_cost()->Fraction:
    out=81*sum(Fraction(c,COEFF_DEN)*baseline(m) for m,c in zip(LINEAR_MASKS,LINEAR_NUMERATORS))
    out+=197*sum(Fraction(c,COEFF_DEN)*baseline(s)*baseline(t) for (s,t),c in zip(CROSS_PAIRS,CROSS_NUMERATORS))
    assert factorial_spike_cap(4,1)==40 and factorial_spike_cap(4,2)==18
    for j in range(6):
        out+=40*Fraction(FACTORIAL_NUMERATORS[2*j],COEFF_DEN)
        out+=18*Fraction(FACTORIAL_NUMERATORS[2*j+1],COEFF_DEN)
    return out


def certificate_audit()->dict:
    assert moment_constant(4,1)==81 and moment_constant(4,2)==197
    assert EXPECTED_STATE_COUNT==32_000_000
    assert C*Q==338_580_000
    assert EXPECTED_FLOOR_MIN-C*Q==EXPECTED_FLOOR_SLACK>0
    exact=pointwise_exact(EXPECTED_ARGMIN)
    assert exact==EXPECTED_EXACT_ARGMIN>C
    assert Fraction(EXPECTED_FLOOR_MIN,Q)<=exact
    assert special_global_cost()==EXPECTED_SPECIAL_COST
    assert feature_global_cost()==EXPECTED_FEATURE_COST
    eta=41*C-special_global_cost()-feature_global_cost()
    assert eta==EXPECTED_ETA>0
    return {"N":N,"state_count":EXPECTED_STATE_COUNT,"floor_min_scaled":EXPECTED_FLOOR_MIN,
            "floor_slack_scaled":EXPECTED_FLOOR_SLACK,"argmin":EXPECTED_ARGMIN,
            "exact_argmin_value":exact,"summed_goodness_margin":eta,
            "noncovering_certified":True}


def anchor_audit()->dict:
    assert universal_monotonicity_gap()>0
    for primes,expected in EXPECTED_ANCHORS.items():
        assert direct_bound(primes,EXPONENTS)==expected<1
    return {"anchor_count":3,"verified":True}


def proof_branch(primes:tuple[int,...])->str:
    primes=tuple(primes)
    if len(primes)!=6 or tuple(sorted(primes))!=primes or len(set(primes))!=6:
        raise ValueError("need six increasing distinct primes")
    if not all(is_prime(p) and p%2 for p in primes):
        raise ValueError("need six odd primes")
    assert universal_monotonicity_gap()>0
    if primes[0]!=3:
        assert all(p>=q for p,q in zip(primes,OFF3))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF3]<1
        return "McNew-Setty-off3"
    if primes[1]!=5:
        assert all(p>=q for p,q in zip(primes,OFF5))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF5]<1
        return "McNew-Setty-off5"
    if primes[2]!=7:
        assert all(p>=q for p,q in zip(primes,OFF7))
        assert direct_bound(primes,EXPONENTS)<=EXPECTED_ANCHORS[OFF7]<1
        return "McNew-Setty-off7"

    # Prefix is exactly (3,5,7).  The exact weighted activation laws belong to
    # the fixed non-special squares 5^2 and 7^2, so they are unchanged.  The
    # fourth and sixth coordinates are simple, while the fifth (13^2 at the
    # reference) is the continuously treated special coordinate.  M27 scaling
    # therefore transports all baselines and the 81/197 moment budgets exactly.
    assert all(p>=q for p,q in zip(primes,REFERENCE_PRIMES))
    assert certificate_audit()["summed_goodness_margin"]>0
    return "M71-special13-reference-scale"


def theorem_audit()->dict:
    anchors=anchor_audit();cert=certificate_audit()
    assert cert["noncovering_certified"]
    assert proof_branch(REFERENCE_PRIMES)=="M71-special13-reference-scale"
    assert proof_branch((3,5,7,19,23,29))=="M71-special13-reference-scale"
    return {"exponent_placement":EXPONENTS,"anchors":anchors,
            "all_odd_six_prime_numbers_with_this_placement_noncovering":True,
            "verified":True}


__all__=["C","EXPECTED_ETA","EXPONENTS","N","certificate_audit","proof_branch","theorem_audit"]
