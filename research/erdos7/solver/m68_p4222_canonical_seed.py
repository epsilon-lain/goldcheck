"""M68: exact certificate for the canonical P4222 minimal seed.

Target
------
    N = 3^4 * 5^2 * 7^2 * 11^2 * 13 * 17.

Stage on 3^4, distinguish 5^2, and retain exact two-level singleton
activations for 7^2 and 11^2.  The simple singleton activations 13 and 17 are
also kept exactly.  The eleven remaining non-special support charges are
reduced to factor-5 endpoints by separate concavity.

The pointwise lower bound is the M66 goodness branch (minimum of full-rho and
all non-special coordinate rhos after the special-coordinate completion), plus
nonnegative linear, pair, and factorial penalties.  M28 supplies the 81/197
support first/pair budgets, and M30 supplies the 40/18 first/second factorial
caps for each exact-divisor activation.

The standalone C++ verifier checks

    25^2 * 5^2 * 2^11 = 32,000,000

states with exact downward-rounded integer arithmetic.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m28_moment_hierarchy import moment_constant
from m30_centered_moments import factorial_spike_cap

N = 3**4 * 5**2 * 7**2 * 11**2 * 13 * 17
assert N == 2_653_375_725

# Local non-special order: (7^2, 11^2, 13, 17).
D = (49, 121, 13, 17)
COORD_NUMERATORS = (8, 12, 1, 1)
DENOMINATORS = tuple(prod(D[i] for i in range(4) if C & (1 << i)) for C in range(16))
SUPPORT_NUMERATORS = tuple(
    prod(COORD_NUMERATORS[i] for i in range(4) if S & (1 << i))
    for S in range(16)
)
X5 = Fraction(6, 25)

LINEAR_MASKS = (3,5,6,7,9,10,11,12,13,14)
LINEAR_NUMERATORS = (29487,24837,29050,53691,19677,28831,49236,18917,51820,40706)
CROSS_PAIRS = (
    (1,3),(1,5),(1,9),(2,6),(3,5),(3,7),(3,9),(3,10),(3,11),(3,14),
    (4,12),(5,7),(5,9),(6,10),(7,9),(7,12),(9,10),(9,11),(10,13),(11,13),(12,14),
)
CROSS_NUMERATORS = (
    37491,39778,42878,9140,39045,133887,42725,0,145320,53495,33261,
    88993,37559,57052,0,0,0,81843,0,914418,61883,
)
# Pairs (first moment, second factorial moment) for
# A7,B7,A11,B11,(z13-1),(z17-1), denominator 100000.
FACTORIAL_NUMERATORS = (2433,1413,425,184,995,844,118,55,826,504,610,312)
COEFF_DEN = 100_000

Q = 10**9
C = Fraction(69699, 200000)  # 0.348495
EXPECTED_STATE_COUNT = 25**2 * 5**2 * 2**11
EXPECTED_FLOOR_MIN = 348_498_368
EXPECTED_FLOOR_SLACK = 3_368
EXPECTED_ARGMIN = (0,0,0,0,1,1,1024)
EXPECTED_EXACT_ARGMIN = Fraction(
    140304882616225190852074066798016594047,
    402598364961488706245123434706160000000,
)
EXPECTED_SPECIAL_COST = Fraction(
    5146853782690471671,
    536534273587812500,
)
EXPECTED_FEATURE_COST = Fraction(
    11425137346771651,
    2452728107830000,
)
EXPECTED_ETA = Fraction(
    320918421385649239,
    8584548377405000000,
)

UNSELECTED = (3,5,6,7,9,10,11,12,13,14,15)


def baseline(mask: int) -> Fraction:
    return Fraction(SUPPORT_NUMERATORS[mask], DENOMINATORS[mask])


def _quadratic_min(linear: Fraction, quadratic: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    x = -linear / (2 * quadratic)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return linear*x + quadratic*x*x


def _rho(state: tuple[int,...]) -> tuple[dict[int,Fraction], dict[int,Fraction]]:
    A7,B7,A11,B11,z13,z17,bits = state
    if any(a not in range(5) for a in (A7,B7,A11,B11)):
        raise ValueError("weighted activations must lie in 0..4")
    if z13 not in range(1,6) or z17 not in range(1,6) or not 0 <= bits < 2**11:
        raise ValueError("bad simple level or endpoint bitmap")

    q = {
        1: Fraction(8 + 7*A7 + B7, 49),
        2: Fraction(12 + 11*A11 + B11, 121),
        4: Fraction(z13, 13),
        8: Fraction(z17, 17),
    }
    for j,m in enumerate(UNSELECTED):
        q[m] = baseline(m) * (5 if bits & (1 << j) else 1)

    rho = {0: Fraction(1)}
    for size in range(1,5):
        for Cmask in range(1,16):
            if Cmask.bit_count() != size:
                continue
            pivot = Cmask & -Cmask
            rest = Cmask ^ pivot
            value = rho[rest]
            T = rest
            while True:
                S = pivot | T
                value -= q[S] * rho[Cmask ^ S]
                if T == 0:
                    break
                T = (T - 1) & rest
            rho[Cmask] = value
    return rho,q


def pointwise_exact(state: tuple[int,...]) -> Fraction:
    rho,q = _rho(state)
    pcoord = Fraction(0)
    full = rho[15]
    for T in range(16):
        sm = 1 | (T << 1)
        lo = X5 * baseline(T)
        hi = 5 * lo
        pcoord += LAMBDA.get(sm, Fraction(0))*lo + DIAGONAL[sm]*lo*lo
        full += _quadratic_min(
            LAMBDA.get(sm, Fraction(0)) - rho[15 ^ T],
            DIAGONAL[sm], lo, hi,
        )
    coordinate = min(rho[Cmask] for Cmask in range(1,16)) + pcoord
    value = min(full, coordinate)

    value += sum(
        Fraction(c,COEFF_DEN) * q[m]
        for m,c in zip(LINEAR_MASKS, LINEAR_NUMERATORS)
    )
    value += sum(
        Fraction(c,COEFF_DEN) * q[s] * q[t]
        for (s,t),c in zip(CROSS_PAIRS, CROSS_NUMERATORS)
    )
    acts = (state[0],state[1],state[2],state[3],state[4]-1,state[5]-1)
    for j,A in enumerate(acts):
        value += Fraction(FACTORIAL_NUMERATORS[2*j],COEFF_DEN) * A
        value += Fraction(FACTORIAL_NUMERATORS[2*j+1],COEFF_DEN) * comb(A,2)
    return value


def special_global_cost() -> Fraction:
    out = Fraction(0)
    for T in range(16):
        sm = 1 | (T << 1)
        b = X5 * baseline(T)
        out += 81 * LAMBDA.get(sm, Fraction(0)) * b
        out += 197 * DIAGONAL[sm] * b*b
    return out


def feature_global_cost() -> Fraction:
    out = 81 * sum(
        Fraction(c,COEFF_DEN) * baseline(m)
        for m,c in zip(LINEAR_MASKS, LINEAR_NUMERATORS)
    )
    out += 197 * sum(
        Fraction(c,COEFF_DEN) * baseline(s) * baseline(t)
        for (s,t),c in zip(CROSS_PAIRS, CROSS_NUMERATORS)
    )
    assert factorial_spike_cap(4,1) == 40
    assert factorial_spike_cap(4,2) == 18
    for j in range(6):
        out += 40 * Fraction(FACTORIAL_NUMERATORS[2*j],COEFF_DEN)
        out += 18 * Fraction(FACTORIAL_NUMERATORS[2*j+1],COEFF_DEN)
    return out


def certificate_audit() -> dict:
    assert moment_constant(4,1) == 81
    assert moment_constant(4,2) == 197
    assert EXPECTED_STATE_COUNT == 32_000_000
    assert C * Q == 348_495_000
    assert EXPECTED_FLOOR_MIN - C*Q == EXPECTED_FLOOR_SLACK > 0

    exact = pointwise_exact(EXPECTED_ARGMIN)
    assert exact == EXPECTED_EXACT_ARGMIN > C
    assert Fraction(EXPECTED_FLOOR_MIN,Q) <= exact

    assert special_global_cost() == EXPECTED_SPECIAL_COST
    assert feature_global_cost() == EXPECTED_FEATURE_COST
    eta = 41*C - special_global_cost() - feature_global_cost()
    assert eta == EXPECTED_ETA > 0
    assert 5*X5 == Fraction(6,5)  # goodness handles bad special upper branches pointwise
    return {
        "N": N,
        "state_count": EXPECTED_STATE_COUNT,
        "floor_min_scaled": EXPECTED_FLOOR_MIN,
        "floor_slack_scaled": EXPECTED_FLOOR_SLACK,
        "argmin": EXPECTED_ARGMIN,
        "exact_argmin_value": exact,
        "special_global_cost": special_global_cost(),
        "feature_global_cost": feature_global_cost(),
        "summed_goodness_margin": eta,
        "noncovering_certified": True,
    }


__all__ = [
    "C", "EXPECTED_ETA", "EXPECTED_FLOOR_MIN", "EXPECTED_STATE_COUNT", "N",
    "certificate_audit", "feature_global_cost", "pointwise_exact", "special_global_cost",
]
