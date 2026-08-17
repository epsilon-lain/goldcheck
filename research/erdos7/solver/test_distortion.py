"""Tests for the Hough--Nielsen Theorem 4 distortion layer."""

from covering import divisors
from distortion import (
    hn_theorem4_bruteforce_check,
    hn_uncovered_density,
    prime_support,
)


def test_hn_weights_reproduce_small_cases():
    # N=3 is non-covering; the fixed point is x_3 = 1/2.
    r = hn_uncovered_density([3], [3])
    assert r["exists"] is True
    assert r["weights"][3] >= __import__("fractions").Fraction(1, 2)

    # N=12 is a covering number, so no fixed point exists.
    primes = prime_support(12)
    moduli = [d for d in divisors(12) if d > 1]
    assert hn_uncovered_density(primes, moduli)["exists"] is False


def test_hn_theorem4_is_valid_for_prime_powers():
    assert hn_theorem4_bruteforce_check(9) is True
    assert hn_theorem4_bruteforce_check(27) is True
