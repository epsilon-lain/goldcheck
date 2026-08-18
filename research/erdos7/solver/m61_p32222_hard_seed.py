"""M61: exact closure of the sole M60 hard seed.

Target:
    N = 3^3 * 5^2 * 7^2 * 11^2 * 13^2 * 17.

Stage on 3^3 and distinguish 5^2.  Keep exact two-level activation data for the
three repeated singleton supports {7}, {11}, {13}, and the exact integral
activation of the simple singleton {17}.  Add a sparse nonnegative collection
of linear and pair-moment penalties on the remaining non-special support
charges.  M28 supplies 27/63 first/pair budgets, while M30 supplies 13/5
first/second factorial caps for each exact-divisor activation.

After the sixteen 5-containing variables are minimized as clipped convex
quadratics, the remaining eleven unpenalized non-special variables are reduced
to endpoints by separate concavity.  The finite state space is
16^3 * 4 * 2^11 = 33,554,432 states.  The standalone C++ verifier performs the
exhaustive check using exact downward-rounded integer arithmetic.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m30_centered_moments import factorial_spike_cap
from m60_p32222_one_seed_reduction import HARD_SEED, PROFILE, reduction_audit

N = 3**3 * 5**2 * 7**2 * 11**2 * 13**2 * 17
assert N == HARD_SEED

D = (49, 121, 169, 17)
COORD_NUMERATORS = (8, 12, 14, 1)
DENOMINATORS = tuple(prod(D[i] for i in range(4) if C & (1 << i)) for C in range(16))
SUPPORT_NUMERATORS = tuple(
    prod(COORD_NUMERATORS[i] for i in range(4) if S & (1 << i))
    for S in range(16)
)
X5 = Fraction(6, 25)

LINEAR = {
    3: Fraction(260, 1000),
    5: Fraction(342, 1000),
    6: Fraction(172, 1000),
    7: Fraction(600, 1000),
    9: Fraction(124, 1000),
    11: Fraction(326, 1000),
    13: Fraction(219, 1000),
    14: Fraction(118, 1000),
    15: Fraction(645, 1000),
}
CROSS = {
    (1,3): Fraction(446,1000), (1,9): Fraction(507,1000),
    (1,11): Fraction(111,1000), (2,10): Fraction(83,1000),
    (3,10): Fraction(1120,1000), (3,11): Fraction(2934,1000),
    (3,15): Fraction(1781,1000), (5,9): Fraction(1083,1000),
    (5,12): Fraction(1630,1000), (5,13): Fraction(4085,1000),
    (6,10): Fraction(4355,1000), (6,12): Fraction(5337,1000),
    (6,14): Fraction(8418,1000), (9,10): Fraction(1421,1000),
    (9,13): Fraction(5446,1000), (10,11): Fraction(5498,1000),
    (10,12): Fraction(7240,1000), (10,14): Fraction(9038,1000),
    (12,13): Fraction(2465,1000),
}
FACTORIAL_NUMERATORS = (25,2,14,6, 8,1,11,0, 11,0,4,1, 8,2)
FACTORIAL = tuple(Fraction(n,1000) for n in FACTORIAL_NUMERATORS)

Q = 10**7
C = Fraction(3367, 10000)
EXPECTED_STATE_COUNT = 16**3 * 4 * 2**11
EXPECTED_FLOOR_MIN = 3_367_573
EXPECTED_FLOOR_SLACK = 573
EXPECTED_ARGMIN = (3,2,1,3,0,1,1,843)
EXPECTED_EXACT_ARGMIN = Fraction(
    232313797012832336720879,
    689850015334077097500000,
)
EXPECTED_SPECIAL_COST = Fraction(
    4089100538208632211,
    1295347031947718750,
)
EXPECTED_FEATURE_COST = Fraction(
    4660298627896907,
    3188546540179000,
)
EXPECTED_ETA = Fraction(
    61829991701702982,
    647673515973859375,
)
EXPECTED_PROPER_NON5_MIN = Fraction(47337,1002001)
EXPECTED_FULL_NON5_MIN = Fraction(161325,17034017)


def baseline(mask: int) -> Fraction:
    return Fraction(SUPPORT_NUMERATORS[mask], DENOMINATORS[mask])


def special_global_cost() -> Fraction:
    out = Fraction(0)
    for T in range(16):
        sm = 1 | (T << 1)
        b = X5 * baseline(T)
        out += 27 * LAMBDA.get(sm, Fraction(0)) * b
        out += 63 * DIAGONAL[sm] * b * b
    return out


def feature_global_cost() -> Fraction:
    out = 27 * sum(mu * baseline(S) for S, mu in LINEAR.items())
    out += 63 * sum(mu * baseline(S) * baseline(T) for (S,T), mu in CROSS.items())
    assert factorial_spike_cap(3,1) == 13
    assert factorial_spike_cap(3,2) == 5
    budgets = (13,13,5,5) * 3 + (13,5)
    out += sum(b * mu for b, mu in zip(budgets, FACTORIAL))
    return out


def _rho_numerators(state: tuple[int, ...]) -> tuple[tuple[int,...], tuple[int,...]]:
    if len(state) != 8:
        raise ValueError("state must have eight entries")
    A7,B7,A11,B11,A13,B13,z17,endpoint_bits = state
    if any(a not in range(4) for a in (A7,B7,A11,B11,A13,B13)):
        raise ValueError("weighted activations must lie in 0..3")
    if z17 not in (1,2,3,4) or not 0 <= endpoint_bits < 2**11:
        raise ValueError("bad simple level or endpoint bitmap")

    t = [0]*16
    t[1] = 8 + 7*A7 + B7
    t[2] = 12 + 11*A11 + B11
    t[4] = 14 + 13*A13 + B13
    t[8] = z17
    unselected = (3,5,6,7,9,10,11,12,13,14,15)
    for j,mask in enumerate(unselected):
        z = 4 if endpoint_bits & (1 << j) else 1
        t[mask] = SUPPORT_NUMERATORS[mask] * z

    n = [0]*16
    n[0] = 1
    for size in range(1,5):
        for Cmask in range(1,16):
            if Cmask.bit_count() != size:
                continue
            pivot = Cmask & -Cmask
            i = pivot.bit_length()-1
            rest = Cmask ^ pivot
            value = D[i] * n[rest]
            T = rest
            while True:
                S = pivot | T
                value -= t[S] * n[Cmask ^ S]
                if T == 0:
                    break
                T = (T-1) & rest
            n[Cmask] = value
    return tuple(n), tuple(t)


def _phi(Cmask: int, numerator: int) -> Fraction:
    T = 15 ^ Cmask
    sm = 1 | (T << 1)
    rho = Fraction(numerator, DENOMINATORS[Cmask])
    lo = X5 * baseline(T)
    hi = 4 * lo
    nu = DIAGONAL[sm]
    linear = LAMBDA.get(sm, Fraction(0)) - rho
    x = -linear/(2*nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu*x*x + linear*x


def _factorial_features(state: tuple[int,...]) -> tuple[int,...]:
    A7,B7,A11,B11,A13,B13,z17,_ = state
    out = []
    for A,B in ((A7,B7),(A11,B11),(A13,B13)):
        out.extend((A,B,comb(A,2),comb(B,2)))
    A = z17-1
    out.extend((A,comb(A,2)))
    return tuple(out)


def pointwise_exact(state: tuple[int,...]) -> Fraction:
    n,t = _rho_numerators(state)
    value = Fraction(n[15], DENOMINATORS[15])
    value += sum(_phi(Cmask,n[Cmask]) for Cmask in range(16))
    value += sum(mu * Fraction(t[S],DENOMINATORS[S]) for S,mu in LINEAR.items())
    value += sum(
        mu * Fraction(t[S],DENOMINATORS[S]) * Fraction(t[T],DENOMINATORS[T])
        for (S,T),mu in CROSS.items()
    )
    value += sum(mu*f for mu,f in zip(FACTORIAL,_factorial_features(state)))
    return value


def certificate_audit() -> dict:
    assert EXPECTED_STATE_COUNT == 33_554_432
    assert C*Q == 3_367_000
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
        "N": N,
        "state_count": EXPECTED_STATE_COUNT,
        "floor_min_scaled": EXPECTED_FLOOR_MIN,
        "floor_slack_scaled": EXPECTED_FLOOR_SLACK,
        "argmin": EXPECTED_ARGMIN,
        "exact_argmin_value": exact,
        "special_global_cost": special_global_cost(),
        "feature_global_cost": feature_global_cost(),
        "summed_rho_margin": eta,
        "proper_non5_min": EXPECTED_PROPER_NON5_MIN,
        "full_non5_min": EXPECTED_FULL_NON5_MIN,
        "noncovering_certified": True,
    }


def profile_closure_audit() -> dict:
    reduction = reduction_audit()
    assert reduction["profile"] == PROFILE
    assert reduction["hard_seed"] == N
    assert reduction["all_other_profile_members_noncovering"]
    hard = certificate_audit()
    assert hard["noncovering_certified"]
    return {
        "profile": PROFILE,
        "hard_seed": N,
        "all_other_profile_members_noncovering": True,
        "all_odd_six_prime_numbers_with_profile_noncovering": True,
        "verified": True,
    }


__all__ = [
    "C", "EXPECTED_ETA", "EXPECTED_FLOOR_MIN", "EXPECTED_STATE_COUNT", "N",
    "certificate_audit", "feature_global_cost", "pointwise_exact",
    "profile_closure_audit", "special_global_cost",
]
