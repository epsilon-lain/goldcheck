"""Milestone 14: exact five-prime Clique-Shearer seed certificate.

This module verifies a finite rational certificate for

    N* = 3^3 * 5^2 * 7 * 11 * 13 * 17 = 11486475.

It does not use a numerical optimizer.  The only exhaustive step is a
2^15 enumeration of the endpoint box for the supports not containing 5.

Mathematical outline
--------------------
After saturating a hypothetical distinct divisor-modulus cover (add an
arbitrary class for every missing divisor d>1), take any 14 fibers modulo
27 that survive the pure moduli 3,9,27.  For each non-empty square-free
support S of the five primes 5,7,11,13,17, group the induced classes in a
fiber according to support and upper-bound its probability by q_S.

If
    b_S = product_{p in S} x_p,
    x_5 = 1/5+1/25 = 6/25,
    x_p = 1/p for p=7,11,13,17,
then b_S <= q_S <= 4 b_S and across any 14 selected fibers
    sum_r q_S(r) <= 27 b_S.

For the support-intersection dependency graph, rho(q) denotes the
independent-set (Clique-Shearer) polynomial.  The 15 events not containing
5 lie in the Clique-Shearer region throughout the box.  A relative
Clique-Shearer bound for those events, followed by a union bound over the
16 events containing 5, shows that rho(q)>0 leaves a point uncovered.

The affine certificate checked here is
    rho(q) >= C - sum_S LAMBDA_S q_S
for every q in the box, with C=8134/12155.  Summing over any 14 surviving
fibers yields
    sum_r rho(q(r)) >= 86563/425425 > 0,
so at least one fiber is not covered.

The event-conditioning argument itself is documented in the certificate note;
this file checks the exact finite arithmetic behind the certificate.
"""

from __future__ import annotations

from fractions import Fraction

PRIMES = (5, 7, 11, 13, 17)
BASE = (
    Fraction(6, 25),
    Fraction(1, 7),
    Fraction(1, 11),
    Fraction(1, 13),
    Fraction(1, 17),
)
J_MASK = 0b11110  # coordinates 7,11,13,17; bit 0 is prime 5

C = Fraction(8134, 12155)

LAMBDA = {
    1: Fraction(1697, 3094),
    2: Fraction(4734, 12155),
    3: Fraction(171, 221),
    4: Fraction(10813, 38675),
    5: Fraction(1117, 1547),
    6: Fraction(2789, 5525),
    7: Fraction(191, 221),
    8: Fraction(1161, 4675),
    9: Fraction(750, 1309),
    10: Fraction(2307, 4675),
    11: Fraction(159, 187),
    12: Fraction(79, 175),
    13: Fraction(95, 119),
    14: Fraction(298, 425),
    15: Fraction(16, 17),
    16: Fraction(5347, 25025),
    17: Fraction(514, 1001),
    18: Fraction(1571, 3575),
    19: Fraction(119, 143),
    20: Fraction(911, 2275),
    21: Fraction(71, 91),
    22: Fraction(222, 325),
    23: Fraction(12, 13),
    24: Fraction(139, 385),
    25: Fraction(59, 77),
    26: Fraction(184, 275),
    27: Fraction(10, 11),
    28: Fraction(108, 175),
    29: Fraction(6, 7),
    30: Fraction(19, 25),
    31: Fraction(1, 1),
}


def baseline(mask: int) -> Fraction:
    """b_S for a nonempty five-prime support encoded by ``mask``."""
    if not 1 <= mask < 32:
        raise ValueError("support mask must be in 1..31")
    out = Fraction(1)
    for i, x in enumerate(BASE):
        if mask & (1 << i):
            out *= x
    return out


def coordinate_rhos(q: dict[int, Fraction], coordinate_mask: int = J_MASK) -> dict[int, Fraction]:
    """Return rho_C(q) for every C subset of ``coordinate_mask``.

    The recurrence chooses the least coordinate i in C.  An independent
    support family either uses no event containing i, or exactly one support
    S containing i and then an independent family on C\\S:

        rho_C = rho_{C\\{i}} - sum_{i in S subset C} q_S rho_{C\\S}.
    """
    if coordinate_mask & ~31:
        raise ValueError("coordinate mask uses an unknown prime")
    rho = {0: Fraction(1)}
    for size in range(1, coordinate_mask.bit_count() + 1):
        for Cmask in range(32):
            if Cmask & ~coordinate_mask or Cmask.bit_count() != size:
                continue
            pivot = Cmask & -Cmask
            rest = Cmask ^ pivot
            value = rho[rest]
            T = rest
            while True:
                S = pivot | T
                value -= q.get(S, Fraction(0)) * rho[Cmask ^ S]
                if T == 0:
                    break
                T = (T - 1) & rest
            rho[Cmask] = value
    return rho


