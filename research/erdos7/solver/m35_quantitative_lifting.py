"""M35: quantitative a=4 Clique-Shearer margins lift five a=5 frontier seeds.

The earlier M16/M25 certificates were used only qualitatively: a positive
summed rho margin implies at least one uncovered 3-adic fibre.  Here we retain
the size of that margin.

If N4=3^4*M and a staged certificate proves

    sum_{r in 41 selected fibres} rho(q(r)) >= eta,

while the associated completion audit guarantees that rho(q)>0 gives an
uncovered proportion at least rho(q), then

    delta(N4) >= M*eta.

The deficiency recurrence

    delta(3^5*M) >= 3*delta(3^4*M) - sigma(M)

therefore proves 3^5*M noncovering whenever

    3*eta > sigma(M)/M.

This module re-verifies the required a=4 margins exactly.  Four seeds use the
M16 diagonal-q_{5} certificate; the p=19 canonical seed uses the stronger M25
cross-support certificate.  Together they eliminate five of the six canonical
(5,2,1,1,1,1) M26 seeds, leaving only

    3^5 * 5^2 * 7 * 11 * 13 * 17

on the canonical branch.
"""
from __future__ import annotations

from fractions import Fraction
from math import prod

from m14_clique_shearer import J_MASK, coordinate_rhos
from m16_quadratic_frontier import LAMBDA as LAMBDA16, MU
from m25_cross_support_seed import (
    CROSS,
    DIAGONAL,
    LAMBDA as LAMBDA25,
)

NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))
FIVE_MASKS = tuple(1 | T for T in J_SUBSETS)

M16_EXPECTED_MARGINS = {
    (7, 11, 13, 23): Fraction(49732740695329, 83861791406250),
    (7, 11, 13, 29): Fraction(34454129718207371, 42463315034765625),
    (7, 11, 13, 31): Fraction(83924772650351557, 97044579663281250),
    (7, 11, 17, 19): Fraction(63881523541951, 76303450781250),
}
M25_P19_MARGIN = Fraction(
    3231212534728550154455103,
    4930518875613871540000000,
)

EXPECTED_LIFT_GAPS = {
    (7, 11, 13, 19): Fraction(
        1052798929867280671365309,
        4930518875613871540000000,
    ),
    (7, 11, 13, 23): Fraction(89914207333, 2150302343750),
    (7, 11, 13, 29): Fraction(
        10075865808207371,
        14154438344921875,
    ),
    (7, 11, 13, 31): Fraction(
        28331122538351557,
        32348193221093750,
    ),
    (7, 11, 17, 19): Fraction(
        20056203541951,
        25434483593750,
    ),
}

UNRESOLVED_CANONICAL = 3**5 * 5**2 * 7 * 11 * 13 * 17


def _baseline(coords: tuple[Fraction, ...], mask: int) -> Fraction:
    if len(coords) != 5 or not 1 <= mask < 32:
        raise ValueError("need five coordinates and a nonempty support mask")
    out = Fraction(1)
    for i, x in enumerate(coords):
        if mask & (1 << i):
            out *= x
    return out


def _coords(non5_primes: tuple[int, int, int, int]) -> tuple[Fraction, ...]:
    return (Fraction(6, 25),) + tuple(Fraction(1, p) for p in non5_primes)


