"""M27: scale one exact M25-style certificate across nine M26 (4,4,1,1,1,1) seeds.

Reference post-3 charge vector:
    (156/625, 1/7, 1/11, 1/13, 1/19).

The same nonnegative coefficients used by M25 give a positive exact
second-moment Clique-Shearer margin at this reference point.  If an actual
charge vector x is coordinatewise <= the reference vector xbar, rescale every
support charge by

    qbar_S = (bbar_S / b_S) q_S.

Then qbar dominates q pointwise, lies in the reference factor-5 box, and the
M15 first/pair moment budgets scale exactly from (81,197) to the reference
baselines.  Thus one exact reference certificate covers every coordinatewise
smaller baseline.

This eliminates 9 of the 11 M26 seeds for profile (4,4,1,1,1,1).  The two
remaining seeds are

    3^4*5^4*7*11*13*17 = 861485625,
    3^4*5*7^4*11*13*17 = 2363916555.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction

from m14_clique_shearer import J_MASK, coordinate_rhos
from m25_cross_support_seed import CROSS, DIAGONAL, LAMBDA

NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
FIVE_MASKS = tuple(1 | T for T in J_SUBSETS)

REFERENCE_COORDS = (
    Fraction(156, 625),
    Fraction(1, 7),
    Fraction(1, 11),
    Fraction(1, 13),
    Fraction(1, 19),
)

EXPECTED_C = Fraction(
    46195504828341741529478638060857243,
    113607824903921989436397505904000000,
)
EXPECTED_MARGIN = Fraction(
    41149879073842994613795978360877402927,
    355024452824756216988742205950000000000,
)
EXPECTED_PROPER_NON5_MIN = Fraction(1, 91)
EXPECTED_FULL_NON5_MIN = Fraction(-236, 19019)
EXPECTED_COMPLETION_MAX = Fraction(-118016, 11886875)

CANONICAL_PRIMES = (19, 23, 29, 31, 37, 41, 43)
DOMINATED_SIMPLE_TUPLES = tuple(
    [(7, 11, 13, p) for p in CANONICAL_PRIMES]
    + [(7, 11, 17, 19), (7, 11, 17, 23)]
)
REMAINING_SEEDS = (
    3**4 * 5**4 * 7 * 11 * 13 * 17,
    3**4 * 5 * 7**4 * 11 * 13 * 17,
)


def support_baseline(coords: tuple[Fraction, ...], mask: int) -> Fraction:
    if len(coords) != 5 or not 1 <= mask < 32:
        raise ValueError("need five coordinates and a nonempty support mask")
    out = Fraction(1)
    for i, x in enumerate(coords):
        if mask & (1 << i):
            out *= x
    return out


def _quadratic_min(linear: Fraction, quadratic: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    if quadratic <= 0:
        raise ValueError("M27 uses strictly positive diagonal coefficients")
    x = -linear / (2 * quadratic)
    if x < lo:
        x = lo
    elif x > hi:
        x = hi
    return linear * x + quadratic * x * x


@lru_cache(maxsize=None)
def reference_certificate() -> dict:
    """Exact 2^15 verification at REFERENCE_COORDS."""
    b = {m: support_baseline(REFERENCE_COORDS, m) for m in range(1, 32)}
    best = None
    proper_non5_min = None
    full_non5_min = None
    completion_max = None

    for bits in range(1 << len(NON5_MASKS)):
        q0 = {
            m: b[m] * (5 if bits & (1 << i) else 1)
            for i, m in enumerate(NON5_MASKS)
        }
        rho = coordinate_rhos(q0, J_MASK)

        for Cmask, value in rho.items():
            if Cmask == J_MASK:
                if full_non5_min is None or value < full_non5_min:
                    full_non5_min = value
            elif proper_non5_min is None or value < proper_non5_min:
                proper_non5_min = value

        alpha = 5 * b[1] - 1
        completion = -alpha * rho[J_MASK]
        completion -= sum(
            b[1 | T] * rho[J_MASK ^ T]
            for T in J_SUBSETS
            if T
        )
        if completion_max is None or completion > completion_max:
            completion_max = completion

        value = rho[J_MASK]
        value += sum(LAMBDA.get(m, Fraction(0)) * q0[m] for m in NON5_MASKS)
        value += sum(mu * q0[s] * q0[t] for (s, t), mu in CROSS.items())

        for T in J_SUBSETS:
            m = 1 | T
            linear = LAMBDA.get(m, Fraction(0)) - rho[J_MASK ^ T]
            value += _quadratic_min(linear, DIAGONAL[m], b[m], 5 * b[m])

        if best is None or value < best:
            best = value

    assert best is not None
    assert proper_non5_min is not None
    assert full_non5_min is not None
    assert completion_max is not None

    linear_cost = 81 * sum(LAMBDA.get(m, Fraction(0)) * b[m] for m in range(1, 32))
    diagonal_cost = 197 * sum(DIAGONAL[m] * b[m] * b[m] for m in FIVE_MASKS)
    cross_cost = 197 * sum(mu * b[s] * b[t] for (s, t), mu in CROSS.items())
    margin = 41 * best - linear_cost - diagonal_cost - cross_cost

    assert best == EXPECTED_C
    assert margin == EXPECTED_MARGIN > 0
    assert proper_non5_min == EXPECTED_PROPER_NON5_MIN > 0
    assert full_non5_min == EXPECTED_FULL_NON5_MIN
    assert completion_max == EXPECTED_COMPLETION_MAX < 0

    return {
        "C": best,
        "summed_margin": margin,
        "proper_non5_min": proper_non5_min,
        "full_non5_min": full_non5_min,
        "completion_upper_max": completion_max,
        "verified": True,
    }


def coordinatewise_scaled(actual: tuple[Fraction, ...]) -> bool:
    """Check whether actual baseline coordinates are dominated by the reference."""
    if len(actual) != 5:
        raise ValueError("need five post-stage coordinates")
    return all(x <= y for x, y in zip(actual, REFERENCE_COORDS))


def scaling_factors(actual: tuple[Fraction, ...]) -> dict[int, Fraction]:
    """Return bbar_S/b_S for the supportwise rescaling q -> qbar."""
    if not coordinatewise_scaled(actual):
        raise ValueError("actual coordinates are not reference-dominated")
    out = {}
    for m in range(1, 32):
        b = support_baseline(actual, m)
        bbar = support_baseline(REFERENCE_COORDS, m)
        out[m] = bbar / b
        assert out[m] >= 1
    return out


def simple_tuple_coords(simple_primes: tuple[int, int, int, int]) -> tuple[Fraction, ...]:
    return (Fraction(156, 625),) + tuple(Fraction(1, p) for p in simple_primes)


def dominated_seed_audit() -> dict:
    cert = reference_certificate()
    for simple in DOMINATED_SIMPLE_TUPLES:
        actual = simple_tuple_coords(simple)
        assert coordinatewise_scaled(actual)
        factors = scaling_factors(actual)
        # These identities are the reason the first and pair budgets transport
        # exactly: gamma_S*(81 b_S)=81 bbar_S and
        # gamma_S gamma_T*(197 b_S b_T)=197 bbar_S bbar_T.
        for s in range(1, 32):
            bs = support_baseline(actual, s)
            bbs = support_baseline(REFERENCE_COORDS, s)
            assert factors[s] * bs == bbs
        for s, t in ((1, 2), (3, 12), (14, 17), (30, 31)):
            bs = support_baseline(actual, s)
            bt = support_baseline(actual, t)
            bbs = support_baseline(REFERENCE_COORDS, s)
            bbt = support_baseline(REFERENCE_COORDS, t)
            assert factors[s] * factors[t] * bs * bt == bbs * bbt

    assert len(DOMINATED_SIMPLE_TUPLES) == 9
    assert REMAINING_SEEDS == (861485625, 2363916555)
    return {
        "reference_margin": cert["summed_margin"],
        "scaled_seed_count": len(DOMINATED_SIMPLE_TUPLES),
        "remaining_seeds": REMAINING_SEEDS,
        "verified": True,
    }


__all__ = [
    "DOMINATED_SIMPLE_TUPLES",
    "EXPECTED_MARGIN",
    "REFERENCE_COORDS",
    "REMAINING_SEEDS",
    "coordinatewise_scaled",
    "dominated_seed_audit",
    "reference_certificate",
    "scaling_factors",
    "simple_tuple_coords",
    "support_baseline",
]
