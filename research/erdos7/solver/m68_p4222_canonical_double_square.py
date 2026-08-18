"""M68: exact double-weighted-square certificate for the canonical P4222 seed.

Target:
    N = 3^4 * 5^2 * 7^2 * 11^2 * 13 * 17.

Stage on 3^4 and distinguish 5^2.  Retain the exact two-level activations
of the repeated non-special singletons 7^2 and 11^2,

    q_7 / b_7   = 1 + (7 A_7 + B_7)/8,
    q_11 / b_11 = 1 + (11 A_11 + B_11)/12,

with A,B in {0,...,4}; retain the exact integral levels of the simple
singletons 13 and 17.  The remaining eleven non-special support charges
are endpoint variables by separate concavity.

A sparse nonnegative family of linear and distinct-support pair penalties,
plus first/second factorial penalties on the six retained activations, is
certified by a standalone exact integer exhaustive verifier.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m28_moment_hierarchy import moment_constant
from m30_centered_moments import factorial_spike_cap

PROFILE = (4, 2, 2, 2, 1, 1)
N = 3**4 * 5**2 * 7**2 * 11**2 * 13 * 17
assert N == 2653375725

# Local non-special order: (7^2, 11^2, 13, 17).
D = (49, 121, 13, 17)
NUM = (8, 12, 1, 1)
DEN = tuple(prod(D[i] for i in range(4) if mask & (1 << i)) for mask in range(16))
BASE_NUM = tuple(prod(NUM[i] for i in range(4) if mask & (1 << i)) for mask in range(16))
X5 = Fraction(6, 25)
UNSELECTED = (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)

COEFF_DEN = 10**6
LINEAR_NUM = {
    3: 299988, 5: 241193, 6: 276475, 7: 506889, 9: 201268,
    10: 206611, 11: 446165, 12: 133302, 13: 361344,
    14: 380235, 15: 661097,
}
CROSS_NUM = {
    (1,3):382568, (1,5):411361, (1,7):14485, (1,9):428912,
    (1,11):62436, (1,13):204817, (2,6):134032, (2,10):271704,
    (2,14):62928, (3,5):365281, (3,7):1035159, (3,9):325072,
    (3,11):1302286, (3,15):660125, (4,12):333243, (5,7):1025825,
    (5,9):282823, (5,13):1304830, (5,15):256337, (6,10):421152,
    (6,12):136703, (6,14):812335, (7,11):6428064, (7,13):2762026,
    (7,15):3929384, (8,12):295228, (9,11):1001449, (9,13):1327325,
    (10,12):348076, (10,14):518787, (11,13):2189698, (11,15):5138425,
}
# Per activation X: alpha*X + beta*C(X,2), in order
# A7, B7, A11, B11, A13, A17.
FACTORIAL_NUM = (
    23938,14204, 4242,1863, 9824,8107,
    1160,584, 8180,5282, 6182,3034,
)

LINEAR = {m: Fraction(c, COEFF_DEN) for m, c in LINEAR_NUM.items()}
CROSS = {st: Fraction(c, COEFF_DEN) for st, c in CROSS_NUM.items()}
FACTORIAL = tuple(Fraction(c, COEFF_DEN) for c in FACTORIAL_NUM)

C = Fraction(34795, 100000)
Q = 10**9
EXPECTED_STATE_COUNT = 25**2 * 5**2 * 2**11
EXPECTED_FLOOR_MIN = 347_959_679
EXPECTED_FLOOR_SLACK = 9_679
EXPECTED_ARGMIN = (0, 0, 0, 0, 1, 1, 0)
EXPECTED_EXACT_ARGMIN = Fraction(
    140088010630411032032228450809957711087,
    402598364961488706245123434706160000000,
)
EXPECTED_SPECIAL_COST = Fraction(
    5146853782690471671,
    536534273587812500,
)
EXPECTED_FEATURE_COST = Fraction(
    7945074076619350717,
    1716909675481000000,
)
EXPECTED_ETA = Fraction(
    391707018496559429,
    8584548377405000000,
)


def baseline(mask: int) -> Fraction:
    return Fraction(BASE_NUM[mask], DEN[mask])


def _rho(q: dict[int, Fraction]) -> dict[int, Fraction]:
    rho = {0: Fraction(1)}
    for size in range(1, 5):
        for Cmask in range(1, 16):
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
    return rho


def _quadratic_min(linear: Fraction, quadratic: Fraction,
                   lo: Fraction, hi: Fraction) -> Fraction:
    x = -linear / (2 * quadratic)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return linear * x + quadratic * x * x


def local_q(state: tuple[int, ...]) -> dict[int, Fraction]:
    A7, B7, A11, B11, z13, z17, bits = state
    if any(x not in range(5) for x in (A7, B7, A11, B11)):
        raise ValueError("two-level activations must lie in 0..4")
    if z13 not in range(1, 6) or z17 not in range(1, 6):
        raise ValueError("simple activation levels must lie in 1..5")
    if not 0 <= bits < 2**11:
        raise ValueError("bad endpoint bitmap")

    q = {
        1: Fraction(8 + 7*A7 + B7, 49),
        2: Fraction(12 + 11*A11 + B11, 121),
        4: Fraction(z13, 13),
        8: Fraction(z17, 17),
    }
    for j, mask in enumerate(UNSELECTED):
        q[mask] = baseline(mask) * (5 if bits & (1 << j) else 1)
    return q


def pointwise_exact(state: tuple[int, ...]) -> Fraction:
    q = local_q(state)
    rho = _rho(q)

    pcoord = Fraction(0)
    full = rho[15]
    for T in range(16):
        sm = 1 | (T << 1)
        lo = X5 * baseline(T)
        hi = 5 * lo
        pcoord += LAMBDA.get(sm, Fraction(0)) * lo + DIAGONAL[sm] * lo * lo
        linear = LAMBDA.get(sm, Fraction(0)) - rho[15 ^ T]
        full += _quadratic_min(linear, DIAGONAL[sm], lo, hi)

    coordinate = min(rho[Cmask] for Cmask in range(1, 16)) + pcoord
    value = min(full, coordinate)
    value += sum(mu * q[m] for m, mu in LINEAR.items())
    value += sum(mu * q[s] * q[t] for (s, t), mu in CROSS.items())

    A7, B7, A11, B11, z13, z17, _ = state
    acts = (A7, B7, A11, B11, z13 - 1, z17 - 1)
    for j, A in enumerate(acts):
        value += FACTORIAL[2*j] * A
        value += FACTORIAL[2*j + 1] * comb(A, 2)
    return value


def special_global_cost() -> Fraction:
    out = Fraction(0)
    for T in range(16):
        sm = 1 | (T << 1)
        b = X5 * baseline(T)
        out += 81 * LAMBDA.get(sm, Fraction(0)) * b
        out += 197 * DIAGONAL[sm] * b * b
    return out


def feature_global_cost() -> Fraction:
    assert moment_constant(4, 1) == 81
    assert moment_constant(4, 2) == 197
    assert factorial_spike_cap(4, 1) == 40
    assert factorial_spike_cap(4, 2) == 18

    out = 81 * sum(mu * baseline(m) for m, mu in LINEAR.items())
    out += 197 * sum(mu * baseline(s) * baseline(t)
                     for (s, t), mu in CROSS.items())
    for j in range(6):
        out += 40 * FACTORIAL[2*j]
        out += 18 * FACTORIAL[2*j + 1]
    return out


def certificate_audit() -> dict:
    assert EXPECTED_STATE_COUNT == 32_000_000
    assert C * Q == 347_950_000
    assert EXPECTED_FLOOR_MIN - C * Q == EXPECTED_FLOOR_SLACK > 0

    exact = pointwise_exact(EXPECTED_ARGMIN)
    assert exact == EXPECTED_EXACT_ARGMIN > C
    assert Fraction(EXPECTED_FLOOR_MIN, Q) <= exact

    assert special_global_cost() == EXPECTED_SPECIAL_COST
    assert feature_global_cost() == EXPECTED_FEATURE_COST
    eta = 41*C - special_global_cost() - feature_global_cost()
    assert eta == EXPECTED_ETA > 0

    return {
        "N": N,
        "profile": PROFILE,
        "state_count": EXPECTED_STATE_COUNT,
        "floor_min_scaled": EXPECTED_FLOOR_MIN,
        "floor_slack_scaled": EXPECTED_FLOOR_SLACK,
        "argmin": EXPECTED_ARGMIN,
        "exact_argmin_value": exact,
        "summed_goodness_margin": eta,
        "noncovering_certified": True,
        "verified": True,
    }


__all__ = [
    "C", "CROSS_NUM", "EXPECTED_ETA", "EXPECTED_FLOOR_MIN",
    "EXPECTED_STATE_COUNT", "FACTORIAL_NUM", "LINEAR_NUM", "N", "PROFILE",
    "certificate_audit", "feature_global_cost", "local_q", "pointwise_exact",
    "special_global_cost",
]