def _clip(x: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    return lo if x < lo else hi if x > hi else x


def m16_tuple_certificate(non5_primes: tuple[int, int, int, int]) -> dict:
    """Exact M16 verifier for a general four-simple-prime post-stage tuple."""
    if non5_primes not in M16_EXPECTED_MARGINS:
        raise ValueError("tuple is not one of the M35 M16 anchors")
    b = {m: _baseline(_coords(non5_primes), m) for m in range(1, 32)}
    best = None
    proper_min = None
    full_min = None
    completion_max = None

    for bits in range(1 << len(NON5_MASKS)):
        q0 = {
            m: b[m] * (5 if bits & (1 << i) else 1)
            for i, m in enumerate(NON5_MASKS)
        }
        rho = coordinate_rhos(q0, J_MASK)
        for Cmask, value in rho.items():
            if Cmask == J_MASK:
                full_min = value if full_min is None or value < full_min else full_min
            else:
                proper_min = value if proper_min is None or value < proper_min else proper_min

        # Here 5*b_{5}=6/5.  If rho_J<=0, the full polynomial is bounded
        # above by this expression.  Negativity therefore proves that
        # full-rho positivity can occur only inside the non-5 Shearer region.
        completion = -rho[J_MASK] / 5
        completion -= sum(
            b[1 | T] * rho[J_MASK ^ T]
            for T in J_SUBSETS
            if T
        )
        completion_max = (
            completion if completion_max is None or completion > completion_max
            else completion_max
        )

        value = rho[J_MASK]
        value += sum(LAMBDA16[m] * q0[m] for m in NON5_MASKS)
        for T in J_SUBSETS:
            m = 1 | T
            if m == 1:
                continue
            coeff = LAMBDA16[m] - rho[J_MASK ^ T]
            value += coeff * b[m] * (5 if coeff < 0 else 1)

        coeff = LAMBDA16[1] - rho[J_MASK]
        q1 = _clip(-coeff / (2 * MU), b[1], 5 * b[1])
        value += coeff * q1 + MU * q1 * q1
        best = value if best is None or value < best else best

    assert best is not None and proper_min is not None and completion_max is not None
    lambda_cost = 81 * sum(LAMBDA16[m] * b[m] for m in range(1, 32))
    quadratic_cost = 197 * MU * b[1] ** 2
    margin = 41 * best - lambda_cost - quadratic_cost

    assert margin == M16_EXPECTED_MARGINS[non5_primes] > 0
    assert proper_min > 0
    assert completion_max < 0
    return {
        "non5_primes": non5_primes,
        "C": best,
        "summed_rho_margin": margin,
        "proper_non5_min": proper_min,
        "full_non5_min": full_min,
        "completion_upper_max": completion_max,
        "verified": True,
    }


def _quadratic_min(linear: Fraction, quadratic: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    if quadratic <= 0:
        raise ValueError("M25 diagonal coefficients must be positive")
    x = _clip(-linear / (2 * quadratic), lo, hi)
    return linear * x + quadratic * x * x


def m25_p19_certificate() -> dict:
    """Exact M25 cross-support margin at (7,11,13,19)."""
    non5_primes = (7, 11, 13, 19)
    b = {m: _baseline(_coords(non5_primes), m) for m in range(1, 32)}
    best = None
    proper_min = None
    full_min = None
    completion_max = None

    for bits in range(1 << len(NON5_MASKS)):
        q0 = {
            m: b[m] * (5 if bits & (1 << i) else 1)
            for i, m in enumerate(NON5_MASKS)
        }
        rho = coordinate_rhos(q0, J_MASK)
        for Cmask, value in rho.items():
            if Cmask == J_MASK:
                full_min = value if full_min is None or value < full_min else full_min
            else:
                proper_min = value if proper_min is None or value < proper_min else proper_min

        alpha = 5 * b[1] - 1
        completion = -alpha * rho[J_MASK]
        completion -= sum(
            b[1 | T] * rho[J_MASK ^ T]
            for T in J_SUBSETS
            if T
        )
        completion_max = (
            completion if completion_max is None or completion > completion_max
            else completion_max
        )

        value = rho[J_MASK]
        value += sum(LAMBDA25.get(m, Fraction(0)) * q0[m] for m in NON5_MASKS)
        value += sum(mu * q0[s] * q0[t] for (s, t), mu in CROSS.items())
        for T in J_SUBSETS:
            m = 1 | T
            linear = LAMBDA25.get(m, Fraction(0)) - rho[J_MASK ^ T]
            value += _quadratic_min(linear, DIAGONAL[m], b[m], 5 * b[m])
        best = value if best is None or value < best else best

    assert best is not None and proper_min is not None and completion_max is not None
    linear_cost = 81 * sum(
        LAMBDA25.get(m, Fraction(0)) * b[m] for m in range(1, 32)
    )
    diagonal_cost = 197 * sum(DIAGONAL[m] * b[m] ** 2 for m in FIVE_MASKS)
    cross_cost = 197 * sum(mu * b[s] * b[t] for (s, t), mu in CROSS.items())
    margin = 41 * best - linear_cost - diagonal_cost - cross_cost

    assert margin == M25_P19_MARGIN > 0
    assert proper_min > 0
    assert completion_max < 0
    return {
        "non5_primes": non5_primes,
        "C": best,
        "summed_rho_margin": margin,
        "proper_non5_min": proper_min,
        "full_non5_min": full_min,
        "completion_upper_max": completion_max,
        "verified": True,
    }


def sigma_over_M(non5_primes: tuple[int, int, int, int]) -> Fraction:
    """sigma(M)/M for M=5^2*prod(non5_primes)."""
    out = Fraction(31, 25)
    for p in non5_primes:
        out *= Fraction(p + 1, p)
    return out


def lift_gap(non5_primes: tuple[int, int, int, int], margin: Fraction) -> Fraction:
    """Normalized deficiency gap: 3*margin-sigma(M)/M."""
    return 3 * margin - sigma_over_M(non5_primes)


def lifted_seed_audit() -> dict:
    """Verify all five quantitative lifts and identify the sole canonical survivor."""
    margins = {(7, 11, 13, 19): m25_p19_certificate()["summed_rho_margin"]}
    for primes in M16_EXPECTED_MARGINS:
        margins[primes] = m16_tuple_certificate(primes)["summed_rho_margin"]

    gaps = {primes: lift_gap(primes, eta) for primes, eta in margins.items()}
    assert gaps == EXPECTED_LIFT_GAPS
    assert all(g > 0 for g in gaps.values())

    lifted_numbers = tuple(
        3**5 * 5**2 * prod(primes)
        for primes in sorted(gaps)
    )
    assert UNRESOLVED_CANONICAL not in lifted_numbers
    return {
        "lifted_seed_count": len(lifted_numbers),
        "lifted_numbers": lifted_numbers,
        "margins": margins,
        "normalized_lift_gaps": gaps,
        "unresolved_canonical": UNRESOLVED_CANONICAL,
        "verified": True,
    }


__all__ = [
    "EXPECTED_LIFT_GAPS",
    "M16_EXPECTED_MARGINS",
    "M25_P19_MARGIN",
    "UNRESOLVED_CANONICAL",
    "lift_gap",
    "lifted_seed_audit",
    "m16_tuple_certificate",
    "m25_p19_certificate",
    "sigma_over_M",
]
