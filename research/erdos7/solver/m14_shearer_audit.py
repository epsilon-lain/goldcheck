"""Independent Milestone 14 audit of the Clique-Shearer conditioning step.

This module deliberately does not reuse the affine-box optimizer/certificate logic.
It checks the one point that was left as a mathematical audit item in M14:
for every non-5 vector q_T in the full box b_T <= q_T <= 4 b_T, every
Clique-Shearer coordinate polynomial rho_C is positive.

Because every rho_C is multi-affine, its minimum on a box is attained at a
corner.  There are only 15 non-5 support variables, hence 2^15 corners.
"""

from __future__ import annotations

from fractions import Fraction

from m14_clique_shearer import J_MASK, baseline, coordinate_rhos


NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))


def non5_box_coordinate_minima() -> dict[int, Fraction]:
    """Exact minima of rho_C on the whole non-5 box [b_T,4b_T]."""
    minima: dict[int, Fraction | None] = {
        C: None for C in range(32) if not (C & ~J_MASK)
    }

    for bits in range(1 << len(NON5_MASKS)):
        q = {
            mask: baseline(mask) * (4 if bits & (1 << idx) else 1)
            for idx, mask in enumerate(NON5_MASKS)
        }
        rho = coordinate_rhos(q, J_MASK)
        for C, value in rho.items():
            old = minima[C]
            if old is None or value < old:
                minima[C] = value

    return {C: value for C, value in minima.items() if value is not None}


def split_recurrence_identity(q: dict[int, Fraction]) -> tuple[Fraction, Fraction]:
    """Check the exact prime-5 split of the full independence polynomial.

    Any independent support family contains at most one support involving the
    5-coordinate.  Hence

        rho_[5 union J] = rho_J
            - sum_{T subset J} q_{5 union T} rho_{J\T}.

    The first value below is computed directly on all five coordinates; the
    second uses the split formula.
    """
    full = coordinate_rhos(q, 31)[31]
    q0 = {m: value for m, value in q.items() if not (m & 1)}
    rho0 = coordinate_rhos(q0, J_MASK)
    split = rho0[J_MASK]
    for T in range(32):
        if T & ~J_MASK:
            continue
        split -= q.get(1 | T, Fraction(0)) * rho0[J_MASK ^ T]
    return full, split


def shearer_audit() -> dict:
    """Run the exact independent audit used to close the M14 conditioning gap."""
    minima = non5_box_coordinate_minima()
    expected_global_min = Fraction(941, 17017)
    assert minima
    assert min(minima.values()) == expected_global_min
    assert all(value > 0 for value in minima.values())

    # A deterministic interior rational vector, chosen independently of the
    # affine certificate, checks the five-coordinate split recurrence.
    q = {
        mask: baseline(mask) * Fraction(2 + (mask.bit_count() % 2), 1)
        for mask in range(1, 32)
    }
    direct, split = split_recurrence_identity(q)
    assert direct == split

    return {
        "non5_coordinate_count": len(minima),
        "non5_box_min": expected_global_min,
        "all_non5_coordinates_positive": True,
        "five_coordinate_split_exact": True,
    }


__all__ = [
    "NON5_MASKS",
    "non5_box_coordinate_minima",
    "shearer_audit",
    "split_recurrence_identity",
]
