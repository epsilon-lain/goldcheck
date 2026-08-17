"""Milestone 9 (M9.1): exact analytic decoupling bound for the full K3 model.

The K3 relaxation prices every star family (all blocks sharing one prime
coordinate ``i``) through the same 32-atom distribution ``y_{i,T}``.  This
module records the exact local star credits and the resulting *analytic
decoupling bound* on the six-prime corner correction:

    F_K3 <= (disjoint-pair credit) + (perfect-matching credit)
             + sum_i LC_i
          <= 323/4480 + 1/896 + 19111/592620
           = 249997/2370480.

Hence ``g_K3 = g1 - F_K3 >= 5989/2688 - 249997/2370480 = 13417473/6321280 > 2``,
so the complete one-coordinate star-atom relaxation is certified insufficient.

The local star credits are certified by exact primal/dual pairs stored in
``certificates/omega6_k3_atom.json``; the verifier is pure ``Fraction``.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def z_values() -> dict[int, Fraction]:
    primes = [3, 5, 7, 11, 13, 17]
    z = {1: Fraction(1, 3)}
    for i in range(2, 7):
        z[i] = Fraction(1, primes[i - 1] - 3)
    return z


def load_k3_certificate() -> dict:
    path = Path(__file__).resolve().parent.parent / "certificates" / "omega6_k3_atom.json"
    return json.loads(path.read_text(encoding="utf-8"))


def verify_local(i: int, cert: dict | None = None) -> dict:
    """Verify the exact local K3 star-credit LP for coordinate ``i``."""
    cert = cert or load_k3_certificate()
    z = {int(k): Fraction(v) for k, v in cert["z"].items()}
    others = [j for j in range(1, 7) if j != i]
    fams = [S for r in range(2, 6) for S in combinations(range(5), r)]
    pS = {}
    for S in fams:
        p = Fraction(1)
        for j in S:
            p *= z[others[j]]
        pS[S] = p

    beta = [Fraction(v) for v in cert["coords"][str(i)]["beta"]]
    v = [Fraction(v) for v in cert["coords"][str(i)]["v"]]
    dual_y = [Fraction(v) for v in cert["coords"][str(i)]["dual_y"]]
    value = Fraction(cert["coords"][str(i)]["value"])

    # Primal feasibility: atom-dual constraints (T) and pointwise (S').
    atom_ok = True
    for T in range(32):
        lhs = v[0]
        for j in range(5):
            if (T >> j) & 1:
                lhs += v[1 + j]
        for idx, S in enumerate(fams):
            if all((T >> j) & 1 for j in S):
                lhs -= beta[idx] * pS[S]
        if lhs > 0:
            atom_ok = False
    pointwise_ok = True
    for mask in range(1, 32):
        s = Fraction(0)
        for idx, S in enumerate(fams):
            if all((mask >> j) & 1 for j in S):
                s += beta[idx]
        if s > mask.bit_count() - 1:
            pointwise_ok = False
    nonneg = all(b >= 0 for b in beta)
    primal_obj = v[0] + z[i] * sum(v[1:])

    # Dual feasibility (dual of the min form), objective = -value.
    dual_ok = all(y <= 0 for y in dual_y)
    for idx, S in enumerate(fams):
        lhs = Fraction(0)
        for T in range(32):
            if all((T >> j) & 1 for j in S):
                lhs += (-pS[S]) * dual_y[T]
        for mask in range(1, 32):
            if all((mask >> j) & 1 for j in S):
                lhs += dual_y[32 + (mask - 1)]
        if lhs > 0:
            dual_ok = False
    for s in range(6):
        if s == 0:
            lhs = sum(dual_y[T] for T in range(32))
        else:
            j = s - 1
            lhs = sum(dual_y[T] for T in range(32) if (T >> j) & 1)
        target = Fraction(-1) if s == 0 else -z[i]
        if lhs != target:
            dual_ok = False
    dual_obj = sum(
        Fraction(mask.bit_count() - 1) * dual_y[32 + (mask - 1)]
        for mask in range(1, 32)
    )

    return {
        "primal_feasible": atom_ok and pointwise_ok and nonneg,
        "primal_obj": primal_obj,
        "dual_feasible": dual_ok,
        "dual_obj": dual_obj,
        "value": value,
        "strong_duality": primal_obj == value and dual_obj == -value,
    }


def local_credits() -> dict[int, Fraction]:
    cert = load_k3_certificate()
    return {i: Fraction(cert["coords"][str(i)]["value"]) for i in range(1, 7)}


def disjoint_pair_sum(z: dict[int, Fraction]) -> Fraction:
    zs = [z[i] for i in range(1, 7)]
    e4 = Fraction(0)
    for c in combinations(zs, 4):
        p = Fraction(1)
        for x in c:
            p *= x
        e4 += p
    return 3 * e4


def k3_insufficient_bound() -> dict:
    """The exact analytic decoupling bound and the resulting ``g`` lower bound."""
    z = z_values()
    disj_pairs = disjoint_pair_sum(z)
    prod_all = Fraction(1)
    for i in range(1, 7):
        prod_all *= z[i]
    perfect_matchings = 15 * 2 * prod_all
    star_sum = sum(local_credits().values(), Fraction(0))
    F_ub = disj_pairs + perfect_matchings + star_sum
    g1 = Fraction(5989, 2688)
    g_lb = g1 - F_ub
    return {
        "disjoint_pairs": disj_pairs,
        "perfect_matchings": perfect_matchings,
        "star_sum": star_sum,
        "F_K3_ub": F_ub,
        "g1": g1,
        "g_K3_lb": g_lb,
        "g_gt_2": g_lb > 2,
        "residual_gap_lb": g_lb - 2,
    }


__all__ = [
    "disjoint_pair_sum",
    "k3_insufficient_bound",
    "load_k3_certificate",
    "local_credits",
    "verify_local",
    "z_values",
]
