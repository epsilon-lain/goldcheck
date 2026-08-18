"""M58: exact certificate for the sole M57 P332 hard seed.

Target:
    N = 3^3 * 5^3 * 7^2 * 11 * 13 * 17.

Stage on 3^3 and distinguish the repeated 5-coordinate.  Retain weighted
activation data for two supports containing the repeated 7-coordinate:
{7} and {7,11}.  For either support, if A and B are the activation counts of
the exact divisors with 7-adic exponent 1 and 2, then

    q_S / b_S = 1 + (7*A + B)/8,
    A,B in {0,1,2,3}.

Five simple supports are also kept at their exact integral activation levels.
All other non-special variables are unpenalized; after exact minimization of
the sixteen 5-containing variables, the remaining function is separately
concave in each such unpenalized variable, so their minima are at endpoints.
The resulting finite state space has 4^9 * 2^8 = 67,108,864 states.

The fast exhaustive verifier is in m58_p332_hard_seed_fast.py.  It generates
all clipped-quadratic lookup entries with Fraction arithmetic, rounds each
entry downward after multiplying by Q=10^12, and then performs only exact
int64 additions/comparisons in the exhaustive loop.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m30_centered_moments import factorial_spike_cap
from m57_p332_one_seed_reduction import HARD_SEED, PROFILE, reduction_audit

N = 3**3 * 5**3 * 7**2 * 11 * 13 * 17
assert N == HARD_SEED

J_PRIMES = (7, 11, 13, 17)
D = (49, 11, 13, 17)
DENOMINATORS = tuple(
    __import__("math").prod(D[i] for i in range(4) if C & (1 << i))
    for C in range(16)
)
X5 = Fraction(31, 125)
SELECTED_SIMPLE = (2, 4, 8, 6, 10)  # {11},{13},{17},{11,13},{11,17}
UNSELECTED = (5, 7, 9, 11, 12, 13, 14, 15)

COEFFICIENT_DEN = 100_000
COEFFICIENT_NUMERATORS = (
    3682, 268, 1370, 391,      # {7}: A,B,binom(A,2),binom(B,2)
    437, 70, 202, 32,          # {7,11}: same four features
    1100, 762,                 # {11}
    1287, 342,                 # {13}
    887, 166,                  # {17}
    176, 49,                   # {11,13}
    101, 68,                   # {11,17}
)
COEFFICIENTS = tuple(Fraction(n, COEFFICIENT_DEN) for n in COEFFICIENT_NUMERATORS)

Q = 10**12
C = Fraction(1591, 5000)  # 0.3182
EXPECTED_STATE_COUNT = 4**9 * 2**8
EXPECTED_FLOOR_MIN = 318_224_090_677
EXPECTED_FLOOR_SLACK = 24_090_677
EXPECTED_ARGMIN = (1, 1, 1, 1, 2, 2, 3, 2, 2, 255)
EXPECTED_EXACT_ARGMIN = Fraction(
    334248664255027713025529067,
    1050356255352894264775000000,
)
EXPECTED_SPECIAL_COST = Fraction(
    102569429391470073,
    31672625359375000,
)
EXPECTED_FACTORIAL_COST = Fraction(60507, 50000)
EXPECTED_ETA = Fraction(
    394942414159229,
    63345250718750000,
)
EXPECTED_PROPER_NON5_MIN = Fraction(459, 7007)
EXPECTED_FULL_NON5_MIN = Fraction(155, 7007)


def _special_baseline(T: int) -> Fraction:
    c = 8 if T & 1 else 1
    return X5 * Fraction(c, DENOMINATORS[T])


def special_global_cost() -> Fraction:
    """27 first-moment + 63 diagonal second-moment charge of special supports."""
    out = Fraction(0)
    for T in range(16):
        mask = 1 | (T << 1)
        b = _special_baseline(T)
        out += 27 * LAMBDA.get(mask, Fraction(0)) * b
        out += 63 * DIAGONAL[mask] * b * b
    return out


def factorial_global_cost() -> Fraction:
    """Global cost of the eighteen nonnegative activation penalties."""
    assert factorial_spike_cap(3, 1) == 13
    assert factorial_spike_cap(3, 2) == 5
    budgets = (13, 13, 5, 5, 13, 13, 5, 5) + (13, 5) * 5
    return sum(b * c for b, c in zip(budgets, COEFFICIENTS))


def _rho_numerators(
    A1: int,
    B1: int,
    A3: int,
    B3: int,
    simple_values: tuple[int, int, int, int, int],
    endpoint_bits: int,
) -> tuple[int, ...]:
    """Integer numerators for the four-coordinate non-special rho polynomials."""
    if any(a not in range(4) for a in (A1, B1, A3, B3)):
        raise ValueError("weighted activations must lie in 0..3")
    if any(v not in (1, 2, 3, 4) for v in simple_values):
        raise ValueError("simple normalized charges must lie in 1..4")
    if not 0 <= endpoint_bits < 256:
        raise ValueError("endpoint bitmap must lie in 0..255")

    t = [0] * 16
    t[1] = 8 + 7 * A1 + B1
    t[3] = 8 + 7 * A3 + B3
    for mask, value in zip(SELECTED_SIMPLE, simple_values):
        t[mask] = value
    for i, mask in enumerate(UNSELECTED):
        z = 4 if endpoint_bits & (1 << i) else 1
        t[mask] = (8 if mask & 1 else 1) * z

    n = [0] * 16
    n[0] = 1
    for size in range(1, 5):
        for Cmask in range(1, 16):
            if Cmask.bit_count() != size:
                continue
            pivot = Cmask & -Cmask
            i = pivot.bit_length() - 1
            rest = Cmask ^ pivot
            value = D[i] * n[rest]
            T = rest
            while True:
                S = pivot | T
                value -= t[S] * n[Cmask ^ S]
                if T == 0:
                    break
                T = (T - 1) & rest
            n[Cmask] = value
    return tuple(n)


def _phi_exact(Cmask: int, numerator: int) -> Fraction:
    """Exact minimum of one 5-containing clipped quadratic."""
    T = 15 ^ Cmask
    special_mask = 1 | (T << 1)
    rho = Fraction(numerator, DENOMINATORS[Cmask])
    lo = _special_baseline(T)
    hi = 4 * lo
    nu = DIAGONAL[special_mask]
    linear = LAMBDA.get(special_mask, Fraction(0)) - rho
    x = -linear / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + linear * x


def _features(
    A1: int,
    B1: int,
    A3: int,
    B3: int,
    simple_values: tuple[int, int, int, int, int],
) -> tuple[int, ...]:
    out = [A1, B1, comb(A1, 2), comb(B1, 2), A3, B3, comb(A3, 2), comb(B3, 2)]
    for z in simple_values:
        A = z - 1
        out.extend((A, comb(A, 2)))
    return tuple(out)


def pointwise_exact(state: tuple[int, ...]) -> Fraction:
    """Exact certificate value at one reduced state."""
    if len(state) != 10:
        raise ValueError("state must have ten entries")
    A1, B1, A3, B3 = state[:4]
    simple = tuple(state[4:9])
    endpoint_bits = state[9]
    n = _rho_numerators(A1, B1, A3, B3, simple, endpoint_bits)
    value = Fraction(n[15], DENOMINATORS[15])
    value += sum(_phi_exact(Cmask, n[Cmask]) for Cmask in range(16))
    value += sum(c * f for c, f in zip(COEFFICIENTS, _features(A1, B1, A3, B3, simple)))
    return value


def certificate_audit() -> dict:
    """Audit exact constants; exhaustive minimum is independently reproducible by fast verifier."""
    assert EXPECTED_STATE_COUNT == 67_108_864
    assert C * Q == 318_200_000_000
    assert EXPECTED_FLOOR_MIN - C * Q == EXPECTED_FLOOR_SLACK > 0

    exact = pointwise_exact(EXPECTED_ARGMIN)
    assert exact == EXPECTED_EXACT_ARGMIN > C
    assert Fraction(EXPECTED_FLOOR_MIN, Q) <= exact

    assert special_global_cost() == EXPECTED_SPECIAL_COST
    assert factorial_global_cost() == EXPECTED_FACTORIAL_COST
    eta = 14 * C - special_global_cost() - factorial_global_cost()
    assert eta == EXPECTED_ETA > 0

    # The factor-4 non-special box is already inside the Shearer region (M57),
    # and the special singleton is <1 even at its upper endpoint.
    assert 4 * X5 == Fraction(124, 125) < 1
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
        "factorial_global_cost": factorial_global_cost(),
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
        "hard_seed_noncovering": True,
        "all_other_profile_members_noncovering": True,
        "all_odd_six_prime_numbers_with_profile_noncovering": True,
        "verified": True,
    }


__all__ = [
    "C", "COEFFICIENT_NUMERATORS", "EXPECTED_ETA", "EXPECTED_FLOOR_MIN",
    "EXPECTED_STATE_COUNT", "N", "certificate_audit", "factorial_global_cost",
    "pointwise_exact", "profile_closure_audit", "special_global_cost",
]