def non5_worst_coordinate_polynomials() -> dict[int, Fraction]:
    """Clique-coordinate polynomials at q_T = 4 b_T for T subset J."""
    q = {m: 4 * baseline(m) for m in range(1, 32) if not (m & 1)}
    return coordinate_rhos(q, J_MASK)


def affine_box_minimum() -> dict:
    """Independently verify the affine certificate on [b_S,4b_S].

    F(q)=rho(q)+sum lambda_S q_S is multi-affine.  Split the 31 variables
    into the 15 supports not containing 5 and the 16 containing 5.

    For each of the 2^15 non-5 corners, compute rho_C for C subset J.
    The recurrence on the 5-coordinate is

      rho_full = rho_J - sum_{T subset J} q_{5 union T} rho_{J\\T}.

    Hence, with the non-5 corner fixed, every 5-containing variable occurs
    independently with coefficient lambda_{5T}-rho_{J\\T}; choose its lower
    or upper endpoint according to the sign.  This reduces 2^31 corners to
    2^15 exact cases.
    """
    non5 = [m for m in range(1, 32) if not (m & 1)]
    best: Fraction | None = None
    best_non5_upper: tuple[int, ...] | None = None
    best_five_upper: tuple[int, ...] | None = None

    for bits in range(1 << len(non5)):
        q0: dict[int, Fraction] = {}
        for idx, mask in enumerate(non5):
            q0[mask] = baseline(mask) * (4 if bits & (1 << idx) else 1)

        rho = coordinate_rhos(q0, J_MASK)
        value = rho[J_MASK]
        value += sum(LAMBDA[m] * q0[m] for m in non5)

        five_upper: list[int] = []
        for T in range(32):
            if T & ~J_MASK:
                continue
            mask = 1 | T
            coeff = LAMBDA[mask] - rho[J_MASK ^ T]
            if coeff < 0:
                q5 = 4 * baseline(mask)
                five_upper.append(mask)
            else:
                q5 = baseline(mask)
            value += coeff * q5

        if best is None or value < best:
            best = value
            best_non5_upper = tuple(
                mask for idx, mask in enumerate(non5) if bits & (1 << idx)
            )
            best_five_upper = tuple(five_upper)

    assert best is not None
    return {
        "minimum": best,
        "non5_upper": best_non5_upper,
        "five_upper": best_five_upper,
    }


def lambda_baseline_sum() -> Fraction:
    return sum(LAMBDA[m] * baseline(m) for m in range(1, 32))


def fourteen_fiber_margin() -> Fraction:
    """14*C - 27*sum lambda_S*b_S."""
    return 14 * C - 27 * lambda_baseline_sum()


def seed_certificate() -> dict:
    """Run all exact arithmetic checks for the N*=11486475 certificate."""
    clique = non5_worst_coordinate_polynomials()
    box = affine_box_minimum()
    lam_sum = lambda_baseline_sum()
    margin = fourteen_fiber_margin()

    expected_clique = {
        0: Fraction(1),
        2: Fraction(3, 7),
        4: Fraction(7, 11),
        6: Fraction(17, 77),
        8: Fraction(9, 13),
        10: Fraction(23, 91),
        12: Fraction(59, 143),
        14: Fraction(109, 1001),
        16: Fraction(13, 17),
        18: Fraction(5, 17),
        20: Fraction(87, 187),
        22: Fraction(177, 1309),
        24: Fraction(113, 221),
        26: Fraction(19, 119),
        28: Fraction(699, 2431),
        30: Fraction(941, 17017),
    }
    assert clique == expected_clique
    assert min(clique.values()) == Fraction(941, 17017)
    assert box["minimum"] == C
    assert box["non5_upper"] == ()
    assert box["five_upper"] == (1, 9, 17)
    assert lam_sum == Fraction(144411, 425425)
    assert margin == Fraction(86563, 425425)
    assert margin > 0

    return {
        "N": 11486475,
        "clique_min": min(clique.values()),
        "affine_box_min": box["minimum"],
        "lambda_baseline_sum": lam_sum,
        "fourteen_fiber_margin": margin,
        "argmin_non5_upper": box["non5_upper"],
        "argmin_five_upper": box["five_upper"],
        "verified": True,
    }


__all__ = [
    "BASE",
    "C",
    "J_MASK",
    "LAMBDA",
    "PRIMES",
    "affine_box_minimum",
    "baseline",
    "coordinate_rhos",
    "fourteen_fiber_margin",
    "lambda_baseline_sum",
    "non5_worst_coordinate_polynomials",
    "seed_certificate",
]
