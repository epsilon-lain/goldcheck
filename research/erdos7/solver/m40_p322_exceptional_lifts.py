"""M40: a quantitative a=3 precursor excludes the six noncanonical P322 seeds.

Profile P322=(3,2,2,1,1,1) has twelve M26 survivor seeds.  Six are canonical
with the second square on 7.  The other six put the second square on one of
11, 13, or P for P in {17,19}.

This module handles those six exceptional seeds.

Reference precursor
-------------------

    N0 = 3^3 * 5^2 * 7 * 11 * 13 * 17.

Stage on 3^3 and select 14 surviving fibres.  Distinguish the repeated prime
5^2.  The remaining coordinates 7,11,13,17 are simple, so every nonempty
support has one exact divisor and normalized charge

    z_S = q_S / b_S = 1 + A_S in {1,2,3,4}.

M30 gives the exact single-divisor factorial budgets

    sum A_S <= 13,
    sum binom(A_S,2) <= 5.

The pointwise certificate keeps the M25 nonnegative linear/diagonal penalties
on the sixteen supports containing 5 and adds first/second factorial penalties
on six simple supports.  Six variables are checked at all four integer levels
and the other nine at endpoints by separate concavity: 4^6*2^9=2,097,152
states.

The resulting quantitative summed-rho margin is then inflated/scaled from
P=17 to P=19.  The M39 quantitative completion lemma converts the margin into
a deficiency lower bound.  Applying the deficiency recurrence in each target
prime q in {11,13,P} excludes all six exceptional P322 seeds.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import comb, prod

from m25_cross_support_seed import DIAGONAL, LAMBDA
from m26_minimal_frontier import P322, SEEDS, family_number
from m30_centered_moments import factorial_spike_cap

REFERENCE_PRIMES = (7, 11, 13, 17)
SELECTED_SUPPORTS = (1, 2, 4, 8, 3, 5)
UNSELECTED_SUPPORTS = tuple(m for m in range(1, 16) if m not in SELECTED_SUPPORTS)
COEFFICIENT_DEN = 1_000_000
ALPHA_NUM = (23714, 15815, 12454, 8914, 4451, 3593)
BETA_NUM = (16013, 3158, 2217, 1344, 1418, 988)
ALPHA = tuple(Fraction(a, COEFFICIENT_DEN) for a in ALPHA_NUM)
BETA = tuple(Fraction(b, COEFFICIENT_DEN) for b in BETA_NUM)

Q = 10**12
C = Fraction(3219, 10000)
EXPECTED_STATE_COUNT = 4**6 * 2**9
EXPECTED_FLOOR_MIN = 321_924_524_492
EXPECTED_FLOOR_SLACK = 24_524_492
EXPECTED_ARGMIN = (2, 2, 2, 4, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4)
EXPECTED_EXACT_ARGMIN = Fraction(
    27602892902794854989741,
    85743367783909735900000,
)
EXPECTED_SPECIAL_COST = Fraction(19049050319373, 6463801093750)
EXPECTED_FACTORIAL_COST = Fraction(1021923, 1000000)
EXPECTED_ETA = Fraction(111206677906959, 206841635000000)

EXPECTED_LIFT_GAPS = {
    (17, 11): Fraction(713749906959, 206841635000000),
    (17, 13): Fraction(31068949906959, 206841635000000),
    (17, 17): Fraction(63543061906959, 206841635000000),
    (19, 11): Fraction(25838240232221, 3929991065000000),
    (19, 13): Fraction(599214240232221, 3929991065000000),
    (19, 19): Fraction(26370825700412199, 74669830235000000),
}


def _denominators(primes: tuple[int, int, int, int] = REFERENCE_PRIMES) -> tuple[int, ...]:
    return tuple(
        prod(primes[i] for i in range(4) if Cmask & (1 << i))
        for Cmask in range(16)
    )


def _rho_numerators(z: tuple[int, ...]) -> tuple[int, ...]:
    """Return integer numerators of the 16 non-special coordinate rhos."""
    if len(z) != 15 or any(v not in (1, 2, 3, 4) for v in z):
        raise ValueError("z must contain fifteen integers in 1..4")
    D = REFERENCE_PRIMES
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
                value -= z[S - 1] * n[Cmask ^ S]
                if T == 0:
                    break
                T = (T - 1) & rest
            n[Cmask] = value
    return tuple(n)


@lru_cache(maxsize=1)
def _numerator_bounds() -> tuple[tuple[int, ...], tuple[int, ...]]:
    lows = [None] * 16
    highs = [None] * 16
    for z in product((1, 4), repeat=15):
        n = _rho_numerators(z)
        for Cmask, value in enumerate(n):
            lows[Cmask] = value if lows[Cmask] is None or value < lows[Cmask] else lows[Cmask]
            highs[Cmask] = value if highs[Cmask] is None or value > highs[Cmask] else highs[Cmask]
    return tuple(lows), tuple(highs)


def _phi_exact(Cmask: int, numerator: int) -> Fraction:
    """Minimize one distinguished-5 quadratic contribution exactly."""
    den = _denominators()
    rho = Fraction(numerator, den[Cmask])
    T = 15 ^ Cmask
    special_mask = 1 | (T << 1)
    lam = LAMBDA.get(special_mask, Fraction(0))
    nu = DIAGONAL[special_mask]
    lo = Fraction(6, 25 * den[T])
    hi = 4 * lo
    x = -(lam - rho) / (2 * nu)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return nu * x * x + (lam - rho) * x


@lru_cache(maxsize=1)
def _floor_tables():
    lows, highs = _numerator_bounds()
    den = _denominators()
    phi = []
    rho = []
    for Cmask in range(16):
        prow = []
        rrow = []
        for numerator in range(lows[Cmask], highs[Cmask] + 1):
            value = _phi_exact(Cmask, numerator)
            prow.append((value.numerator * Q) // value.denominator)
            value = Fraction(numerator, den[Cmask])
            rrow.append((value.numerator * Q) // value.denominator)
        phi.append(tuple(prow))
        rho.append(tuple(rrow))
    return tuple(phi), tuple(rho), lows


def _lookup(row: tuple[int, ...], low: int, numerator: int) -> int:
    idx = numerator - low
    if idx < 0 or idx >= len(row):
        raise AssertionError("numerator escaped endpoint-derived range")
    return row[idx]


def _factorial_penalty(z: tuple[int, ...]) -> Fraction:
    return sum(
        alpha * (z[mask - 1] - 1) + beta * comb(z[mask - 1] - 1, 2)
        for mask, alpha, beta in zip(SELECTED_SUPPORTS, ALPHA, BETA)
    )


def _pointwise_exact(z: tuple[int, ...]) -> Fraction:
    n = _rho_numerators(z)
    den = _denominators()
    return (
        Fraction(n[15], den[15])
        + sum(_phi_exact(Cmask, n[Cmask]) for Cmask in range(16))
        + _factorial_penalty(z)
    )


@lru_cache(maxsize=1)
def pointwise_certificate() -> dict:
    assert factorial_spike_cap(3, 1) == 13
    assert factorial_spike_cap(3, 2) == 5
    assert Q % COEFFICIENT_DEN == 0
    scale = Q // COEFFICIENT_DEN
    phi, rho, lows = _floor_tables()

    best = None
    best_state = None
    checked = 0
    for selected in product(range(1, 5), repeat=6):
        penalty_units = sum(
            anum * (value - 1) + bnum * comb(value - 1, 2)
            for value, anum, bnum in zip(selected, ALPHA_NUM, BETA_NUM)
        )
        for endpoints in product((1, 4), repeat=9):
            z = [0] * 15
            for mask, value in zip(SELECTED_SUPPORTS, selected):
                z[mask - 1] = value
            for mask, value in zip(UNSELECTED_SUPPORTS, endpoints):
                z[mask - 1] = value
            zt = tuple(z)
            n = _rho_numerators(zt)
            value = scale * penalty_units
            value += _lookup(rho[15], lows[15], n[15])
            for Cmask in range(16):
                value += _lookup(phi[Cmask], lows[Cmask], n[Cmask])
            checked += 1
            if best is None or value < best:
                best = value
                best_state = zt

    assert checked == EXPECTED_STATE_COUNT
    assert best == EXPECTED_FLOOR_MIN
    assert best_state == EXPECTED_ARGMIN
    assert C * Q == 321_900_000_000
    assert best - C * Q == EXPECTED_FLOOR_SLACK > 0
    exact = _pointwise_exact(EXPECTED_ARGMIN)
    assert exact == EXPECTED_EXACT_ARGMIN > C
    assert Fraction(best, Q) <= exact
    return {
        "state_count": checked,
        "floor_min_scaled": best,
        "floor_slack_scaled": best - C * Q,
        "argmin": best_state,
        "exact_argmin_value": exact,
        "verified": True,
    }


def special_global_cost() -> Fraction:
    den = _denominators()
    out = Fraction(0)
    for T in range(16):
        mask = 1 | (T << 1)
        b = Fraction(6, 25 * den[T])
        out += 27 * LAMBDA.get(mask, Fraction(0)) * b
        out += 63 * DIAGONAL[mask] * b * b
    return out


def factorial_global_cost() -> Fraction:
    return 13 * sum(ALPHA, Fraction(0)) + 5 * sum(BETA, Fraction(0))


def reference_margin() -> Fraction:
    eta = 14 * C - special_global_cost() - factorial_global_cost()
    assert special_global_cost() == EXPECTED_SPECIAL_COST
    assert factorial_global_cost() == EXPECTED_FACTORIAL_COST
    assert eta == EXPECTED_ETA > 0
    return eta


def _sigma_ratio_B(P: int, q: int) -> Fraction:
    """sigma(B)/B for B=5^2*7*11*13*P/q."""
    if P not in (17, 19) or q not in (11, 13, P):
        raise ValueError("unsupported exceptional seed")
    out = Fraction(31, 25)
    removed = False
    for r in (7, 11, 13, P):
        if r == q and not removed:
            removed = True
            continue
        out *= Fraction(r + 1, r)
    assert removed
    return out


def lift_gap(P: int, q: int) -> Fraction:
    """Reference-normalized gap eta - 40/q^2 * sigma(B)/B."""
    gap = reference_margin() - Fraction(40, q * q) * _sigma_ratio_B(P, q)
    assert gap == EXPECTED_LIFT_GAPS[(P, q)] > 0
    return gap


def exceptional_seed_numbers() -> tuple[int, ...]:
    nums = tuple(
        sorted(3**3 * 5**2 * 7 * 11 * 13 * P * q for P in (17, 19) for q in (11, 13, P))
    )
    expected = {
        family_number(primes, exponents)
        for primes, exponents in SEEDS[P322]
        if tuple(exponents) != P322
    }
    assert set(nums) == expected
    return nums


@lru_cache(maxsize=1)
def seed_audit() -> dict:
    pointwise = pointwise_certificate()
    eta = reference_margin()
    gaps = {(P, q): lift_gap(P, q) for P in (17, 19) for q in (11, 13, P)}
    nums = exceptional_seed_numbers()
    assert len(nums) == 6 and all(g > 0 for g in gaps.values())
    return {
        "pointwise": pointwise,
        "reference_eta": eta,
        "lift_gaps": gaps,
        "exceptional_seed_numbers": nums,
        "exceptional_seed_count": 6,
        "all_exceptional_seeds_noncovering": True,
    }


__all__ = [
    "C",
    "EXPECTED_ETA",
    "EXPECTED_LIFT_GAPS",
    "REFERENCE_PRIMES",
    "exceptional_seed_numbers",
    "factorial_global_cost",
    "lift_gap",
    "pointwise_certificate",
    "reference_margin",
    "seed_audit",
    "special_global_cost",
]
