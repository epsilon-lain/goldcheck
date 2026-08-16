"""Symbolic exponent-cone machinery for infinite excluded families.

Everything is exact integer arithmetic over a single free prime ``q``.  A lower
bound for a deficiency is represented as an affine form

    delta(N(q)) >= const + coeff * q

where ``N(q)`` has the fixed primes at prescribed exponents and one further
prime ``q`` at exponent 1.  The two ingredients are

* the square-free CRT/Hall bound (McNew--Setty Lemma 4.10) evaluated
  symbolically on a square-free kernel ``(prod fixed primes) * q``; and
* the deficiency recurrence ``delta(p^{a+1} M) >= p * delta(p^a M) - sigma(M)``,
  applied one prime-power step at a time.

The headline tool is :func:`power_lift_criterion`: if at a state the bound
satisfies ``(p-1) * delta(pM) >= sigma(M)`` uniformly in ``q >= q_min``, then
``p^a M`` is not a covering number for every ``a >= 1`` (proved in ``NOTES.md``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations

from certificate import complementary_bell_coeff
from covering import sigma


@dataclass(frozen=True)
class Lin:
    """``const + coeff * q``."""

    const: int
    coeff: int

    def __add__(self, other: "Lin") -> "Lin":
        return Lin(self.const + other.const, self.coeff + other.coeff)

    def __sub__(self, other: "Lin") -> "Lin":
        return Lin(self.const - other.const, self.coeff - other.coeff)

    def __mul__(self, k: int) -> "Lin":
        return Lin(self.const * k, self.coeff * k)

    __rmul__ = __mul__

    def eval(self, q: int) -> int:
        return self.const + self.coeff * q


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def smallest_odd_prime_gt(x: int) -> int:
    """Smallest odd prime strictly greater than ``x``."""
    y = x + 1
    while True:
        if is_prime(y) and y % 2 == 1:
            return y
        y += 1


def inclusion_exclusion_coverage_of_primes(primes: list[int]) -> int:
    """McNew--Setty Lemma 4.10 coverage bound for the square-free ``prod primes``."""
    k = len(primes)
    total = 0
    for size in range(1, k + 1):
        coeff = complementary_bell_coeff(size)
        for subset in combinations(range(k), size):
            outside = 1
            for i in range(k):
                if i not in subset:
                    outside *= primes[i]
            total += coeff * outside
    return total


def kernel_deficiency_bound(fixed_primes: list[int]) -> tuple[Lin, Lin]:
    """Symbolic square-free bound for ``N(q) = (prod fixed primes) * q``.

    Returns ``(coverage, delta)`` where both are affine in ``q`` and
    ``delta = N(q) - coverage`` (a lower bound on ``delta(N(q))``).

    Writing ``S = fixed_primes``:

        coverage(q) = q * F(S) + G(S)
        F(S) = inclusion--exclusion coverage bound of ``prod S``
        G(S) = sum_{U subseteq S} C_{|U|+1} * prod_{i in S\\U} p_i
    """
    P = 1
    for p in fixed_primes:
        P *= p
    F = inclusion_exclusion_coverage_of_primes(fixed_primes)
    k = len(fixed_primes)
    G = 0
    for size in range(0, k + 1):
        coeff = complementary_bell_coeff(size + 1)
        for subset in combinations(range(k), size):
            outside = 1
            for i in range(k):
                if i not in subset:
                    outside *= fixed_primes[i]
            G += coeff * outside
    coverage = Lin(G, F)
    delta = Lin(-G, P - F)
    return coverage, delta


def sigma_fixed(primes: list[int], exps: dict[int, int]) -> int:
    """``sigma(prod p^e)`` for the fixed primes only (no free ``q``)."""
    n = 1
    for p in primes:
        n *= p ** exps[p]
    return sigma(n)


def lift(delta: Lin, p: int, cofactor_sigma: int) -> Lin:
    """One recurrence step: ``delta(p^{a+1}M) >= p*delta(p^aM) - sigma(M)``.

    Here ``M = cofactor * q``, so ``sigma(M) = cofactor_sigma * (q + 1)``.
    """
    sigma_M = Lin(cofactor_sigma, cofactor_sigma)  # C*q + C = C*(q+1)
    return p * delta - sigma_M


def power_lift_criterion(
    delta_pM: Lin, p: int, cofactor_sigma: int, q_min: int
) -> tuple[bool, int | None, Lin]:
    """Test ``(p-1) * delta(pM) >= sigma(M)`` uniformly for ``q >= q_min``.

    Returns ``(ok, threshold, diff)`` where ``diff = (p-1)*delta_pM - sigma(M)``
    and ``threshold`` is the smallest integer ``q >= q_min`` for which ``diff >= 0``
    (``None`` when the inequality fails for arbitrarily large ``q``).
    """
    sigma_M = Lin(cofactor_sigma, cofactor_sigma)
    diff = (p - 1) * delta_pM - sigma_M
    if diff.coeff > 0:
        if diff.const >= 0:
            return True, q_min, diff
        threshold = -(diff.const // diff.coeff)  # ceil(-const/coeff), const<0
        threshold = max(q_min, threshold)
        return True, threshold, diff
    if diff.coeff == 0:
        return (diff.const >= 0, q_min if diff.const >= 0 else None, diff)
    return False, None, diff


@dataclass
class InfiniteFamily:
    """An infinite family of non-covering numbers of the shape ``(kernel) * q``.

    ``free`` is a single prime whose exponent is allowed to be arbitrary (>=1);
    the remaining fixed primes are held at ``exps``.  The family holds for every
    odd prime ``q >= q_min``.
    """

    fixed_primes: tuple[int, ...]
    exps: dict[int, int]
    free: int
    q_min: int
    derivation: list[str] = field(default_factory=list)


@dataclass
class MineResult:
    base_derivation: list[str]
    families: list[InfiniteFamily]
    fixed_exclusions: list[tuple[dict[int, int], int]]


def mine_families(
    fixed_primes: list[int],
    max_exponent: int = 4,
) -> MineResult:
    """Search exponent-raising orders and collect proved infinite families.

    The search is a BFS over exponent vectors for ``fixed_primes`` (each entry in
    ``1..max_exponent``).  For every state we keep an affine lower bound on the
    deficiency; a prime at exponent 1 is turned into a free exponent whenever the
    power-lifting criterion holds uniformly in ``q >= q_min``.
    """
    q_min = smallest_odd_prime_gt(max(fixed_primes))
    base_coverage, base_delta = kernel_deficiency_bound(fixed_primes)
    base_text = (
        f"kernel {''.join(str(p) for p in fixed_primes)}*q: "
        f"coverage <= {base_coverage.coeff}q + {base_coverage.const}; "
        f"delta >= {base_delta.coeff}q + {base_delta.const}  [McNew-Setty Lemma 4.10]"
    )

    start = tuple(1 for _ in fixed_primes)
    memo: dict[tuple[int, ...], Lin] = {start: base_delta}
    queue = [start]
    families: list[InfiniteFamily] = []
    fixed: list[tuple[dict[int, int], int]] = []
    seen: set[tuple[tuple[int, ...], int]] = set()

    while queue:
        exps_tuple = queue.pop(0)
        exps = {p: e for p, e in zip(fixed_primes, exps_tuple)}
        delta = memo[exps_tuple]

        # Finite exclusion: bound positive for all q >= q_min.
        if delta.coeff >= 0 and delta.const + delta.coeff * q_min >= 1:
            fixed.append((dict(exps), q_min))

        # Free (unbounded) exponent in a prime currently at exponent 1.
        for idx, p in enumerate(fixed_primes):
            if exps[p] != 1:
                continue
            cofactor = [r for j, r in enumerate(fixed_primes) if j != idx]
            c = sigma_fixed(cofactor, {r: exps[r] for r in cofactor})
            ok, threshold, diff = power_lift_criterion(delta, p, c, q_min)
            if ok and threshold is not None and (exps_tuple, p) not in seen:
                seen.add((exps_tuple, p))
                derivation = [
                    base_text,
                    f"state exponents: { {r: exps[r] for r in fixed_primes} } -> delta >= "
                    f"{delta.coeff}q + {delta.const}",
                    f"p = {p}: cofactor sigma = {c}(q+1); "
                    f"(p-1)*delta - sigma(M) = {diff.coeff}q + {diff.const} >= 0 for q >= {threshold}",
                    f"power-lifting criterion => {p}^a * (rest)^(fixed) * q is not a covering "
                    f"number for all a >= 1, q >= {threshold}",
                ]
                families.append(
                    InfiniteFamily(
                        fixed_primes=tuple(fixed_primes),
                        exps=dict(exps),
                        free=p,
                        q_min=threshold,
                        derivation=derivation,
                    )
                )

        # Raise one fixed exponent and enqueue the child state.
        for idx, p in enumerate(fixed_primes):
            if exps_tuple[idx] >= max_exponent:
                continue
            child = list(exps_tuple)
            child[idx] += 1
            child_t = tuple(child)
            if child_t in memo:
                continue
            cofactor = [r for j, r in enumerate(fixed_primes) if j != idx]
            c = sigma_fixed(cofactor, {r: exps[r] for r in cofactor})
            memo[child_t] = lift(delta, p, c)
            queue.append(child_t)

    return MineResult(
        base_derivation=[base_text],
        families=families,
        fixed_exclusions=fixed,
    )


def all_primes_condition(primes: list[int], exps: dict[int, int]) -> bool:
    """Necessary primitive-covering condition for ``N = prod p_i^{a_i}``.

    Returns True iff ``p_i <= tau(N / p_i^{a_i})`` for every fixed prime.
    """
    for i, p in enumerate(primes):
        tau_other = 1
        for j, r in enumerate(primes):
            if j != i:
                tau_other *= exps[r] + 1
        if p > tau_other:
            return False
    return True


@lru_cache(maxsize=None)
def delta_lower_fixed(primes: tuple[int, ...], exps: tuple[int, ...]) -> int:
    """Certified lower bound for ``delta(prod p_i^{a_i})`` from exponent data.

    Mirrors ``certificate.best_chain`` but works directly on prime/exponent
    vectors, so it never has to factor a huge integer.
    """
    if all(e == 1 for e in exps) and all(p % 2 == 1 for p in primes):
        N = 1
        for p in primes:
            N *= p
        return N - inclusion_exclusion_coverage_of_primes(list(primes))

    best = 0
    for idx, p in enumerate(primes):
        if exps[idx] == 0:
            continue
        sub_exps = list(exps)
        sub_exps[idx] -= 1
        sub = delta_lower_fixed(primes, tuple(sub_exps))
        M_sigma = 1
        for j, r in enumerate(primes):
            if j != idx:
                M_sigma *= sigma(r ** exps[j])
        cand = p * sub - M_sigma
        if cand > best:
            best = cand
    return max(0, best)


def surviving_candidates(
    primes: list[int],
    max_exponent: int,
) -> list[tuple[int, dict[int, int]]]:
    """Enumerate primitive-candidate patterns not killed by the *scalar* bounds.

    A pattern survives if (a) the all-primes necessary condition holds and
    (b) the chained recurrence lower bound ``delta_lower_fixed`` is 0 (so the
    scalar recurrence + square-free Lemma 4.10 bound does not prove the number
    is non-covering).

    This is the Milestone 2 scalar frontier only.  The full prime-power form of
    Lemma 4.10 (``full_bound.py``) is strictly stronger and supersedes it; use
    ``full_bound.smallest_omega5_survivor`` for the corrected frontier.
    """
    survivors: list[tuple[int, dict[int, int]]] = []
    def rec(idx: int, exps: dict[int, int]) -> None:
        if idx == len(primes):
            N = 1
            for p in primes:
                N *= p ** exps[p]
            exps_tuple = tuple(exps[p] for p in primes)
            if all_primes_condition(primes, exps) and delta_lower_fixed(
                tuple(primes), exps_tuple
            ) == 0:
                survivors.append((N, dict(exps)))
            return
        p = primes[idx]
        for e in range(1, max_exponent + 1):
            exps[p] = e
            rec(idx + 1, exps)

    rec(0, {})
    survivors.sort()
    return survivors


__all__ = [
    "InfiniteFamily",
    "Lin",
    "MineResult",
    "all_primes_condition",
    "inclusion_exclusion_coverage_of_primes",
    "is_prime",
    "kernel_deficiency_bound",
    "lift",
    "delta_lower_fixed",
    "mine_families",
    "power_lift_criterion",
    "sigma_fixed",
    "smallest_odd_prime_gt",
    "surviving_candidates",
]
