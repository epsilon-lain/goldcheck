"""Exact solver for distinct covering systems with moduli dividing N.

The problem modelled here is: does there exist a finite family of congruence
classes ``a_d mod d`` (``d | N``, ``d > 1``, all ``d`` pairwise distinct) whose
union is all of ``Z/NZ``?  A positive integer ``N`` with such a family is a
*covering number* in the sense of McNew--Setty.  An odd covering number is
exactly what the Erdős--Selfridge problem forbids.

This module reduces the question to SAT.  For each divisor ``d > 1`` of ``N``
and each residue ``r`` in ``Z/dZ`` there is a boolean variable meaning "the
class ``r mod d`` is used".  The two constraint families are

* *distinct moduli*: for every ``d`` at most one residue is chosen;
* *covering*: every ``x`` in ``Z/NZ`` lies in at least one chosen class.

Cardinality constraints are encoded with PySAT's sequential-counter encoder,
so the CNF is fully explicit and every arithmetic value is an exact integer.
"""

from __future__ import annotations

import threading

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical153, Glucose4, Kissat404, Minisat22


def divisors(n: int) -> list[int]:
    """Sorted list of all positive divisors of ``n``."""
    if n < 1:
        raise ValueError("n must be positive")
    out: set[int] = set()
    i = 1
    while i * i <= n:
        if n % i == 0:
            out.add(i)
            out.add(n // i)
        i += 1
    return sorted(out)


def factor(n: int) -> list[tuple[int, int]]:
    """Prime factorization of ``n`` as a list of ``(prime, exponent)`` pairs."""
    if n < 1:
        raise ValueError("n must be positive")
    res: list[tuple[int, int]] = []
    m = n
    p = 2
    while p * p <= m:
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            res.append((p, e))
        p += 1 if p == 2 else 2
    if m > 1:
        res.append((m, 1))
    return res


def sigma(n: int) -> int:
    """Sum of divisors of ``n``."""
    return sum(divisors(n))


def tau(n: int) -> int:
    """Number of divisors of ``n``."""
    return len(divisors(n))


def add_at_most_k(cnf: CNF, pool: IDPool, lits: list[int], k: int) -> None:
    """Append a sequential-counter encoding of "at most ``k`` of ``lits``"."""
    if k < 0:
        raise ValueError("k must be nonnegative")
    m = len(lits)
    if k >= m:
        return
    if k == 0:
        for x in lits:
            cnf.append([-x])
        return
    card = CardEnc.atmost(list(lits), bound=k, vpool=pool, encoding=EncType.seqcounter)
    cnf.extend(card.clauses)


def add_at_most_one(cnf: CNF, pool: IDPool, lits: list[int]) -> None:
    """Append an encoding of "at most one of ``lits``"."""
    add_at_most_k(cnf, pool, lits, 1)


class CoverProblem:
    """CNF formulation of a covering/max-coverage instance for a fixed N."""

    def __init__(self, N: int) -> None:
        if N < 2:
            raise ValueError("N must be at least 2")
        self.N = N
        self.divs = [d for d in divisors(N) if d > 1]
        self.pool: IDPool = IDPool()
        self._ctr = 0
        self.var: dict[tuple[int, int], int] = {}
        for d in self.divs:
            for r in range(d):
                self.var[(d, r)] = self._fresh()
        self.cnf = CNF()

    def _fresh(self) -> int:
        self._ctr += 1
        return self.pool.id(("v", self._ctr))

    def _base_clauses(self) -> None:
        # Distinct moduli: at most one residue per divisor.
        for d in self.divs:
            add_at_most_one(self.cnf, self.pool, [self.var[(d, r)] for r in range(d)])

    def build_cover(self) -> CNF:
        """Clauses asserting a full cover of Z/NZ."""
        self._base_clauses()
        for x in range(self.N):
            self.cnf.append([self.var[(d, x % d)] for d in self.divs])
        return self.cnf

    def build_partial(self) -> tuple[CNF, list[int]]:
        """Clauses for the max-coverage problem.

        Returns the CNF together with ``covered`` literals: ``covered[y]`` can
        only be true when point ``y`` is covered by some chosen class.
        """
        self._base_clauses()
        covered = [self._fresh() for _ in range(self.N)]
        for y in range(self.N):
            clause = [-covered[y]]
            clause.extend(self.var[(d, y % d)] for d in self.divs)
            self.cnf.append(clause)
        return self.cnf, covered


def solve_cover(
    N: int, solver: str = "cadical153", timeout: float | None = None
) -> tuple[bool, list[tuple[int, int]] | None]:
    """Decide whether N is a covering number.

    Returns ``(sat, cover)`` where ``cover`` is a list of ``(modulus, residue)``
    pairs for a satisfying assignment, or ``None`` if unsatisfiable.
    """
    prob = CoverProblem(N)
    cnf = prob.build_cover()
    cls = _solver_class(solver)
    with cls(bootstrap_with=cnf, use_timer=True) as s:
        ok = _solve(s, timeout)
        if not ok:
            return False, None
        model = s.get_model()
    if model is None:
        return False, None
    chosen: list[tuple[int, int]] = []
    for (d, r), lit in prob.var.items():
        if 0 < lit <= len(model) and model[lit - 1] > 0:
            chosen.append((d, r))
    return True, sorted(chosen)


def max_coverage(
    N: int, solver: str = "cadical153", timeout: float | None = None
) -> tuple[int, int]:
    """Maximum number of points of Z/NZ coverable by distinct classes mod d|N.

    Returns ``(covered, deficiency)`` with ``deficiency = N - covered``.
    """
    lo, hi = 0, N
    best = 0
    while lo <= hi:
        k = (lo + hi) // 2
        if _covers_at_least(N, k, solver, timeout):
            best = k
            lo = k + 1
        else:
            hi = k - 1
    return best, N - best


def _covers_at_least(
    N: int, k: int, solver: str, timeout: float | None
) -> bool:
    """Decide whether at least ``k`` points can be covered."""
    prob = CoverProblem(N)
    cnf, covered = prob.build_partial()
    uncovered = [-lit for lit in covered]
    add_at_most_k(cnf, prob.pool, uncovered, N - k)
    cls = _solver_class(solver)
    with cls(bootstrap_with=cnf, use_timer=True) as s:
        return bool(_solve(s, timeout))


def deficiency(N: int, solver: str = "cadical153", timeout: float | None = None) -> int:
    """``N - r(N)``: minimum number of uncovered residues over all distinct systems."""
    _, d = max_coverage(N, solver=solver, timeout=timeout)
    return d


def _solve(s, timeout: float | None) -> bool:
    """Run ``s.solve()`` with an optional wall-clock timeout via interrupt."""
    if timeout is None:
        return bool(s.solve())
    result: list[bool] = []
    timer = threading.Timer(timeout, s.interrupt)
    timer.daemon = True
    timer.start()
    try:
        result.append(bool(s.solve()))
    finally:
        timer.cancel()
    return result[0] if result else False


def _solver_class(name: str):
    if name in ("cadical", "cadical153"):
        return Cadical153
    if name in ("glucose", "glucose4"):
        return Glucose4
    if name in ("kissat", "kissat404"):
        return Kissat404
    if name in ("minisat", "minisat22"):
        return Minisat22
    raise ValueError(f"unknown solver {name!r}")


def verify_cover(N: int, cover: list[tuple[int, int]]) -> bool:
    """Independently verify that ``cover`` is a valid distinct covering of Z/NZ."""
    if N < 2:
        return False
    moduli = [d for d, _ in cover]
    if len(moduli) != len(set(moduli)):
        return False
    covered = [False] * N
    for d, r in cover:
        if d <= 1 or N % d != 0 or not 0 <= r < d:
            return False
        for x in range(r, N, d):
            covered[x] = True
    return all(covered)


__all__ = [
    "CoverProblem",
    "add_at_most_k",
    "add_at_most_one",
    "deficiency",
    "divisors",
    "factor",
    "max_coverage",
    "sigma",
    "solve_cover",
    "tau",
    "verify_cover",
]
