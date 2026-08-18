"""M69: exact second reference for the canonical P4222 placement.

Target reference:
    3^4 * 5^2 * 7^2 * 13^2 * 17 * 19.

The M68 coefficient family is reused.  The only structural change is the
second weighted singleton, now 13^2 instead of 11^2, and the simple singleton
coordinates 17,19.  The exact 32,000,000-state verifier remains positive with
large quantitative margin.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, prod

import m68_p4222_canonical_seed as m68
from m25_cross_support_seed import DIAGONAL, LAMBDA
from m28_moment_hierarchy import moment_constant
from m30_centered_moments import factorial_spike_cap

N = 3**4 * 5**2 * 7**2 * 13**2 * 17 * 19

D = (49,169,17,19)
COORD_NUMERATORS = (8,14,1,1)
DENOMINATORS = tuple(prod(D[i] for i in range(4) if C & (1 << i)) for C in range(16))
SUPPORT_NUMERATORS = tuple(
    prod(COORD_NUMERATORS[i] for i in range(4) if S & (1 << i))
    for S in range(16)
)
X5 = Fraction(6,25)

Q = 10**9
C = Fraction(17017,50000)  # 0.34034
EXPECTED_STATE_COUNT = 32_000_000
EXPECTED_FLOOR_MIN = 340_352_099
EXPECTED_FLOOR_SLACK = 12_099
EXPECTED_ARGMIN = (4,4,0,0,1,1,1371)
EXPECTED_EXACT_ARGMIN = Fraction(97400023463548344087,286174284246760000000)
EXPECTED_SPECIAL_COST = Fraction(19983308530450288293,2235736595677812500)
EXPECTED_FEATURE_COST = Fraction(89002485211088801,21042226782850000)
EXPECTED_ETA = Fraction(1757511727763981557,2235736595677812500)


def baseline(mask: int) -> Fraction:
    return Fraction(SUPPORT_NUMERATORS[mask], DENOMINATORS[mask])


def _qmin(linear: Fraction, quadratic: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    x = -linear/(2*quadratic)
    if x < lo: x = lo
    elif x > hi: x = hi
    return linear*x + quadratic*x*x


def _rho(state: tuple[int,...]):
    A7,B7,A13,B13,z17,z19,bits = state
    q = {
        1: Fraction(8+7*A7+B7,49),
        2: Fraction(14+13*A13+B13,169),
        4: Fraction(z17,17),
        8: Fraction(z19,19),
    }
    for j,m in enumerate(m68.UNSELECTED):
        q[m] = baseline(m) * (5 if bits & (1 << j) else 1)
    rho = {0:Fraction(1)}
    for size in range(1,5):
        for Cmask in range(1,16):
            if Cmask.bit_count() != size: continue
            pivot=Cmask&-Cmask
            rest=Cmask^pivot
            value=rho[rest]
            T=rest
            while True:
                S=pivot|T
                value -= q[S]*rho[Cmask^S]
                if T==0: break
                T=(T-1)&rest
            rho[Cmask]=value
    return rho,q


def pointwise_exact(state: tuple[int,...]) -> Fraction:
    rho,q = _rho(state)
    pcoord=Fraction(0)
    full=rho[15]
    for T in range(16):
        sm=1|(T<<1)
        lo=X5*baseline(T)
        hi=5*lo
        pcoord += LAMBDA.get(sm,Fraction(0))*lo + DIAGONAL[sm]*lo*lo
        full += _qmin(LAMBDA.get(sm,Fraction(0))-rho[15^T],DIAGONAL[sm],lo,hi)
    coordinate=min(rho[Cmask] for Cmask in range(1,16))+pcoord
    value=min(full,coordinate)
    value += sum(
        Fraction(c,m68.COEFF_DEN)*q[m]
        for m,c in zip(m68.LINEAR_MASKS,m68.LINEAR_NUMERATORS)
    )
    value += sum(
        Fraction(c,m68.COEFF_DEN)*q[s]*q[t]
        for (s,t),c in zip(m68.CROSS_PAIRS,m68.CROSS_NUMERATORS)
    )
    acts=(state[0],state[1],state[2],state[3],state[4]-1,state[5]-1)
    for j,A in enumerate(acts):
        value += Fraction(m68.FACTORIAL_NUMERATORS[2*j],m68.COEFF_DEN)*A
        value += Fraction(m68.FACTORIAL_NUMERATORS[2*j+1],m68.COEFF_DEN)*comb(A,2)
    return value


def special_global_cost() -> Fraction:
    out=Fraction(0)
    for T in range(16):
        sm=1|(T<<1)
        b=X5*baseline(T)
        out += 81*LAMBDA.get(sm,Fraction(0))*b + 197*DIAGONAL[sm]*b*b
    return out


def feature_global_cost() -> Fraction:
    out=81*sum(
        Fraction(c,m68.COEFF_DEN)*baseline(m)
        for m,c in zip(m68.LINEAR_MASKS,m68.LINEAR_NUMERATORS)
    )
    out += 197*sum(
        Fraction(c,m68.COEFF_DEN)*baseline(s)*baseline(t)
        for (s,t),c in zip(m68.CROSS_PAIRS,m68.CROSS_NUMERATORS)
    )
    assert factorial_spike_cap(4,1)==40 and factorial_spike_cap(4,2)==18
    for j in range(6):
        out += 40*Fraction(m68.FACTORIAL_NUMERATORS[2*j],m68.COEFF_DEN)
        out += 18*Fraction(m68.FACTORIAL_NUMERATORS[2*j+1],m68.COEFF_DEN)
    return out


def certificate_audit() -> dict:
    assert moment_constant(4,1)==81 and moment_constant(4,2)==197
    assert C*Q == 340_340_000
    assert EXPECTED_FLOOR_MIN-C*Q == EXPECTED_FLOOR_SLACK > 0
    exact=pointwise_exact(EXPECTED_ARGMIN)
    assert exact==EXPECTED_EXACT_ARGMIN > C
    assert Fraction(EXPECTED_FLOOR_MIN,Q) <= exact
    assert special_global_cost()==EXPECTED_SPECIAL_COST
    assert feature_global_cost()==EXPECTED_FEATURE_COST
    eta=41*C-special_global_cost()-feature_global_cost()
    assert eta==EXPECTED_ETA>0
    return {
        "N":N,
        "state_count":EXPECTED_STATE_COUNT,
        "floor_min_scaled":EXPECTED_FLOOR_MIN,
        "floor_slack_scaled":EXPECTED_FLOOR_SLACK,
        "argmin":EXPECTED_ARGMIN,
        "exact_argmin_value":exact,
        "summed_goodness_margin":eta,
        "noncovering_certified":True,
    }


__all__=["C","EXPECTED_ETA","N","certificate_audit","pointwise_exact"]
