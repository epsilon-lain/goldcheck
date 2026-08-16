"""Milestone 7 (K1/K2): one-coordinate star-collision lower envelope.

In the BFF product-set model, for a fixed prime coordinate ``i`` the five blocks
``B_{ij}`` (``j != i``) are subsets of the ``i``-th coordinate of measure ``z_i``
each.  Since all five live in one coordinate, they must collide; the minimum
possible pairwise collision is not ``0`` whenever ``5 z_i > 1``.

The exact relaxation is the *star* lower-envelope LP: for nonnegative pair
weights ``c_{jk}``,

    min_{y}  sum_T y_T * sum_{{j,k} subset T} c_{jk}
    s.t.     y_T >= 0,  sum_T y_T = 1,
             sum_{T containing j} y_T = z_i   (for every j != i),

where ``T`` ranges over the ``2^5 = 32`` membership patterns of the five
neighbours.  Its optimum is a certified lower bound on the aggregate weighted
pair-collision in coordinate ``i``.

The certificates are stored in ``certificates/omega6_star.json``; everything in
the trusted verification path is pure ``Fraction`` arithmetic.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def z_values() -> dict[int, Fraction]:
    """The six-prime corner parameters ``z = (1/3, 1/2, 1/4, 1/8, 1/10, 1/14)``."""
    primes = [3, 5, 7, 11, 13, 17]
    z = {1: Fraction(1, 3)}
    for i in range(2, 7):
        z[i] = Fraction(1, primes[i - 1] - 3)
    return z


def load_star_certificate() -> dict:
    path = Path(__file__).resolve().parent.parent / "certificates" / "omega6_star.json"
    return json.loads(path.read_text(encoding="utf-8"))


def verify_star(i: int, cert: dict | None = None) -> dict:
    """Independently verify the exact star certificate for coordinate ``i``."""
    cert = cert or load_star_certificate()
    z = {int(k): Fraction(v) for k, v in cert["z"].items()}
    others = [j for j in range(1, 7) if j != i]
    y = [Fraction(v) for v in cert["coords"][str(i)]["primal_y"]]
    v = [Fraction(v) for v in cert["coords"][str(i)]["dual_v"]]
    value = Fraction(cert["coords"][str(i)]["value"])

    # Primal feasibility.
    nonneg = all(a >= 0 for a in y)
    total = sum(y)
    margins = [sum(y[m] for m in range(32) if (m >> idx) & 1) for idx in range(5)]
    primal_ok = nonneg and total == 1 and all(margins[idx] == z[i] for idx in range(5))

    # Dual feasibility: v0 + sum_{j in T} v_j <= E_T for every atom T.
    dual_ok = True
    for m in range(32):
        lhs = v[0]
        for idx in range(5):
            if (m >> idx) & 1:
                lhs += v[1 + idx]
        E = Fraction(0)
        for a in range(5):
            for b in range(a + 1, 5):
                if (m >> a) & 1 and (m >> b) & 1:
                    E += z[others[a]] * z[others[b]]
        if lhs > E:
            dual_ok = False

    energy = Fraction(0)
    for m in range(32):
        E = Fraction(0)
        for a in range(5):
            for b in range(a + 1, 5):
                if (m >> a) & 1 and (m >> b) & 1:
                    E += z[others[a]] * z[others[b]]
        energy += y[m] * E
    dual_obj = v[0] + z[i] * sum(v[1:])

    return {
        "primal_ok": primal_ok,
        "dual_ok": dual_ok,
        "energy": energy,
        "dual_obj": dual_obj,
        "value": value,
        "strong_duality": energy == dual_obj == value,
    }


def star_values() -> dict[int, Fraction]:
    cert = load_star_certificate()
    return {i: Fraction(cert["coords"][str(i)]["value"]) for i in range(1, 7)}


def disjoint_pair_sum(z: dict[int, Fraction]) -> Fraction:
    """Sum of exact disjoint-pair intersection weights ``= 3 e_4(z)``.

    Each disjoint pair ``{I, J}`` has intersection ``prod_{i in I u J} z_i``; the
    ``45`` disjoint pairs are the ``3`` perfect matchings inside each of the
    ``15`` four-subsets of ``{1,...,6}``, hence the total is ``3 e_4(z)``.
    """
    zs = [z[i] for i in range(1, 7)]
    e4 = Fraction(0)
    for comb in combinations(zs, 4):
        p = Fraction(1)
        for x in comb:
            p *= x
        e4 += p
    return 3 * e4


def star_insufficient_bound() -> dict:
    """The exact Milestone-7 star-pair insufficiency certificate.

    For any coefficient certificate, each pair multiplier is ``<= 1`` (the
    two-vertex pointwise constraint), so the disjoint-pair credit is at most
    ``sum L_e = 3 e_4(z)`` and, by monotonicity of each star LP, the overlapping
    pair credit is at most ``sum_i LP_i(1)``.  Hence

        F_star* <= 3 e_4(z) + sum_i LP_i(1) = 323/4480 + 383/6720 = 347/2688,

    and therefore ``g_star = g1 - F_star* >= 5989/2688 - 347/2688 = 2821/1344 > 2``.
    """
    z = z_values()
    dsum = disjoint_pair_sum(z)
    ssum = sum(star_values().values(), Fraction(0))
    F_ub = dsum + ssum
    g1 = Fraction(5989, 2688)
    g_lb = g1 - F_ub
    return {
        "disjoint_pair_sum": dsum,
        "star_sum": ssum,
        "F_ub": F_ub,
        "g1": g1,
        "g_lb": g_lb,
        "g_lb_gt_2": g_lb > 2,
        "residual_gap_lb": g_lb - 2,
    }


__all__ = [
    "disjoint_pair_sum",
    "load_star_certificate",
    "star_insufficient_bound",
    "star_values",
    "verify_star",
    "z_values",
]
