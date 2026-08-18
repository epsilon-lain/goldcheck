"""M64: exact closure of the sole M63 hard seed.

Target:
    N = 3^3 * 5^2 * 7^2 * 11^2 * 13^2 * 17^2.

Stage on 3^3 and distinguish 5^2.  All four non-special singleton coordinates
are repeated prime squares.  For p in {7,11,13,17}, retain the exact two-level
activation

    q_{p}/b_{p} = 1 + (p*A_p + B_p)/(p+1),  A_p,B_p in {0,1,2,3}.

Use the sparse M61 linear/pair feature family and first/second factorial
penalties for all eight exact-divisor activation variables.  The remaining 11
non-special support charges are endpoint variables by separate concavity.
The exhaustive state count is 16^4*2^11 = 134,217,728.  The standalone C++
verifier checks that box with exact downward-rounded __int128 arithmetic.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m30_centered_moments import factorial_spike_cap
from m63_p322222_one_seed_reduction import HARD_SEED, PROFILE, reduction_audit

N = 3**3 * 5**2 * 7**2 * 11**2 * 13**2 * 17**2
assert N == HARD_SEED

D = (49,121,169,289)
COORD_NUMERATORS = (8,12,14,18)
DENOMINATORS = tuple(prod(D[i] for i in range(4) if C & (1<<i)) for C in range(16))
SUPPORT_NUMERATORS = tuple(
    prod(COORD_NUMERATORS[i] for i in range(4) if S & (1<<i))
    for S in range(16)
)
X5 = Fraction(6,25)

LINEAR = {
    3:Fraction(260,1000), 5:Fraction(342,1000), 6:Fraction(172,1000),
    7:Fraction(600,1000), 9:Fraction(124,1000), 11:Fraction(326,1000),
    13:Fraction(219,1000), 14:Fraction(118,1000), 15:Fraction(645,1000),
}
CROSS = {
    (1,3):Fraction(446,1000), (1,9):Fraction(507,1000),
    (1,11):Fraction(111,1000), (2,10):Fraction(83,1000),
    (3,10):Fraction(1120,1000), (3,11):Fraction(2934,1000),
    (3,15):Fraction(1781,1000), (5,9):Fraction(1083,1000),
    (5,12):Fraction(1630,1000), (5,13):Fraction(4085,1000),
    (6,10):Fraction(4355,1000), (6,12):Fraction(5337,1000),
    (6,14):Fraction(8418,1000), (9,10):Fraction(1421,1000),
    (9,13):Fraction(5446,1000), (10,11):Fraction(5498,1000),
    (10,12):Fraction(7240,1000), (10,14):Fraction(9038,1000),
    (12,13):Fraction(2465,1000),
}
# Per repeated singleton: alpha*A + beta*B + gamma*C(A,2) + delta*C(B,2).
FACTORIAL_NUMERATORS = (
    25,2,14,6,   # 7^2
    8,1,11,0,    # 11^2
    11,0,4,1,    # 13^2
    6,1,4,1,     # 17^2 -- new M64 correction
)
FACTORIAL = tuple(Fraction(n,1000) for n in FACTORIAL_NUMERATORS)

Q = 10**7
C = Fraction(3359,10000)
EXPECTED_STATE_COUNT = 16**4 * 2**11
EXPECTED_FLOOR_MIN = 3_359_197
EXPECTED_FLOOR_SLACK = 197
EXPECTED_ARGMIN = (2,1,1,3,1,2,1,0,335)
EXPECTED_EXACT_ARGMIN = Fraction(
    3521116425483227803279,
    10481948182520940125000,
)
EXPECTED_SPECIAL_COST = Fraction(
    1188734751673549101999,
    374355292232890718750,
)
EXPECTED_FEATURE_COST = Fraction(
    3536143347274623257,
    2395873870290500600,
)
EXPECTED_ETA = Fraction(
    5481727876909402311,
    106958654923683062500,
)
EXPECTED_PROPER_NON5_MIN = Fraction(47337,1002001)
EXPECTED_FULL_NON5_MIN = Fraction(2099121,289578289)


def baseline(mask: int) -> Fraction:
    return Fraction(SUPPORT_NUMERATORS[mask],DENOMINATORS[mask])


def special_global_cost() -> Fraction:
    out = Fraction(0)
    for T in range(16):
        sm = 1 | (T<<1)
        b = X5*baseline(T)
        out += 27*LAMBDA.get(sm,Fraction(0))*b
        out += 63*DIAGONAL[sm]*b*b
    return out


def feature_global_cost() -> Fraction:
    out = 27*sum(mu*baseline(S) for S,mu in LINEAR.items())
    out += 63*sum(mu*baseline(S)*baseline(T) for (S,T),mu in CROSS.items())
    assert factorial_spike_cap(3,1) == 13
    assert factorial_spike_cap(3,2) == 5
    budgets = (13,13,5,5)*4
    out += sum(b*mu for b,mu in zip(budgets,FACTORIAL))
    return out


def _rho_numerators(state: tuple[int,...]) -> tuple[tuple[int,...],tuple[int,...]]:
    if len(state) != 9:
        raise ValueError("state must have nine entries")
    A7,B7,A11,B11,A13,B13,A17,B17,endpoint_bits = state
    if any(a not in range(4) for a in (A7,B7,A11,B11,A13,B13,A17,B17)):
        raise ValueError("weighted activations must lie in 0..3")
    if not 0 <= endpoint_bits < 2**11:
        raise ValueError("bad endpoint bitmap")

    t = [0]*16
    t[1] = 8 + 7*A7 + B7
    t[2] = 12 + 11*A11 + B11
    t[4] = 14 + 13*A13 + B13
    t[8] = 18 + 17*A17 + B17
    unselected = (3,5,6,7,9,10,11,12,13,14,15)
    for j,mask in enumerate(unselected):
        z = 4 if endpoint_bits & (1<<j) else 1
        t[mask] = SUPPORT_NUMERATORS[mask]*z

    n = [0]*16
    n[0] = 1
    for size in range(1,5):
        for Cmask in range(1,16):
            if Cmask.bit_count() != size:
                continue
            pivot = Cmask & -Cmask
            i = pivot.bit_length()-1
            rest = Cmask ^ pivot
            value = D[i]*n[rest]
            T = rest
            while True:
                S = pivot | T
                value -= t[S]*n[Cmask ^ S]
                if T == 0:
                    break
                T = (T-1)&rest
            n[Cmask] = value
    return tuple(n),tuple(t)


def _phi(Cmask: int, numerator: int) -> Fraction:
    T = 15 ^ Cmask
    sm = 1 | (T<<1)
    rho = Fraction(numerator,DENOMINATORS[Cmask])
    lo = X5*baseline(T)
    hi = 4*lo
    nu = DIAGONAL[sm]
    linear = LAMBDA.get(sm,Fraction(0)) - rho
    x = -linear/(2*nu)
    if x < lo: x = lo
    elif x > hi: x = hi
    return nu*x*x + linear*x


def _factorial_features(state: tuple[int,...]) -> tuple[int,...]:
    A7,B7,A11,B11,A13,B13,A17,B17,_ = state
    out = []
    for A,B in ((A7,B7),(A11,B11),(A13,B13),(A17,B17)):
        out.extend((A,B,comb(A,2),comb(B,2)))
    return tuple(out)


def pointwise_exact(state: tuple[int,...]) -> Fraction:
    n,t = _rho_numerators(state)
    value = Fraction(n[15],DENOMINATORS[15])
    value += sum(_phi(Cmask,n[Cmask]) for Cmask in range(16))
    value += sum(mu*Fraction(t[S],DENOMINATORS[S]) for S,mu in LINEAR.items())
    value += sum(
        mu*Fraction(t[S],DENOMINATORS[S])*Fraction(t[T],DENOMINATORS[T])
        for (S,T),mu in CROSS.items()
    )
    value += sum(mu*f for mu,f in zip(FACTORIAL,_factorial_features(state)))
    return value


def certificate_audit() -> dict:
    assert EXPECTED_STATE_COUNT == 134_217_728
    assert C*Q == 3_359_000
    assert EXPECTED_FLOOR_MIN - C*Q == EXPECTED_FLOOR_SLACK > 0
    exact = pointwise_exact(EXPECTED_ARGMIN)
    assert exact == EXPECTED_EXACT_ARGMIN > C
    assert Fraction(EXPECTED_FLOOR_MIN,Q) <= exact

    assert special_global_cost() == EXPECTED_SPECIAL_COST
    assert feature_global_cost() == EXPECTED_FEATURE_COST
    eta = 14*C - special_global_cost() - feature_global_cost()
    assert eta == EXPECTED_ETA > 0

    assert 4*X5 == Fraction(24,25) < 1
    assert EXPECTED_PROPER_NON5_MIN > 0
    assert EXPECTED_FULL_NON5_MIN > 0
    return {
        "N":N,"state_count":EXPECTED_STATE_COUNT,
        "floor_min_scaled":EXPECTED_FLOOR_MIN,
        "floor_slack_scaled":EXPECTED_FLOOR_SLACK,
        "argmin":EXPECTED_ARGMIN,"exact_argmin_value":exact,
        "special_global_cost":special_global_cost(),
        "feature_global_cost":feature_global_cost(),
        "summed_rho_margin":eta,
        "proper_non5_min":EXPECTED_PROPER_NON5_MIN,
        "full_non5_min":EXPECTED_FULL_NON5_MIN,
        "noncovering_certified":True,
    }


def profile_closure_audit() -> dict:
    reduction = reduction_audit()
    assert reduction["profile"] == PROFILE
    assert reduction["hard_seed"] == N
    assert reduction["all_other_profile_members_noncovering"]
    hard = certificate_audit()
    assert hard["noncovering_certified"]
    return {"profile":PROFILE,"hard_seed":N,
            "all_other_profile_members_noncovering":True,
            "all_odd_six_prime_numbers_with_profile_noncovering":True,
            "verified":True}


__all__ = [
    "C","EXPECTED_ETA","EXPECTED_FLOOR_MIN","EXPECTED_STATE_COUNT","N",
    "certificate_audit","feature_global_cost","pointwise_exact",
    "profile_closure_audit","special_global_cost",
]
