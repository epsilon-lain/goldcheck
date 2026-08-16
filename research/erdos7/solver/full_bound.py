"""Full prime-power form of McNew--Setty Lemma 4.10.

McNew--Setty equation (10) applies Lemma 4.10 to the full divisor set
``D_{>1}(n)`` and gives

    r(n)/n  <=  R(n) := sum_{empty != U subseteq supp(n)} C_|U| * prod_{i in U} x_i,

where ``n = prod p_i^{a_i}``, ``x_i = (1 - p_i^{-a_i})/(p_i-1)``, and
``C_m = sum_{t=1..m} (-1)^{t+1} S2(m,t)``.  The right-hand side factors by
prime support: for a fixed support ``U``, summing ``1/d`` over all positive
exponent choices factorises as ``prod_{i in U} (sum_{j=1}^{a_i} p_i^{-j})``.

Consequently ``delta(n) = n - r(n) >= n * (1 - R(n))``, and the right-hand side
is an exact integer (``n * R(n)`` is an integer).  This is strictly stronger
than both the square-free-only bound and the raw deficiency recurrence.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product

from certificate import complementary_bell_coeff
from covering import divisors, factor


# A five-prime support whose largest prime is at least 23 is excluded by the
# direct Lemma 4.10 bound via the coordinatewise-monotonicity corner argument
# proved in NOTES.md.  ``R(m_1,m_2,m_3,m_4,1/22) = 5263/5280`` for the corner
# ``(1/2,1/4,1/6,1/10,1/22)``, and 1 - 5263/5280 = 17/5280.
OMEGA5_LARGE_Q_THRESHOLD = 23
OMEGA5_CORNER_BOUND = Fraction(5263, 5280)
OMEGA5_CORNER_DEFICIT = Fraction(1) - OMEGA5_CORNER_BOUND  # 17/5280

# A five-prime survivor of the direct bound cannot have a prime >= 23 (see
# ``omega5_large_q_excluded``), so only these seven primes can appear in the
# smallest omega=5 survivor.
OMEGA5_SURVIVOR_POOL = (3, 5, 7, 11, 13, 17, 19)


def x_of(p: int, a: int) -> Fraction:
    """``x_i = (1 - p_i^{-a_i}) / (p_i - 1)`` as an exact rational."""
    return Fraction(p**a - 1, (p - 1) * p**a)


def support_R_from_xs(xs: list[Fraction]) -> Fraction:
    """The support form ``R = sum_U C_|U| prod_{i in U} x_i`` from raw ``x_i``."""
    k = len(xs)
    R = Fraction(0)
    for m in range(1, k + 1):
        C = complementary_bell_coeff(m)
        for subset in combinations(range(k), m):
            prod = Fraction(1)
            for i in subset:
                prod *= xs[i]
            R += C * prod
    return R


def support_R(primes: list[int], exps: list[int]) -> Fraction:
    """The prime-power support form ``R(n)`` for ``n = prod p_i^{a_i}``."""
    xs = [x_of(p, a) for p, a in zip(primes, exps)]
    return support_R_from_xs(xs)


def support_R_limit(primes: list[int]) -> Fraction:
    """``R(n)`` in the infinite-exponent limit ``x_i = 1/(p_i - 1)``."""
    return support_R_from_xs([Fraction(1, p - 1) for p in primes])


def divisor_R(n: int) -> Fraction:
    """Direct divisor-sum form of McNew--Setty equation (10).

    Independent of :func:`support_R`; used as a cross-check.
    """
    R = Fraction(0)
    for d in divisors(n):
        if d <= 1:
            continue
        omega = len(factor(d))
        R += Fraction(complementary_bell_coeff(omega), d)
    return R


def coverage_bound_from(primes: list[int], exps: list[int]) -> int:
    """Integer upper bound ``n * R(n) >= r(n)`` from exponent data."""
    n = 1
    for p, a in zip(primes, exps):
        n *= p**a
    return int(n * support_R(primes, exps))


def coverage_bound(n: int) -> int:
    """Integer upper bound ``n * R(n) >= r(n)``."""
    fs = factor(n)
    return coverage_bound_from([p for p, _ in fs], [a for _, a in fs])


def deficiency_bound(n: int) -> int:
    """Certified lower bound ``delta(n) >= n - n*R(n)``."""
    return n - coverage_bound(n)


@lru_cache(maxsize=None)
def odd_omega_limit(k: int) -> Fraction:
    """Supremum of ``R`` over odd ``n`` with ``omega(n) = k`` (infinite exponents)."""
    primes = [3, 5, 7, 11, 13, 17, 19][:k]
    xs = [Fraction(1, p - 1) for p in primes]
    R = Fraction(0)
    for m in range(1, k + 1):
        C = complementary_bell_coeff(m)
        for subset in combinations(range(k), m):
            prod = Fraction(1)
            for i in subset:
                prod *= xs[i]
            R += C * prod
    return R


def omega_le_4_excluded(n: int) -> bool:
    """Whether the full bound proves ``n`` is non-covering (odd, omega<=4)."""
    fs = factor(n)
    if len(fs) > 4 or any(p == 2 for p, _ in fs):
        raise ValueError("omega_le_4_excluded expects an odd n with omega(n) <= 4")
    return support_R([p for p, _ in fs], [a for _, a in fs]) < 1


def all_primes_condition_vec(primes: list[int], exps: list[int]) -> bool:
    """All-primes necessary condition for ``N = prod p_i^{a_i}``."""
    k = len(primes)
    for i in range(k):
        tau_other = 1
        for j in range(k):
            if j != i:
                tau_other *= exps[j] + 1
        if primes[i] > tau_other:
            return False
    return True


def sigma_from(primes: list[int], exps: list[int]) -> int:
    """``sigma(prod p_i^{a_i})`` computed multiplicatively (no factoring)."""
    s = 1
    for p, a in zip(primes, exps):
        s *= sum(p**j for j in range(a + 1))
    return s


def n_from(primes: list[int], exps: list[int]) -> int:
    n = 1
    for p, a in zip(primes, exps):
        n *= p**a
    return n


def smallest_omega5_survivor(max_exponent: int = 8) -> tuple[int, dict[int, int], Fraction]:
    """Smallest odd ``omega=5`` primitive candidate not excluded by the direct bound.

    The search is *globally* exact for the direct bound, by two proved facts
    (see NOTES.md):

    * any five-prime number whose largest prime is at least 23 has ``R < 1``
      (``omega5_large_q_excluded``), so only supports drawn from
      ``OMEGA5_SURVIVOR_POOL`` can survive; and
    * for each such support we enumerate every exponent vector whose product is
      strictly smaller than the running best survivor, so no smaller survivor is
      missed.

    A vector survives only if it passes the all-primes primitive necessary
    condition, abundance (``sigma(n) > 2n``), and ``R(n) >= 1`` (the direct
    bound does not certify positive deficiency).  ``max_exponent`` is a seeding
    bound used to obtain an initial finite best value on ``{3,5,7,11,13}``; the
    pruning pass below does not depend on it.
    """
    seed_primes = [3, 5, 7, 11, 13]
    best: tuple[int, dict[int, int], Fraction] | None = None
    for exps in product(range(1, max_exponent + 1), repeat=5):
        n = n_from(seed_primes, list(exps))
        if best is not None and n >= best[0]:
            continue
        if not _omega5_survivor(seed_primes, list(exps), n):
            continue
        best = (n, dict(zip(seed_primes, exps)), support_R(seed_primes, list(exps)))
    assert best is not None

    for primes_tuple in combinations(OMEGA5_SURVIVOR_POOL, 5):
        primes = list(primes_tuple)
        if tuple(primes) == tuple(seed_primes):
            continue
        for exps in _enumerate_exps_under(primes, best[0]):
            n = n_from(primes, exps)
            if not _omega5_survivor(primes, exps, n):
                continue
            best = (n, dict(zip(primes, exps)), support_R(primes, exps))
    return best


def _omega5_survivor(primes: list[int], exps: list[int], n: int) -> bool:
    """Whether a five-prime exponent vector is a surviving candidate."""
    if not all_primes_condition_vec(primes, exps):
        return False
    if sigma_from(primes, exps) <= 2 * n:
        return False
    if support_R(primes, exps) < 1:
        return False
    return True


def _enumerate_exps_under(primes: list[int], cap: int):
    """Yield all exponent vectors (>=1) with ``prod p_i^{a_i} < cap``."""
    exps = [1] * len(primes)
    yield from _dfs_exps(primes, 0, 1, cap, exps)


def _dfs_exps(primes: list[int], idx: int, cur: int, cap: int, exps: list[int]):
    if idx == len(primes):
        if cur < cap:
            yield list(exps)
        return
    p = primes[idx]
    other_min = 1
    for j in range(idx + 1, len(primes)):
        other_min *= primes[j]
    e = 1
    while cur * (p**e) * other_min < cap:
        exps[idx] = e
        yield from _dfs_exps(primes, idx + 1, cur * (p**e), cap, exps)
        e += 1
    exps[idx] = 1


def omega5_large_q_excluded(primes: list[int], exps: list[int]) -> tuple[bool, int]:
    """Uniform corner bound excluding five-prime ``n`` with largest prime >= 23.

    Returns ``(True, lower_bound)`` when ``max(primes) >= 23``, in which case
    ``delta(n) >= ceil(n * 17/5280)`` (so ``n`` is not a covering number).  The
    proof is the coordinatewise-monotonicity corner argument in NOTES.md.
    """
    if len(primes) != 5 or max(primes) < OMEGA5_LARGE_Q_THRESHOLD:
        return False, 0
    n = n_from(primes, exps)
    # delta(n) >= n*(1 - R(n)) >= n*17/5280; ceil it to an integer.
    num = OMEGA5_CORNER_DEFICIT.numerator
    den = OMEGA5_CORNER_DEFICIT.denominator
    return True, (n * num + den - 1) // den


def omega5_support_excluded(primes: list[int]) -> bool:
    """Whether every exponent vector on a five-prime support has ``R < 1``.

    ``R`` is coordinatewise nondecreasing in each ``x_i`` (NOTES.md), so its
    maximum over exponents is ``support_R_limit(primes)``.
    """
    assert len(primes) == 5 and all(p % 2 == 1 for p in primes)
    return support_R_limit(primes) < 1


__all__ = [
    "OMEGA5_CORNER_BOUND",
    "OMEGA5_CORNER_DEFICIT",
    "OMEGA5_LARGE_Q_THRESHOLD",
    "OMEGA5_SURVIVOR_POOL",
    "all_primes_condition_vec",
    "coverage_bound",
    "coverage_bound_from",
    "deficiency_bound",
    "divisor_R",
    "n_from",
    "odd_omega_limit",
    "omega_le_4_excluded",
    "omega5_large_q_excluded",
    "omega5_support_excluded",
    "sigma_from",
    "smallest_omega5_survivor",
    "support_R",
    "support_R_from_xs",
    "support_R_limit",
    "x_of",
]
