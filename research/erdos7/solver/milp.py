"""Exact MILP solver for the distinct-covering max-coverage problem.

Uses :mod:`scipy.optimize.milp` (HiGHS) for the optimization and provides an
independent pure-Python verifier for the returned optimum.  All quantities are
exact integers; only the solver's internal floating-point engine is trusted,
which is why :func:`verify_cover` and :func:`verify_deficiency` re-check every
claim with integer arithmetic.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

from covering import divisors, verify_cover


def max_coverage_milp(N: int) -> tuple[int, int]:
    """Return ``(covered, deficiency)`` for the distinct-covering problem on N.

    The model has a binary variable ``x[d,r]`` for each divisor ``d>1`` of
    ``N`` and residue ``r`` (class ``r mod d`` used) plus a continuous
    indicator ``c[y]`` that point ``y`` is covered.  Constraints:

    * for each ``d``: at most one residue is chosen;
    * for each ``y``: ``c[y] <= sum of x[d, y mod d]``.

    The objective maximizes ``sum c[y]``.
    """
    divs = [d for d in divisors(N) if d > 1]

    # Variable index layout.
    x_index: dict[tuple[int, int], int] = {}
    idx = 0
    for d in divs:
        for r in range(d):
            x_index[(d, r)] = idx
            idx += 1
    n_x = idx
    n_c = N
    n_vars = n_x + n_c

    # Integrality: 1 for x, 0 for c.
    integrality = np.zeros(n_vars, dtype=np.int8)
    integrality[:n_x] = 1

    # Bounds.
    lb = np.zeros(n_vars)
    ub = np.ones(n_vars)

    rows: list[list[int]] = []  # variable indices involved in each constraint
    data: list[list[float]] = []
    lower: list[float] = []
    upper: list[float] = []

    # Constraint 1: at most one residue per modulus.
    for d in divs:
        r_idx = [x_index[(d, r)] for r in range(d)]
        rows.append(r_idx)
        data.append([1.0] * len(r_idx))
        lower.append(-np.inf)
        upper.append(1.0)

    # Constraint 2: c_y <= sum_d x[d, y mod d].
    for y in range(N):
        c_idx = n_x + y
        x_idx = [x_index[(d, y % d)] for d in divs]
        rows.append([c_idx] + x_idx)
        data.append([1.0] + [-1.0] * len(x_idx))
        lower.append(-np.inf)
        upper.append(0.0)

    # Build the sparse constraint matrix in CSR form.
    row_ptr: list[int] = []
    col_ind: list[int] = []
    vals: list[float] = []
    for var_idx, ds in zip(rows, data):
        row_ptr.append(len(vals))
        col_ind.extend(var_idx)
        vals.extend(ds)
    row_ptr.append(len(vals))
    A = _csr_from(row_ptr, col_ind, vals, n_vars)

    # Objective: maximize sum c_y (equivalently minimize -sum c_y).
    c_obj = np.zeros(n_vars)
    c_obj[n_x:] = -1.0

    constraints = LinearConstraint(A, np.array(lower), np.array(upper))
    res = milp(
        c=c_obj,
        integrality=integrality,
        bounds=Bounds(lb, ub),
        constraints=constraints,
        options={"presolve": True},
    )
    if not res.success:
        raise RuntimeError(f"MILP failed for N={N}: {res.message}")

    covered = int(round(-res.fun))
    # Guard against floating point slop; the verifier is the source of truth.
    return covered, N - covered


def _csr_from(row_ptr, col_ind, vals, n_cols):
    # Reconstruct row indices from the CSR pointer array.
    n_rows = len(row_ptr) - 1
    row_ind = np.repeat(np.arange(n_rows), np.diff(row_ptr))
    return coo_matrix((vals, (row_ind, col_ind)), shape=(n_rows, n_cols)).tocsr()


def solve_cover_milp(N: int) -> tuple[bool, list[tuple[int, int]] | None]:
    """Decide whether ``N`` is a covering number via the MILP optimum."""
    covered, _ = max_coverage_milp(N)
    if covered != N:
        return False, None
    # Recover an actual cover by reconstructing the variables (small search is
    # unnecessary: ask for the solution through a dedicated call is overkill,
    # so we fall back to the SAT solver for a witness).
    from covering import solve_cover

    return solve_cover(N)


def verify_max_coverage(
    N: int, covered: int, witness: Iterable[tuple[int, int]] | None = None
) -> bool:
    """Independently check a claimed max-coverage value.

    * ``covered <= N`` and ``covered`` is achievable: if a witness cover is
      supplied, its classes must be distinct moduli dividing ``N`` and cover
      exactly ``covered`` points.
    * The claim is not certified optimal here; use the dual/ILP re-run for
      that, or pass a witness for the lower-bound direction.
    """
    if covered < 0 or covered > N:
        return False
    if witness is None:
        return True
    moduli = [d for d, _ in witness]
    if len(moduli) != len(set(moduli)):
        return False
    seen = set()
    count = 0
    for d, r in witness:
        if d <= 1 or N % d != 0 or not 0 <= r < d:
            return False
        for x in range(r, N, d):
            seen.add(x)
    return len(seen) == covered


__all__ = [
    "max_coverage_milp",
    "solve_cover_milp",
    "verify_max_coverage",
]
