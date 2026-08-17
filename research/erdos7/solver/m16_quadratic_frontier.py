"""M16: exact quadratic Clique-Shearer certificates for the first a=4 frontier.

For p in {17,19,23}, this module verifies that

    N_p = 3^4 * 5^2 * 7 * 11 * 13 * p

is not a covering number.

The input from M15 is the exact 3-adic moment data over 41 surviving fibres:

    sum_r q_S(r) <= 81 b_S,
    sum_r q_S(r)^2 <= 197 b_S^2.

Only the diagonal second moment for S={5} is needed below.

Pointwise, the verifier proves on the full support box b_S <= q_S <= 5 b_S

    rho(q) + sum_S lambda_S q_S + mu q_{5}^2 >= C_p,

with rational lambda_S >= 0 and mu=258/625.  The global minimum is checked
exactly: enumerate the 2^15 non-5 corners; for each corner the 15 remaining
5-containing variables other than {5} minimize at endpoints, while q_{5}
is a one-dimensional convex quadratic and is minimized exactly.

A separate exact audit checks that rho(q)>0 is sufficient for an uncovered
point even though the full non-5 four-coordinate polynomial is not positive
on the entire factor-5 box.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction

from m14_clique_shearer import J_MASK, coordinate_rhos


FRONTIER_PRIMES = (17, 19, 23)
NON5_MASKS = tuple(m for m in range(1, 32) if not (m & 1))
J_SUBSETS = tuple(T for T in range(32) if not (T & ~J_MASK))

MU = Fraction(258, 625)

LAMBDA = {
    1: Fraction(0),
    2: Fraction(3697, 10000),
    3: Fraction(3869, 5000),
    4: Fraction(1193, 5000),
    5: Fraction(7221, 10000),
    6: Fraction(2271, 5000),
    7: Fraction(8643, 10000),
    8: Fraction(2139, 10000),
    9: Fraction(3541, 5000),
    10: Fraction(781, 2000),
    11: Fraction(8503, 10000),
    12: Fraction(236, 625),
    13: Fraction(499, 625),
    14: Fraction(701, 1000),
    15: Fraction(2353, 2500),
    16: Fraction(951, 5000),
    17: Fraction(863, 1250),
    18: Fraction(5939, 10000),
    19: Fraction(4161, 5000),
    20: Fraction(2961, 10000),
    21: Fraction(7803, 10000),
    22: Fraction(6831, 10000),
    23: Fraction(9231, 10000),
    24: Fraction(3021, 10000),
    25: Fraction(7663, 10000),
    26: Fraction(6691, 10000),
    27: Fraction(9091, 10000),
    28: Fraction(2863, 5000),
    29: Fraction(2143, 2500),
    30: Fraction(19, 25),
    31: Fraction(1),
}

EXPECTED = {
    17: {
        "C": Fraction(27401186093, 53178125000),
        "lambda_b": Fraction(426240497, 2127125000),
        "margin": Fraction(2804670823, 13294531250),
        "proper_non5_min": Fraction(1, 91),
        "full_non5_min": Fraction(-258, 17017),
        "completion_upper_max": Fraction(-744, 85085),
    },
    19: {
        "C": Fraction(78588921636187, 153494028187500),
        "lambda_b": Fraction(233934989, 1188687500),
        "margin": Fraction(704120180922703, 1918675352343750),
        "proper_non5_min": Fraction(1, 91),
        "full_non5_min": Fraction(-236, 19019),
        "completion_upper_max": Fraction(-4766, 475475),
    },
    23: {
        "C": Fraction(5953112226799, 11740650796875),
        "lambda_b": Fraction(27556447, 143893750),
        "margin": Fraction(49732740695329, 83861791406250),
        "proper_non5_min": Fraction(1, 91),
        "full_non5_min": Fraction(-192, 23023),
        "completion_upper_max": Fraction(-6858, 575575),
    },
}


def baseline_p(mask: int, last_prime: int) -> Fraction:
    """b_S for support mask S on coordinates (5,7,11,13,p)."""
    if not 1 <= mask < 32:
        raise ValueError("support mask must be in 1..31")
    base = (
        Fraction(6, 25),
        Fraction(1, 7),
        Fraction(1, 11),
        Fraction(1, 13),
        Fraction(1, last_prime),
    )
    out = Fraction(1)
    for i, x in enumerate(base):
        if mask & (1 << i):
            out *= x
    return out


def _clip_fraction(x: Fraction, lo: Fraction, hi: Fraction) -> Fraction:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


@lru_cache(maxsize=None)
def frontier_certificate(last_prime: int) -> dict:
    """Run the exact 2^15 pointwise and Shearer-completion audit."""
    if last_prime not in FRONTIER_PRIMES:
        raise ValueError(f"unsupported certified prime: {last_prime}")

    b = {m: baseline_p(m, last_prime) for m in range(1, 32)}

    best: Fraction | None = None
    proper_non5_min: Fraction | None = None
    full_non5_min: Fraction | None = None
    completion_upper_max: Fraction | None = None

    for bits in range(1 << len(NON5_MASKS)):
        q0 = {
            mask: b[mask] * (5 if bits & (1 << idx) else 1)
            for idx, mask in enumerate(NON5_MASKS)
        }
        rho = coordinate_rhos(q0, J_MASK)

        for Cmask, value in rho.items():
            if Cmask == J_MASK:
                if full_non5_min is None or value < full_non5_min:
                    full_non5_min = value
            else:
                if proper_non5_min is None or value < proper_non5_min:
                    proper_non5_min = value

        completion_upper = -rho[J_MASK] / 5
        completion_upper -= sum(
            b[1 | T] * rho[J_MASK ^ T]
            for T in J_SUBSETS
            if T != 0
        )
        if completion_upper_max is None or completion_upper > completion_upper_max:
            completion_upper_max = completion_upper

        value = rho[J_MASK]
        value += sum(LAMBDA[m] * q0[m] for m in NON5_MASKS)

        for T in J_SUBSETS:
            mask = 1 | T
            if mask == 1:
                continue
            coeff = LAMBDA[mask] - rho[J_MASK ^ T]
            q5 = b[mask] * (5 if coeff < 0 else 1)
            value += coeff * q5

        coeff1 = LAMBDA[1] - rho[J_MASK]
        q1 = _clip_fraction(-coeff1 / (2 * MU), b[1], 5 * b[1])
        value += coeff1 * q1 + MU * q1 * q1

        if best is None or value < best:
            best = value

    assert best is not None
    assert proper_non5_min is not None
    assert full_non5_min is not None
    assert completion_upper_max is not None

    lambda_b = sum(LAMBDA[S] * b[S] for S in range(1, 32))
    margin = 41 * best - 81 * lambda_b - 197 * MU * b[1] * b[1]

    expected = EXPECTED[last_prime]
    assert best == expected["C"]
    assert lambda_b == expected["lambda_b"]
    assert margin == expected["margin"]
    assert proper_non5_min == expected["proper_non5_min"]
    assert full_non5_min == expected["full_non5_min"]
    assert completion_upper_max == expected["completion_upper_max"]

    assert proper_non5_min > 0
    assert completion_upper_max < 0
    assert margin > 0

    N = 3**4 * 5**2 * 7 * 11 * 13 * last_prime
    return {
        "last_prime": last_prime,
        "N": N,
        "C": best,
        "lambda_b": lambda_b,
        "mu": MU,
        "proper_non5_min": proper_non5_min,
        "full_non5_min": full_non5_min,
        "completion_upper_max": completion_upper_max,
        "summed_margin": margin,
        "noncovering_certified": True,
    }


def certified_frontier() -> dict[int, dict]:
    return {p: frontier_certificate(p) for p in FRONTIER_PRIMES}


__all__ = [
    "EXPECTED",
    "FRONTIER_PRIMES",
    "LAMBDA",
    "MU",
    "baseline_p",
    "certified_frontier",
    "frontier_certificate",
]
